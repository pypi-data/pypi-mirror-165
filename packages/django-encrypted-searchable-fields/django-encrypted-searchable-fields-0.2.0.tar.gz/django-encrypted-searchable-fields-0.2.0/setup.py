#!/usr/bin/env python

from setuptools import setup

setup(
    name="django-encrypted-searchable-fields",
    version="0.2.0",
    license="MIT",
    description="A fork of django-searchable-encrypted-fields with a bug fix.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Guy Willett",
    author_email="<guy@chamsoft.co>",
    maintainer="Kenny Lajara",
    url="https://github.com/ucoran-saas/django-encrypted-searchable-fields/",
    packages=["encrypted_fields"],
    install_requires=["Django>=3.2", "pycryptodome>=3.7.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
    ],
)
