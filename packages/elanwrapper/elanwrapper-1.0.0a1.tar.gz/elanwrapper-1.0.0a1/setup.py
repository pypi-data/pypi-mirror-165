from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name = "elanwrapper",
    author = "PALAT Labs",
    version="1.0.0a01",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pympi-ling>=1.69",
        "sortedcontainers>=2.4.0",
    ],
)
