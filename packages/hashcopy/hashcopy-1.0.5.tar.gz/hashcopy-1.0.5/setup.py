#!/usr/bin/env python3

from setuptools import setup, Extension

setup(
    name = "hashcopy",
    version = "1.0.5",
    url="https://ktpanda.org/software/hashcopy",
    author = "Katie Rust",
    author_email = "katie@ktpanda.org",
    readme = "README.md",
    description = "Copy a file in the most efficient way possible while generating a SHA256 hash of the data",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux"
    ],
    ext_modules=[
        Extension(
            "hashcopy",
            sources=["hashcopy.c"],
            libraries=['crypto'],
            py_limited_api=True,
        )
    ]
)
