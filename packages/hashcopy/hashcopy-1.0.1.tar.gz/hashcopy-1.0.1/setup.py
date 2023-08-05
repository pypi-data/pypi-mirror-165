#!/usr/bin/env python3

from setuptools import setup, Extension

setup(
    url="https://ktpanda.org/software/hashcopy",
    ext_modules=[
        Extension(
            "hashcopy",
            sources=["hashcopy.c"],
            libraries=['crypto'],
            py_limited_api=True,
        )
    ]
)
