# -*- coding: utf-8 -*-
"""Anything you need for lord of the rings chapters
"""

from dataclasses import dataclass
import logging
from typing import List, Optional

import theoneapisdk._utils as utils
from theoneapisdk.exceptions import ChapterNotFound, QuoteNotFound

_logger: logging.Logger = logging.getLogger(__name__)
MISSING_CHAPTER_ID_MESSAGE = "Chapter id can't be empty"
MISSING_CHAPTER_NAME_MESSAGE = "Chapter dialog can't be empty"
CHAPTER_NOT_FOUND_MESSAGE = "Timeout exception, probably because Chapter id doesn't exist"

@dataclass
class Chapter:
    """Chapter from one of the lord of the ringss book
    """
    _id: str
    name: str
    book: Optional[str]
    
def get_chapters() -> List[Chapter]:
    """Returns list of Lord of the rings chapters

    Returns:
        List[Chapter]: list of chapters
    """
    response = utils._get_request_w_auth("chapter")
    _logger.debug(f"get_chapters -> response: {response}")
    return [
        Chapter(
            _id=ch.get("_id"),
            name=ch.get("name"),
            book=ch.get("book")
        )
        for ch in response.docs
    ]


def get_chapter(name: str) -> Chapter:
    """Get one Lord of the rings chapters by name

    Args:
        name (str): lords of the ring chapter name

    Raises:
        ChapterNotFound - The chapter name was not found in the lord of the rings books
        ValueError - Chapter name can't be empty or None

    Returns:
        Chapter: _description_

    """
    if not name:
        raise ValueError(MISSING_CHAPTER_NAME_MESSAGE)
    _logger.debug(f"get chapter with name: {name}")
    chapters = get_chapters()
    for ch in chapters:
        if ch.name.lower() == name.lower():
            return ch
    raise ChapterNotFound(f"the chaptacer name {name} was not found")


def get_chapter_by_id(id: str) -> Chapter:
    """Find chapter by id

    Args:
        id (str): Chapter Id

    Raises:
        ChapterNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        Chapter: The lord of the ring
    """
    _logger.debug(f"get chapter by id: {id}")
    if not id:
        raise ValueError(MISSING_CHAPTER_ID_MESSAGE)
    response = utils._get_request_w_auth(f"chapter/{id}")
    if response.success:
        return [Chapter(
            _id=ch.get("_id"),
            name=ch.get("name"),
            book=ch.get("book")
        ) for ch in response.docs][0]
    raise ChapterNotFound(response.message)