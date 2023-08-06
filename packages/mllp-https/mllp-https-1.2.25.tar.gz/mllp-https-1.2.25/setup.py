#!/usr/bin/env python3
import os
import setuptools

version = {}
with open("mllp_http_https/version.py", "r") as f:
    exec(f.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author="Tiago Rodrigues/SECTRA Iberia",
    author_email="tiagoepr@hotmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    description="Translate between MLLP and HTTP/HTTPS",
    entry_points={
        "console_scripts": [
            "mllp2http=mllp_http_https.main:mllp2http",
            "http2mllp=mllp_http_https.main:http2mllp",
            "mllp2https=mllp_http_https.main:mllp2https",
            "https2mllp=mllp_http_https.main:https2mllp",
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests"
    ],
    name="mllp-https",
    packages=setuptools.find_packages(),
    project_urls={
        "Issues": "https://github.com/tiagoepr/mllp-https/issues",
        "Original Project by Rivet Health": "https://github.com/rivethealth/mllp-http/",
    },
    url="https://github.com/tiagoepr/mllp-https",
    version=version["__version__"],
)
