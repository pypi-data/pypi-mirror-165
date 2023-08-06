# -*- coding: utf-8 -*-
"""Anything you need for lord of the rings characters

This moudle requires access_token to https://the-one-api.dev/.
Make sure you register first and have it ready
"""
import logging
from dataclasses import dataclass, field
from typing import List, Optional

from requests.exceptions import ReadTimeout

import theoneapisdk._utils as utils
from theoneapisdk.exceptions import CharacterNotFound, CharacterNotInitialized
from theoneapisdk.quotes import Quote

_logger: logging.Logger = logging.getLogger(__name__)

MISSING_CHARACTER_ID_MESSAGE = "character id can't be empty"
MISSING_CHARACTER_NAME_MESSAGE = "character name can't be empty"
CHARACTER_NOT_FOUND_MESSAGE = "Timeout exception, probably because character id doesn't exist"


@dataclass
class Character:
    _id: Optional[str]
    height: Optional[str]
    race: Optional[str]
    gender: Optional[str]
    birth: Optional[str]
    spouse: Optional[str]
    death: Optional[str]
    realm: Optional[str]
    hair: Optional[str]
    name: Optional[str]
    wiki_url: Optional[str]
    _quotes: Optional[List[Quote]] = field(default_factory=list)

    @property
    def quotes(self) -> List[Quote]:
        """Get all the quotes by character

        Raises:
            CharacterNotInitialized: Character ID is missing

        Returns:
            List[Quote]: List of quotes
        """
        if not self._id:
            raise CharacterNotInitialized(MISSING_CHARACTER_ID_MESSAGE)
        if not self._quotes:
            self._quotes = get_character_quotes_by_character_id(self._id)
        return self._quotes

def get_characters() -> List[Character]:
    """Returns list of Lord of the rings Characters

    Returns:
        List[Character]: list of characters
    """
    response = utils._get_request_w_auth("character")
    _logger.debug(f"get_characters -> response: {response}")
    return [
        Character(
            _id=character.get("_id"),
            name=character.get("name"),
            height=character.get("height"),
            race=character.get("race"),
            gender=character.get("gender"),
            birth=character.get("birth"),
            spouse=character.get("spouse"),
            death=character.get("death"),
            realm=character.get("realm"),
            hair=character.get("hair"),
            wiki_url=character.get("wikiUrl")
        )
        for character in response.docs
    ]


def get_character(name: str) -> Character:
    """Get one Lord of the rings character

    Args:
        name (str): lords of the ring character

    Raises:
        CharacterNotFound - The character name was not found in the lord of the rings characters

    Returns:
        Character: _description_

    """
    _logger.debug(f"get character with name: {name}")
    characters = get_characters()
    for character in characters:
        if character.name.lower() == name.lower():
            return character
    raise CharacterNotFound(f"the character {name} was not found")

def get_character_quotes(name: str) -> List[Quote]:
    """Get all the quotes of a lord of the ring character

    Args:
        name (str): the lord of the rings character

    Raises:
        CharacterNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        List[Quote]: _description_
    """
    _logger.debug(f"get character quotes by name: {name}")
    if not name:
        raise ValueError(MISSING_CHARACTER_NAME_MESSAGE)
    characters = get_characters()
    for character in characters:
        if character.name.lower() == name.lower():
            response = utils._get_request_w_auth(f"character/{character._id}/quote")
            return [Quote(
                _id=quote["_id"],
                dialog=quote.get("dialog"),
                movie=quote.get("movie"),
                character=quote.get("character")
            ) for quote in response.docs]
    raise CharacterNotFound(f"the character {name} was not found")

def get_character_by_id(id: str) -> Character:
    """Find character by id

    Args:
        id (str): Character Id

    Raises:
        CharacterNotFound - If the id not found
        ValueError - id is required and can't be empty or None

    Returns:
        Character: The lord of the ring
    """
    _logger.debug(f"get character by id: {id}")
    if not id:
        raise ValueError(MISSING_CHARACTER_ID_MESSAGE)
    response = utils._get_request_w_auth(f"character/{id}")
    if response.success:
        return [Character(
            _id=character.get("_id"),
            name=character.get("name"),
            height=character.get("height"),
            race=character.get("race"),
            gender=character.get("gender"),
            birth=character.get("birth"),
            spouse=character.get("spouse"),
            death=character.get("death"),
            realm=character.get("realm"),
            hair=character.get("hair"),
            wiki_url=character.get("wikiUrl")
        ) for character in response.docs][0]
    raise CharacterNotFound(response.message)

def get_character_quotes_by_character_id(id: str) -> List[Quote]:
    """Get all the quotes of a lord of the ring character

    Args:
        id (str): the lord of the rings character id

    Raises:
        CharacterNotFound - The character name was not found in the lord of the rings characters
        ValueError - Character name is required and can't be empty or None

    Returns:
        List[Quote]: _description_
    """
    if not id:
        raise ValueError(MISSING_CHARACTER_ID_MESSAGE)
    try:
        response = utils._get_request_w_auth(f"character/{id}/quote")
        if response.success:
            return [Quote(
                _id=quote.get("_id"),
                dialog=quote.get("dialog"),
                movie=quote.get("movie"),
                character=quote.get("character")
            ) for quote in response.docs]
        raise CharacterNotFound(response.message)
    except ReadTimeout as timeout_ex:
        _logger.exception(timeout_ex)
        raise CharacterNotFound(CHARACTER_NOT_FOUND_MESSAGE)
