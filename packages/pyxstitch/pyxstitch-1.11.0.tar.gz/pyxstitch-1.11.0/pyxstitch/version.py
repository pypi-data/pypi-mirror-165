#!/usr/bin/python3
"""Set version attribute."""
import sys

__version__ = "1.11.0"

_MIN_VERS = (3, 7)


def python_version_supported(version=None):
    """Check (exits) that the python version is supported."""
    vers = version
    if vers is None:
        vers = sys.version_info
    return vers >= _MIN_VERS
