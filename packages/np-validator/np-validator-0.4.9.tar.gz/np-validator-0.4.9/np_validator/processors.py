from typing import Any

import logging
import pickle
import sys

logger = logging.getLogger(__name__)

try:
    from .sync_dataset import Dataset
except ImportError as ie:
    if sys.version_info[1] < 8:  # numpy only supported for 3.8+
        logger.debug("Numpy not supported for python versions < 3.8")
    else:
        raise ie


def unpickle(filepath: str, encoding: str = "latin1") -> Any:
    """Unpickles a filepath to an arbitrary object.

    Args:
        filepath (str): Filepath to unpickle.
        encoding (str): Encoding used to unpickle.

    Returns:
        unpickled: Unpickled object.
    """
    with open(filepath, "rb") as f:
        return pickle.load(f, encoding=encoding)  # nosec


def load_data_set(filepath: str) -> Dataset:
    """Loads a sync Dataset instance from a filepath.

    Args:
        filepath (str): Filepath to load.

    Returns:
        loaded (Dataset): Loaded dataset.
    """
    return Dataset(filepath)
