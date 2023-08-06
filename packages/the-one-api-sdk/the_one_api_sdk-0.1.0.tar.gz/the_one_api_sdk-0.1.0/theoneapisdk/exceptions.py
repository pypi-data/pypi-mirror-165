"""Centralized exceptions Module."""

class MISSING_ACCESS_TOKEN_ERROR(Exception):
    """Missing access token error"""

class BookNotInitialized(Exception):
    """Book Id is missing"""


class BookNotFound(ValueError):
    """Book was not found"""


class MovieNotInitialized(Exception):
    """Movie Id is missing"""


class MovieNotFound(ValueError):
    """Movie was not found"""

class CharacterNotInitialized(Exception):
    """Character Id is missing"""

class CharacterNotFound(ValueError):
    """Character was not found"""    

class ChapterNotFound(ValueError):
    """Chapter was not found"""    

class QuoteNotFound(ValueError):
    """Quote was not found"""   

class InvalidArgumentValue(Exception):
    """Invalid argument value."""


class InvalidArgumentType(Exception):
    """Invalid argument type."""


class InvalidArgumentCombination(Exception):
    """Invalid argument combination."""


class InvalidArgument(Exception):
    """Invalid argument."""


class UnsupportedType(Exception):
    """UnsupportedType exception."""


class UndetectedType(Exception):
    """UndetectedType exception."""


class ServiceApiError(Exception):
    """ServiceApiError exception."""
