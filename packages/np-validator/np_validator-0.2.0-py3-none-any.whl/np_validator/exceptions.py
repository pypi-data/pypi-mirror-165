class NpValidatorError(Exception):

    """General error base."""


class ValidationError(Exception):

    """Some part of the validation critically failed."""


class ParsingError(Exception):

    """An error parsing the validation manifest."""
