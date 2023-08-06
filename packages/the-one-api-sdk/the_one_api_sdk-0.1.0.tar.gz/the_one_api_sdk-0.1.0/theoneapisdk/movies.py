# -*- coding: utf-8 -*-
"""Anything you need for lord of the rings movie
This moudle can get the list of movies, a movie by id or name 
and get the quotes in a movie

This moudle requires access_token to https://the-one-api.dev/.
Make sure you register first and have it ready
"""
import logging
from dataclasses import dataclass, field
from doctest import REPORT_CDIFF
from tokenize import Double
from typing import List, Optional

from requests.exceptions import ReadTimeout

import theoneapisdk._utils as utils
from theoneapisdk.characters import Character
from theoneapisdk.exceptions import MovieNotFound, MovieNotInitialized
from theoneapisdk.quotes import Quote

_logger: logging.Logger = logging.getLogger(__name__)
MISSING_MOVIE_ID_MESSAGE = "movie id can't be empty"
MISSING_MOVIE_NAME_MESSAGE = "movie name can't be empty"
MOVIE_NOT_FOUND_MESSAGE = "Timeout exception, probably because movie id doesn't exist"

@dataclass
class Movie:
    """Lord of the rings movie"""

    _id: Optional[str]
    name: Optional[str]
    runtime_in_minutes: Optional[int]
    budget_in_millions: Optional[int]
    box_office_revenue_in_millions: Optional[int]
    academy_award_nominations: Optional[int]
    academ_award_wins: Optional[int]
    rotten_tomatoes_score: Optional[float]
    _quotes: Optional[List[Quote]] = field(default_factory=list)

    @property
    def quotes(self) -> List[Quote]:
        """Get all the quotes in a movie

        Raises:
            MovieNotInitialized: Movie ID is missing

        Returns:
            List[Quote]: List of quotes
        """
        if not self._id:
            raise MovieNotInitialized(MISSING_MOVIE_ID_MESSAGE)
        if not self._quotes:
            self._quotes = get_movie_quotes_by_movie_id(self._id)
        return self._quotes


def get_movies() -> List[Movie]:
    """Returns list of Lord of the rings Movies

    Returns:
        List[Movie]: list of movies
    """
    response = utils._get_request_w_auth("movie")
    _logger.debug(f"get_movies -> response: {response}")
    return [
        Movie(
            _id=movie.get("_id"),
            name=movie.get("name"),
            runtime_in_minutes=movie.get("runtimeInMinutes"),
            budget_in_millions=movie.get("budgetInMillions"),
            box_office_revenue_in_millions=movie.get(
                "boxOfficeRevenueInMillions"),
            academy_award_nominations=movie.get("academyAwardNominations"),
            academ_award_wins=movie.get("academyAwardWins"),
            rotten_tomatoes_score=movie.get("rottenTomatoesScore")
        )
        for movie in response.docs
    ]


def get_movie(name: str) -> Movie:
    """Get one Lord of the rings movie

    Args:
        name (str): lords of the ring movie

    Raises:
        MovieNotFound - The movie name was not found in the lord of the rings movies

    Returns:
        Movie: _description_

    """
    _logger.debug(f"get movie with name: {name}")
    movies = get_movies()
    for movie in movies:
        if movie.name.lower() == name.lower():
            return movie
    raise MovieNotFound(f"the movie {name} was not found")


def get_movie_by_id(id: str) -> Movie:
    """Find movie by id

    Args:
        id (str): Movie Id

    Raises:
        MovieNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        Movie: The lord of the ring
    """
    _logger.debug(f"get movie by id: {id}")
    if not id:
        raise ValueError(MISSING_MOVIE_ID_MESSAGE)
    response = utils._get_request_w_auth(f"movie/{id}")
    if response.success:
        return [Movie(
            _id=movie.get("_id"),
            name=movie.get("name"),
            runtime_in_minutes=movie.get("runtimeInMinutes"),
            budget_in_millions=movie.get("budgetInMillions"),
            box_office_revenue_in_millions=movie.get(
                "boxOfficeRevenueInMillions"),
            academy_award_nominations=movie.get("academyAwardNominations"),
            academ_award_wins=movie.get("academyAwardWins"),
            rotten_tomatoes_score=movie.get("rottenTomatoesScore")
        ) for movie in response.docs][0]
    raise MovieNotFound(response.message)


def get_movie_quotes(name: str) -> List[Quote]:
    """Get all the quotes of a lord of the ring movie

    Args:
        name (str): the lord of the rings movie

    Raises:
        MovieNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        List[Quote]: _description_
    """
    _logger.debug(f"get movie quotes by name: {name}")
    if not name:
        raise ValueError(MISSING_MOVIE_NAME_MESSAGE)
    movies = get_movies()
    for movie in movies:
        if movie.name.lower() == name.lower():
            response = utils._get_request_w_auth(f"movie/{movie._id}/quote")
            return [Quote(
                _id=quote["_id"],
                dialog=quote.get("dialog"),
                movie=quote.get("movie"),
                character=quote.get("character")
            ) for quote in response.docs]
    raise MovieNotFound(f"the movie {name} was not found")


def get_movie_quotes_by_movie_id(id: str) -> List[Quote]:
    """Get all the quotes of a lord of the ring movie

    Args:
        id (str): the lord of the rings movie id

    Raises:
        MovieNotFound - The movie name was not found in the lord of the rings movies
        ValueError - Movie name is required and can't be empty or None

    Returns:
        List[Quote]: _description_
    """
    if not id:
        raise ValueError(MISSING_MOVIE_ID_MESSAGE)
    try:
        response = utils._get_request_w_auth(f"movie/{id}/quote")
        if response.success:
            return [Quote(
                _id=quote.get("_id"),
                dialog=quote.get("dialog"),
                movie=quote.get("movie"),
                character=quote.get("character")
            ) for quote in response.docs]
        raise MovieNotFound(response.message)
    except ReadTimeout as timeout_ex:
        _logger.exception(timeout_ex)
        raise MovieNotFound(MOVIE_NOT_FOUND_MESSAGE)
