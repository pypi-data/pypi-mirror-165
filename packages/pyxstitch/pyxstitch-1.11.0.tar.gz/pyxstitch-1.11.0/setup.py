#!/usr/bin/python3

"""Setup for pyxstitch."""

from setuptools import setup

__pkg_name__ = "pyxstitch"

long_description = ""
with open("README.rst", 'r') as f:
    long_description = f.read()

installs = []
with open("requirements.txt", "r") as f:
    for line in f:
        installs += [line.strip().replace(" ", "")]

vers = ""
min_vers = ""
with open("pyxstitch/version.py", "r") as f:
    for line in f:
        stripped = line.strip()
        if stripped.startswith("__version__"):
            vers = stripped.split("=")[1].strip().replace('"', '')
        if stripped.startswith("_MIN_VERS"):
            min_vers = stripped.split("=")[1].strip().replace(", ", ".")
            min_vers = min_vers.replace("(", "").replace(")", "").strip()

setup(
    author="Sean Enck",
    author_email="enckse@voidedtech.com",
    name=__pkg_name__,
    version=vers,
    description='Convert source code to cross stitch patterns',
    long_description=long_description,
    url='https://github.com/enckse/pyxstitch',
    license='GPL3',
    python_requires='>={}'.format(min_vers),
    packages=[__pkg_name__, __pkg_name__ + ".fonts"],
    install_requires=installs,
    keywords='crossstitch cross stitch',
    entry_points={
        'console_scripts': [
            'pyxstitch = pyxstitch.pyxstitch:main',
        ],
    },
)
