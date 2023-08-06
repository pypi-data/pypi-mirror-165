# -*- coding: utf-8 -*-
from typing import Any
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsAccount(BaseProvider):
    """Aws account class

    Args:
        BaseProvider (Class): Base provider class
    """
    def __init__(self, resource, **kwargs) -> None:
        """
        Construct account service
        """

        super().__init__(**kwargs, client_type="account")
        try:
            self.resource = resource
        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        return [{"type": "account"}]

    def get_resources(self):
        """
        Fetches account details.
        """
        resource = {**self.resource}
        try:
            alternate_contact = self.conn.get_alternate_contact(AlternateContactType='SECURITY')
            alternate_contact_information = alternate_contact["AlternateContact"]
            resource['AlternateContact'] = alternate_contact_information
        except Exception as ex:
            logger.error(ex)
        current_contact = self.conn.get_contact_information()
        contact_information = current_contact["ContactInformation"]
        resource['ContactInformation'] = contact_information
        return resource


def register() -> Any:
    """Register plugin"""
    factory.register("account", AwsAccount)
