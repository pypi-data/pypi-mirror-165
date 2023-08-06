import os
from dotenv import load_dotenv
from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

load_dotenv("./src/.env")
MAJOR_VERSION = int(os.getenv("MAJOR_VERSION"))
MINOR_VERSION = int(os.getenv("MINOR_VERSION"))
VERSION_STRING = f"{MAJOR_VERSION}.{MINOR_VERSION}"

setup(
    name="cgcsdk",
    # version=VERSION_STRING,
    version="0.2.4",
    description="Comtegra GPU Cloud REST API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Comtegra/cgc",
    author="Comtegra AI Team",
    author_email="info@comtegra.pl",
    keywords=["cloud", "sdk"],
    license="BSD 2-clause",
    packages=find_packages(exclude=["src.tests.*, src.tests"]),
    package_data={"src": [".env"]},
    py_modules=["src/cgc"],
    install_requires=[
        "click",
        "python-dotenv",
        "tabulate",
        "pycryptodomex",
        "paramiko>=2.11",
        "statsd",
        "requests",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "cgc = src.cgc:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
