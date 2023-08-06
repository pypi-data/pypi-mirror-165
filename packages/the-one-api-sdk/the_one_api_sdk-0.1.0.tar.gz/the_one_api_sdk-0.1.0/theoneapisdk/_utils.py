"""
Utils function to help calling the one api endpoint
"""

import json
from typing import List
from urllib.parse import urljoin

import requests

import theoneapisdk as theone
from theoneapisdk.exceptions import MISSING_ACCESS_TOKEN_ERROR

USE_DEFAULT = -1
UNKNOWN_ERROR = "Unknown error"
AUTHORIZATION_HEADER = "Authorization"
MISSING_ACESS_TOKEN_MESSAGE = "Access token is required"

class OneAPIReponse:
    docs: List[any]
    total: int
    limit: int
    offset: int
    page: int
    pages: int
    success: bool = True
    message: str

    @staticmethod
    def from_json(input: str) -> any:
        resp = OneAPIReponse()
        resp_json = json.loads(input)
        if "success" in resp_json:
            resp.success = resp_json["success"]
            resp.message = resp_json.get("message", UNKNOWN_ERROR)
            return resp
        resp.docs = resp_json["docs"]
        resp.limit = resp_json["limit"]
        resp.page = resp_json["page"]
        resp.total = resp_json["total"]
        resp.offset = resp_json["offset"]
        resp.pages = resp_json["pages"]
        return resp


def _get_request(path: str, limit: int = USE_DEFAULT, offset: int = USE_DEFAULT) -> OneAPIReponse:
    """Call the endpoint. Autherization not required"""
    base_url = theone.config.the_one_api_base_endpoint_url
    full_path = urljoin(base_url, path)
    return OneAPIReponse.from_json(requests.get(full_path, timeout=theone.config.request_timeout).text)


def _get_request_w_auth(path: str, limit: int = USE_DEFAULT, offset: int = USE_DEFAULT) -> str:
    """Call the endpoint. Autherization required"""
    access_token = theone.config.access_token
    if not access_token:
        raise MISSING_ACCESS_TOKEN_ERROR(MISSING_ACESS_TOKEN_MESSAGE)
    headers = {AUTHORIZATION_HEADER: f"Bearer {access_token}"}
    base_url = theone.config.the_one_api_base_endpoint_url
    full_path = urljoin(base_url, path)
    return OneAPIReponse.from_json(requests.get(full_path, headers=headers, timeout=theone.config.request_timeout).text)
