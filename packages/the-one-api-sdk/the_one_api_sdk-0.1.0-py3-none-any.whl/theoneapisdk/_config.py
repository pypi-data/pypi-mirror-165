# -*- coding: utf-8 -*-
"""Configuration file for the_one_api_sdk.
The configuration can be loaded form env vars, or set directly into the config object

Example:
    $ import theoneapisdk as theone
    $ theone.config.access_token = TEST_ACCESS_TOKEN
    
"""

import logging
import os
from typing import Any, Dict, NamedTuple, Optional, Type, Union, cast

from theoneapisdk import exceptions

_logger: logging.Logger = logging.getLogger(__name__)

ENV_PREFIX = "ONEAPI_SDK_"
DEFAULT_LIMIT = 100
DEFAULT_BASE_ENDPOINT = "https://the-one-api.dev/v2/"
DEFAULT_TIMEOUT = 5  # seconds

_ConfigValueType = Union[str, bool, int, None]


class _ConfigArg(NamedTuple):
    dtype: Type[Union[str, bool, int]]
    nullable: bool
    default: _ConfigValueType


# Please, also add any new argument as a property in the _Config class
_CONFIG_ARGS: Dict[str, _ConfigArg] = {
    "access_token": _ConfigArg(dtype=str, nullable=True, default=None),
    "default_limit": _ConfigArg(dtype=int, nullable=True, default=DEFAULT_LIMIT),
    "request_timeout": _ConfigArg(dtype=int, nullable=True, default=DEFAULT_TIMEOUT),
    # Endpoints URLs
    "the_one_api_base_endpoint_url": _ConfigArg(dtype=str, nullable=True, default=DEFAULT_BASE_ENDPOINT),
}


class _Config:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """the one api sdk's Configuration class."""

    def __init__(self) -> None:
        self._loaded_values: Dict[str, _ConfigValueType] = {}
        name: str
        self.access_token = None
        self.default_limit = None
        self.the_one_api_base_endpoint_url = None
        self.request_timeout = None
        for name in _CONFIG_ARGS:
            self._load_config(name=name)

    def reset(self, item: Optional[str] = None) -> None:
        """Reset one or all (if None is received) configuration values.

        Args:
            item (Optional[str], optional): Configuration item name.. Defaults to None.

        Examples:
            $ import theoneapisdk as onesdk
            $ onesdk.config.reset("access_token")  # Reset one specific configuration
            $ onesdk.config.reset()  # Reset all
        """
        if item is None:
            for name in _CONFIG_ARGS:
                self._reset_item(item=name)
        else:
            self._reset_item(item=item)

    def _load_config(self, name: str) -> bool:
        env_var: Optional[str] = os.getenv(f"{ENV_PREFIX}{name.upper()}")
        if env_var is not None:
            self._set_config_value(key=name, value=env_var)
            return True
        elif name in _CONFIG_ARGS and _CONFIG_ARGS[name].default:
            self._set_config_value(key=name, value=_CONFIG_ARGS[name].default)
            return True
        return False

    def _set_config_value(self, key: str, value: Any) -> None:
        if key not in _CONFIG_ARGS:
            raise exceptions.InvalidArgumentValue(
                f"{key} is not a valid configuration. Please use: {list(_CONFIG_ARGS.keys())}"
            )
        value_casted: _ConfigValueType = self._apply_type(
            name=key, value=value, dtype=_CONFIG_ARGS[key].dtype, nullable=_CONFIG_ARGS[key].nullable
        )
        self._loaded_values[key] = value_casted

    def __getitem__(self, item: str) -> _ConfigValueType:
        if item not in self._loaded_values:
            raise AttributeError(f"{item} not configured yet.")
        return self._loaded_values[item]

    def _reset_item(self, item: str) -> None:
        if item in self._loaded_values:
            if item.endswith("_endpoint_url"):
                self._loaded_values[item] = None
            else:
                del self._loaded_values[item]
        self._load_config(name=item)

    @staticmethod
    def _apply_type(name: str, value: Any, dtype: Type[Union[str, bool, int]], nullable: bool) -> _ConfigValueType:
        if _Config._is_null(value=value):
            if nullable is True:
                return None
            raise exceptions.InvalidArgumentValue(
                f"{name} configuration does not accept a null value. Please pass {dtype}."
            )
        try:
            return dtype(value) if isinstance(value, dtype) is False else value
        except ValueError as ex:
            raise exceptions.InvalidConfiguration(f"Config {name} must receive a {dtype} value.") from ex

    @staticmethod
    def _is_null(value: _ConfigValueType) -> bool:
        if value is None:
            return True
        if isinstance(value, str) is True:
            value = cast(str, value)
            if value.lower() in ("none", "null", "nil"):
                return True
        return False

    @property
    def access_token(self) -> Optional[str]:
        """Property access_token."""
        return cast(Optional[str], self["access_token"])

    @access_token.setter
    def access_token(self, value: Optional[str]) -> None:
        self._set_config_value(key="access_token", value=value)

    @property
    def default_limit(self) -> Optional[int]:
        """Property default_limit."""
        return cast(Optional[int], self["default_limit"])

    @default_limit.setter
    def default_limit(self, value: Optional[int]) -> None:
        self._set_config_value(key="default_limit", value=value)

    @property
    def request_timeout(self) -> Optional[int]:
        """Property default_limit."""
        return cast(Optional[int], self["request_timeout"])

    @request_timeout.setter
    def request_timeout(self, value: Optional[int]) -> None:
        self._set_config_value(key="request_timeout", value=value)

    @property
    def the_one_api_base_endpoint_url(self) -> Optional[str]:
        """Property the_one_api_base_endpoint_url."""
        return cast(Optional[str], self["the_one_api_base_endpoint_url"])

    @the_one_api_base_endpoint_url.setter
    def the_one_api_base_endpoint_url(self, value: Optional[str]) -> None:
        self._set_config_value(key="the_one_api_base_endpoint_url", value=value)


config: _Config = _Config()
