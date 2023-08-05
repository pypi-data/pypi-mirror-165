#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path

SCRIPTDIR = path.abspath(path.dirname(__file__))

with open(path.join(SCRIPTDIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
                             name = "termwriter",
                      description = "Organize your terminal output.",
                          version = "1.0.0",
                          license = "Apache 2.0",
                           author = "Mark Kim",
                     author_email = "markuskimius+py@gmail.com",
                              url = "https://github.com/markuskimius/termwriter-py",
                         keywords = [ "screen", "stdout" ],
                 long_description = long_description,
    long_description_content_type = "text/markdown",
                         packages = find_packages("lib"),
                      package_dir = { "": "lib" },
)
