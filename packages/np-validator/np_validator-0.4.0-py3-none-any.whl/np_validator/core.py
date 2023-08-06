from typing import Any, Dict, List, Tuple, Union

import logging

from .dataclasses import (
    BuiltinCallable,
    ValidationResult,
    ValidationStep,
    load_ValidationStep,
)
from .exceptions import ParsingError, ValidationError
from .path_matching import path_matches_pattern

logger = logging.getLogger(__name__)


def run_BuiltinCallable(target: Any, builtin: BuiltinCallable) -> Any:
    """Runs a BuiltinCallable on an arbitrary value."""
    return builtin.resolved_function(
        target,
        **builtin.args,
    )


def run_ValidationStep(filepath: str, step: ValidationStep) -> ValidationResult:
    """Runs a single validation step.

    Args:
        filepath (str): filepath of data to validate.
        step (ValidationStep): validation step to run.

    Returns:
        result (ValidationResult): result of the validation
    """
    if step.processor:
        processed = run_BuiltinCallable(
            filepath,
            step.processor.builtin,
        )  # type: Union[Any, str]
    else:
        processed = filepath

    return ValidationResult(
        filepath=filepath,
        results=[
            run_BuiltinCallable(processed, validator.builtin)
            for validator in step.validators
        ],
    )


def run_validation(
    file_list: List[str], validation_steps: List[ValidationStep]
) -> List[ValidationResult]:
    """Validates a list of files.

    Args:
        file_list (:obj:`list` of :obj:`str`): List of filepaths to validate.
        validation_steps: List of validation steps to run.

    Returns:
        results: List of validation results.
    """
    results = []
    for validation_step in validation_steps:
        for filepath in file_list:
            if path_matches_pattern(filepath, validation_step.path_suffix):
                results.append(
                    run_ValidationStep(
                        filepath,
                        validation_step,
                    )
                )

    return results
