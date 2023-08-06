from marshmallow import Schema, fields, post_load, validate

from .. import processors, validators
from .utils import list_functions


class ProcessorSchema(Schema):

    """Serialized builtin callable"""

    name = fields.String(validate=validate.OneOf(list_functions(processors)))
    args = fields.Dict(load_default={})


class ValidatorSchema(Schema):

    """Serialized builtin callable"""

    name = fields.String(validate=validate.OneOf(list_functions(validators)))
    args = fields.Dict(load_default={})


class ValidationStepSchema(Schema):

    """Serialized validation step"""

    path_suffix = fields.String()
    processor = fields.Nested(ProcessorSchema, many=False)
    validators = fields.Nested(ValidatorSchema, many=True)


class ValidationResultSchema(Schema):

    """Serialized validation result"""

    filepath = fields.String()
    results = fields.List(
        fields.Tuple(
            (
                fields.Raw(),
                fields.Bool(),
            )
        )
    )
