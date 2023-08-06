# -*- coding: utf-8 -*-
"""Anything you need for lord of the rings book
This moudle can get the list of books, a book by id or name 
and get the chapters in a book
"""
import logging
from dataclasses import dataclass, field
from doctest import REPORT_CDIFF
from typing import List, Optional

from requests.exceptions import ReadTimeout

import theoneapisdk._utils as utils
from theoneapisdk.chapters import Chapter
from theoneapisdk.exceptions import BookNotFound, BookNotInitialized

_logger: logging.Logger = logging.getLogger(__name__)
MISSING_BOOK_ID_MESSAGE = "book id can't be empty"
MISSING_BOOK_NAME_MESSAGE = "book name can't be empty"
BOOK_NOT_FOUND_MESSAGE = "Timeout exception, probably because book id doesn't exist"


@dataclass
class Book:
    """Lord of the rings book"""

    _id: Optional[str]
    name: Optional[str]
    _chapters: Optional[List[Chapter]] = field(default_factory=list)

    @property
    def chapters(self) -> List[Chapter]:
        """Get all the chapters in a book

        Raises:
            BookNotInitialized: Book ID is missing

        Returns:
            List[Chapter]: List of chapters
        """
        if not self._id:
            raise BookNotInitialized(MISSING_BOOK_ID_MESSAGE)
        if not self._chapters:
            self._chapters = get_book_chapters_by_book_id(self._id)
        return self._chapters


def get_books() -> List[Book]:
    """Returns list of Lord of the rings Books

    Returns:
        List[Book]: list of books
    """
    response = utils._get_request("book")
    _logger.debug(f"get_books -> response: {response}")
    return [Book(_id=book["_id"], name=book["name"]) for book in response.docs]


def get_book(name: str) -> Book:
    """Get one Lord of the rings book

    Args:
        name (str): lords of the ring book

    Raises:
        BookNotFound - The book name was not found in the lord of the rings books

    Returns:
        Book: _description_

    """
    _logger.debug(f"get book with name: {name}")
    books = get_books()
    for book in books:
        if book.name.lower() == name.lower():
            return book
    raise BookNotFound(f"the book {name} was not found")


def get_book_by_id(id: str) -> Book:
    """Find book by id

    Args:
        id (str): Book Id

    Raises:
        BookNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        Book: The lord of the ring
    """
    _logger.debug(f"get book by id: {id}")
    if not id:
        raise ValueError(MISSING_BOOK_ID_MESSAGE)
    response = utils._get_request(f"book/{id}")
    if response.success:
        return [Book(_id=book_tmp.get("_id"), name=book_tmp.get("name")) for book_tmp in response.docs][0]
    raise BookNotFound(response.message)


def get_book_chapters(name: str) -> List[Chapter]:
    """Get all the chapters of a lord of the ring book

    Args:
        name (str): the lord of the rings book

    Raises:
        BookNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        List[Chapter]: _description_
    """
    _logger.debug(f"get book chapters by name: {name}")
    if not name:
        raise ValueError(MISSING_BOOK_NAME_MESSAGE)
    books = get_books()
    for book in books:
        if book.name.lower() == name.lower():
            response = utils._get_request(f"book/{book._id}/chapter")
            return [Chapter(_id=chapter["_id"], name=chapter["chapterName"], book=book._id) for chapter in response.docs]
    raise BookNotFound(f"the book {name} was not found")


def get_book_chapters_by_book_id(id: str) -> List[Chapter]:
    """Get all the chapters of a lord of the ring book

    Args:
        id (str): the lord of the rings book id

    Raises:
        BookNotFound - The book name was not found in the lord of the rings books
        ValueError - Book name is required and can't be empty or None

    Returns:
        List[Chapter]: _description_
    """
    if not id:
        raise ValueError(MISSING_BOOK_ID_MESSAGE)
    try:
        response = utils._get_request(f"book/{id}/chapter")
        if response.success:
            return [Chapter(_id=chapter.get("_id"), 
                            name=chapter.get("chapterName"), 
                            book=id) for chapter in response.docs]
        raise BookNotFound(response.message)
    except ReadTimeout as timeout_ex:
        _logger.exception(timeout_ex)
        raise BookNotFound(BOOK_NOT_FOUND_MESSAGE)
