# function-burger 🍔 by shinya_sun_sun, MIT license

from setuptools import setup

import function_burger

DESCRIPTION = "function-burger🍔 is a library that outputs logs \
before and(or) after a function."
NAME = "function-burger"
AUTHOR = "shinya_sun_sun"
AUTHOR_EMAIL = "dynabook.miu@gmail.com"
URL = "https://github.com/MamedenQ/function-burger"
LICENSE = "MIT License"
DOWNLOAD_URL = "https://github.com/MamedenQ/function-burger"
VERSION = function_burger.__version__
PYTHON_REQUIRES = ">=3.7"

INSTALL_REQUIRES: list[str] = []

EXTRAS_REQUIRE: dict[str, list[str]] = {
    "testing": [
        "pytest",
        "pytest-cov",
    ],
}

PACKAGES = ["function_burger"]

CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
)
