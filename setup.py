#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from setuptools import setup

metadata = load_source("metadata", "jsonserver/__init__.py")

setup(
    name="jsonserver",
    version=metadata.__VERSION__,
    license="GPL",
    description="Simple pythonic json backend server to easily test frontends",
    author=metadata.__AUTHOR__,
    author_email=metadata.__AUTHOR_EMAIL__,
    maintainer=metadata.__AUTHOR__,
    maintainer_email=metadata.__AUTHOR_EMAIL__,
    platforms=["Linux", "Windows", "MAC OS X"],
    url="http://github.com/timofurrer/jsonserver",
    download_url="http://github.com/timofurrer/jsonserver",
    install_requires=[""],
    packages=["jsonserver"],
    entry_points={"console_scripts": ["jsonserver = jsonserver.main:main"]},
    package_data={"jsonserver": ["*.md"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing"
    ],
)
