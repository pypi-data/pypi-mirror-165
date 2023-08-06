from asyncio.coroutines import iscoroutinefunction
from logging import error
from typing import Dict
import paho.mqtt.client as mqtt
import os
import urllib
import time
import base64
import json
import socket
import asyncio
import threading
import ssl

# TODO: $iothub/methods/POST/# is unnecessary in topics
# TODO: on_settings does not work when not used
# TODO: generate sas on reconnect


class Module:
    topics = [
        "$iothub/twin/res/#",  # Twin-Get or Twin-Patch
        "$iothub/methods/POST/#",  # direct method calls
        "$iothub/twin/PATCH/properties/desired/#",
    ]

    def sign(self, data):
        gen_id = urllib.parse.quote(os.environ["IOTEDGE_MODULEGENERATIONID"])
        api_ver = urllib.parse.quote(os.environ["IOTEDGE_APIVERSION"])
        workload = os.environ["IOTEDGE_WORKLOADURI"]

        module = urllib.parse.quote((self.module_id))
        host = workload.split('/').pop()

        b64_encoded = base64.b64encode(bytes(data, 'ascii'))
        req_data = {"algo": "HMACSHA256",
                    "keyId": "primary",
                    "data": b64_encoded.decode('ascii')
                    }
        payload = json.dumps(req_data)
        req = f"POST http://{host}/modules/{module}/genid/{gen_id}/sign?api-version={api_ver} HTTP/1.1\r\n"
        req += f"Content-Type: application/json\r\n"
        req += f"Content-Length: {len(payload)}\r\n"
        req += f"\r\n{payload}"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(workload.split("://").pop())

        sock.send(bytes(req, 'ascii'))

        buf = sock.recv(4096)
        sock.close()

        lines = buf.decode('ascii').strip().split("\n")
        first = lines[0].strip()
        last = lines.pop().strip("\0")

        if first != "HTTP/1.1 200 OK":
            raise error("Cannot sign")

        res = json.loads(last)
        return res.get('digest')

    def get_module_token(self, expiry_in_seconds=3600):
        expiry = str(int(time.time() + expiry_in_seconds))
        resource = urllib.parse.quote(
            f"{self.iot_hub_hostname}/devices/{self.device_id}/modules/{self.module_id}")
        data_to_sign = f"{resource}\n{expiry}"
        signature = urllib.parse.quote(self.sign(data_to_sign))
        return f"SharedAccessSignature sr={resource}&sig={signature}&se={expiry}"

    def get_connect_options(self):
        self.host = host = os.environ['IOTEDGE_GATEWAYHOSTNAME']
        self.device_id = os.environ['IOTEDGE_DEVICEID']
        self.module_id = os.environ['IOTEDGE_MODULEID']
        self.iot_hub_hostname = os.environ['IOTEDGE_IOTHUBHOSTNAME']

        client_id = f"{self.device_id}/{self.module_id}"
        login = f"{self.iot_hub_hostname}/{self.device_id}/{self.module_id}/?api-version=2018-06-30"

        password = self.get_module_token(36000)
        return client_id, login, password, host

    async def connect(self):
        self.rid = 1000
        client_id, login, password, host = self.get_connect_options()

        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(login, password)

        def disconnect_handler(a, b, c):
            print("MQTT Disconnected", flush=True)
            client_id, login, password, host = self.get_connect_options()
            self.client.username_pw_set(login, password)
            print(f"updated login={login} pw={password}", flush=True)
            try:
                self.client.reconnect()
            except:
                print(f"cannot reconnect")
                return disconnect_handler(a, b, c)

        def connect_handler(a, b, c, d):
            print("MQTT Connected", flush=True)
            for topic in self.topics:
                print(f"Re-subscribed to {topic}")
                self.client.subscribe(topic)

        self.client.on_disconnect = disconnect_handler
        self.client.on_connect = connect_handler
        self.client.on_message = lambda c, u, message: print(
            "Unhandled message", message.topic, message.payload, flush=True)

        self.client.connect(host)
        self.client.loop_start()

        if not self.client.is_connected:
            raise error("MQTT server rejected connection")

        print("IoT module connected", flush=True)

        twin: Dict = await self.get_twin()
        self.settings = twin.get('desired')

        print("Settings", self.settings, flush=True)

        def on_restart(params):
            def exit_after():
                time.sleep(1)
                raise os._exit(0)

            t1 = threading.Thread(target=exit_after)
            t1.start()
            return "Restarting"

        self.on_method('restart', on_restart)

    def on_settings(self, cb):
        def handler(topic, payload):
            data = json.loads(payload)
            cb(data)
        self.subscribe_mqtt("$iothub/twin/PATCH/properties/desired/+", handler)

    async def update_telemetry(self, data):
        id = str(self.rid)
        self.rid += 1
        filter = f"$iothub/twin/res/+/?$rid={id}"
        future = asyncio.get_running_loop().create_future()

        def handler(c, u, message: mqtt.MQTTMessage):
            topic: str = message.topic

            code = topic.split("/")[3]
            future.set_result(code)

        self.client.message_callback_add(filter, handler)

        self.publish_mqtt(
            f"$iothub/twin/PATCH/properties/reported/?$rid={id}", json.dumps(data))

        while not future.done():
            await asyncio.sleep(.1)

        self.client.message_callback_remove(filter)
        return future.result()

    async def get_twin(self):
        if not self.client:
            raise error("Client not initialized")

        id = str(self.rid)
        self.rid += 1
        filter = f"$iothub/twin/res/+/?$rid={id}"

        future = asyncio.get_running_loop().create_future()

        def handler(c, u, message: mqtt.MQTTMessage):
            topic: str = message.topic

            code = topic.split("/")[3]
            if code != "200":
                future.set_exception(f"Cannot fetch twin, code={code}")
                return

            result = json.loads(message.payload.decode('utf-8'))
            print("msg is ready", result, flush=True)

            future.set_result(result)

        self.client.message_callback_add(filter, handler)

        self.publish_mqtt(f"$iothub/twin/GET/?$rid={id}", "")

        while not future.done():
            await asyncio.sleep(.1)

        self.client.message_callback_remove(filter)
        return future.result()

    def on_method(self, name: str, cb):
        async def handler(topic: str, payload: bytes):
            [notused, rid] = topic.split("=")
            try:
                data = json.loads(payload.decode())
                if asyncio.iscoroutinefunction(cb):
                    result = await cb(data)
                else:
                    result = cb(data)

                self.publish_mqtt(
                    f"$iothub/methods/res/{200}/?$rid={rid}", json.dumps(result))
            except Exception as e:
                print(f"Error when handling method {name}: {e}", flush=True)
                self.publish_mqtt(
                    f"$iothub/methods/res/{500}/?$rid={rid}", json.dumps("error"))
                pass

        self.subscribe_mqtt(f"$iothub/methods/POST/{name}/+", handler)

    def subscribe(self, type: str, cb):
        if not '/' in type:
            type = 'message/' + type

        async def handler(topic: str, payload):
            args = json.loads(payload)
            type = topic.split("/")[3]
            if asyncio.iscoroutinefunction(cb):
                await cb(args, type)
            else:
                cb(args, type)

        self.subscribe_mqtt(f"ombori/grid/{type}", handler)

    def on_event(self, type: str, cb):
        self.subscribe(type, cb)

    def publish(self, type: str, payload):
        if not '/' in type:
            type = 'message/' + type

        data = json.dumps(payload)
        self.publish_mqtt(f"ombori/grid/{type}", data)

    def broadcast(self, type: str, payload):
        self.publish(type, payload)

    # FIXME: blocking
    def publish_mqtt(self, topic: str, payload):
        if not self.client:
            raise error("Client not initialized")

        self.client.publish(topic, payload)

    def subscribe_mqtt(self, topic: str, cb):
        if not self.client:
            raise error("Client not initialized")

        def handler(c, u, message):
            if asyncio.iscoroutinefunction(cb):
                async def subhandler():
                    await cb(message.topic, message.payload)
                asyncio.run(subhandler)
            else:
                cb(message.topic, message.payload)

        self.client.subscribe(topic)
        self.topics.append(topic)
        self.client.message_callback_add(topic, handler)

    # FIXME: blocking
    async def invoke(self, moduleId: str, method: str, payload={}, connect_timeout=15, response_timeout=15):
        myssl = ssl.create_default_context()
        myssl.check_hostname = False
        myssl.verify_mode = ssl.CERT_NONE

        data = {
            "methodName": method,
            "payload": payload,
            "connectTimeoutInSeconds": connect_timeout,
            "responseTimeoutInSeconds": response_timeout
        }

        req = urllib.request.Request(
            f"https://{self.host}/twins/{urllib.parse.quote(self.device_id)}/modules/{urllib.parse.quote(moduleId)}/methods")
        req.add_header('content-type', 'application/json')
        req.add_header('x-ms-edge-moduleId',
                       f"{self.device_id}/{self.module_id}")
        req.add_header('authorization', self.get_module_token())
        req.data = json.dumps(data).encode("utf-8")

        contents: bytes = urllib.request.urlopen(req, context=myssl).read()
        return json.loads(contents.decode('utf-8'))
