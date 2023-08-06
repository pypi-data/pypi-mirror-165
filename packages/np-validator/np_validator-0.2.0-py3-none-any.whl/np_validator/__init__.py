# type: ignore[attr-defined]
"""Awesome `np-validator` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""

import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

from .core import run_validation
from .dataclasses import Processor, ValidationStep, Validator, load_ValidationStep


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
