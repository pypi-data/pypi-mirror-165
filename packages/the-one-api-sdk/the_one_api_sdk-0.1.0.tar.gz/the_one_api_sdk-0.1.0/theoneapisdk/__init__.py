"""Initial theoneapisdk Module.
Seamlessly integration with the one api.

Usage: 
    TODO
"""


import logging as _logging

import theoneapisdk.books as books
from theoneapisdk.__metadata__ import __description__, __license__, __title__, __version__  # noqa
from theoneapisdk._config import config  # noqa

__all__ = [
    "config",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
    "books",
]

_logging.getLogger("theoneapisdk").addHandler(_logging.NullHandler())
