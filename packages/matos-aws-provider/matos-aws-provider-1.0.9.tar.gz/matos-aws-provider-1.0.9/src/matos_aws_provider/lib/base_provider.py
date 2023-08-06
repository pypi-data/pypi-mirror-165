# -*- coding: utf-8 -*-
import logging
from typing import Any
from matos_aws_provider.lib.auth import Connection

logger = logging.getLogger(__name__)


class BaseProvider(Connection):
    """Base plugins provider

    Args:
        Connection (_type_): _description_
    """

    def __init__(self, **kwargs) -> None:
        """Class Constructor method"""
        try:

            super().__init__(**kwargs)
            self._client_type = kwargs.pop("client_type")
            if self._client_type:
                self._conn = self.client(service_name=self._client_type)
        except Exception as ex:
            logging.error(ex)

    @property
    def conn(self) -> Any:
        """Connection property"""
        if not self._conn:
            return None
        return self._conn

    @property
    def client_type(self) -> str:
        """Client type property

        Returns:
            str: client type
        """
        return self._client_type

    def get_inventory(self) -> Any:
        """Get inventory method

        Raises:
            NotImplementedError: Not implement exeception

        Returns:
            Any: cloud asset inventory
        """
        raise NotImplementedError

    def get_resources(self) -> Any:
        """_summary_

        Raises:
            NotImplementedError: _description_

        Returns:
            Any: _description_
        """
        raise NotImplementedError
