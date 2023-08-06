# put here as an easy way to isolate dependencies and not
# populate validators function namespace
import logging
import sys

logger = logging.getLogger(__name__)

try:
    import numpy as np
except ImportError as ie:
    if sys.version_info[1] < 8:  # numpy only supported for 3.8+
        logger.debug("Numpy not supported for python versions < 3.8")
    else:
        raise ie


def rate(timestamps):
    return 1 / np.median(np.diff(timestamps))


def above_minimum(value, threshold):
    validation_bool = value > threshold
    return validation_bool


def within_tolerance(value, tolerance, threshold):
    return (threshold - tolerance) < value < (threshold + tolerance)
