from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple

from dataclasses import dataclass, field

from .. import processors, validators
from .schemas import ValidationResultSchema, ValidationStepSchema
from .utils import list_functions, resolve_function


@dataclass
class BuiltinCallable:

    """Resolved builtin callable function."""

    resolved_function: Callable[..., Tuple[Any, bool]]
    args: Dict[str, Any]


@dataclass
class Processor:

    """Processor abstraction.

    Args:
        name (str): Name of the processor to use.
        args (:obj:`dict`, optional): Additional arguments supplied to builtin.

    Attributes:
        name (str): Name of the processor.
        args (dict): Additional arguments supplied to builtin.
        builtin (BuiltinCallable): BuiltinCallable instance resolved from `name`.

    Note:
        Refer to `Supported Processors` for a list of supported `name` to use.
    """

    name: str
    args: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        self.builtin = load_BuiltinCallable(
            processors,
            {
                "name": self.name,
                "args": self.args,
            },
        )


@dataclass
class Validator:

    """Validator abstraction.

    Args:
        name (str): Name of the validator to use.
        args (:obj:`dict`, optional): Additional arguments supplied to builtin.

    Attributes:
        name (str): Name of the validator.
        args (dict): Additional arguments supplied to builtin.
        builtin (BuiltinCallable): BuiltinCallable instance resolved from `name`.

    Note:
        Refer to `Supported Validators` for a list of supported `name` to use.
    """

    name: str
    args: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        self.builtin = load_BuiltinCallable(
            validators,
            {
                "name": self.name,
                "args": self.args,
            },
        )


@dataclass
class ValidationStep:

    """Validation step abstraction.

    Attributes:
        path_suffix: Filepath suffix matched against filepaths. Determines what filepaths this step will be called on.
        processor: Processors to use on filepath before validation.
        validators: Validators to apply to a matched filepath, or processor output, if a Processor is supplied.
    """

    path_suffix: str
    processor: Optional[Processor] = None
    validators: List[Validator] = field(default_factory=lambda: [])


@dataclass
class ValidationResult:

    filepath: str
    results: List[Any] = field(default_factory=lambda: [])


validation_step_schema = ValidationStepSchema()


def validate_ValidationStep_data(data: dict) -> dict:  # type: ignore
    """Validates that a dictionary has the shape we expect for ValidationStep."""
    return validation_step_schema.load(data)  # type: ignore


def load_BuiltinCallable(mod: ModuleType, data: dict) -> BuiltinCallable:  # type: ignore
    """Loads a BuiltinCallable from a structured dictionary."""
    return BuiltinCallable(
        resolved_function=resolve_function(
            mod,
            data["name"],
        ),
        args=data["args"],
    )


def load_ValidationStep(data: dict) -> ValidationStep:  # type: ignore
    """Loads a ValidationStep from a structured dictionary."""
    validated = validate_ValidationStep_data(data)

    processor_data = validated.get("processor")

    if processor_data:
        loaded_processor = Processor(**processor_data)  # type: Processor
    else:
        loaded_processor = None

    loaded_validators = [
        Validator(**validator_data) for validator_data in validated["validators"]
    ]

    return ValidationStep(
        path_suffix=data["path_suffix"],
        processor=loaded_processor,
        validators=loaded_validators,
    )


validation_result_schema = ValidationResultSchema()


def dump_ValidationResult(result: ValidationResult) -> dict:
    return validation_result_schema.dump(result)
