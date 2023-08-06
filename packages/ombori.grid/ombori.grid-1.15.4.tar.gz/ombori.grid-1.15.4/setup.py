from setuptools import setup, find_packages

setup(
    name='ombori.grid',
    version='1.15.4',
    packages=find_packages(where="src"),
    install_requires=["paho-mqtt"],
    package_dir={"": "src"},
    python_requires=">=3.6",
)
