# -*- coding: utf-8 -*-
"""Anything you need for lord of the rings quotes
"""

from dataclasses import dataclass
import logging
from typing import List

import theoneapisdk._utils as utils
from theoneapisdk.exceptions import QuoteNotFound

_logger: logging.Logger = logging.getLogger(__name__)
MISSING_QUOTE_ID_MESSAGE = "quote id can't be empty"
MISSING_QUOTE_DIALOG_MESSAGE = "quote dialog can't be empty"
QUOTE_NOT_FOUND_MESSAGE = "Timeout exception, probably because quote id doesn't exist"

@dataclass
class Quote:
    """A quote from one of the Lord of the rings movies
    Also holds which character said it
    """
    _id: str
    dialog: str
    movie: str
    character: str
    
def get_quotes() -> List[Quote]:
    """Returns list of Lord of the rings quotes

    Returns:
        List[Quote]: list of quotes
    """
    response = utils._get_request_w_auth("quote")
    _logger.debug(f"get_quotes -> response: {response}")
    return [
        Quote(
            _id=quote.get("_id"),
            dialog=quote.get("dialog"),
            movie=quote.get("movie"),
            character=quote.get("character")
        )
        for quote in response.docs
    ]


def get_quote(dialog: str) -> Quote:
    """Get one Lord of the rings quotes by dialog

    Args:
        dialog (str): lords of the ring quote dialog

    Raises:
        QuoteNotFound - The quote dialog was not found in the lord of the rings quotes
        ValueError - Quote dialog can't be empty or None

    Returns:
        Quote: _description_

    """
    if not dialog:
        raise ValueError(MISSING_QUOTE_DIALOG_MESSAGE)
    _logger.debug(f"get movie with name: {dialog}")
    quotes = get_quotes()
    for quote in quotes:
        if quote.dialog.lower() == dialog.lower():
            return quote
    raise QuoteNotFound(f"the quote dialog {dialog} was not found")


def get_quote_by_id(id: str) -> Quote:
    """Find quote by id

    Args:
        id (str): Quote Id

    Raises:
        QuoteNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        Quote: The lord of the ring
    """
    _logger.debug(f"get quote by id: {id}")
    if not id:
        raise ValueError(MISSING_QUOTE_ID_MESSAGE)
    response = utils._get_request_w_auth(f"quote/{id}")
    if response.success:
        return [Quote(
            _id=quote.get("_id"),
            dialog=quote.get("dialog"),
            movie=quote.get("movie"),
            character=quote.get("character")
        ) for quote in response.docs][0]
    raise QuoteNotFound(response.message)