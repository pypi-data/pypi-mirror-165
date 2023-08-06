# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsEip(BaseProvider):
    "Aws eip plugin class"

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """
        self.eip = resource
        super().__init__(**kwargs, client_type="ec2")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        response = self.conn.describe_addresses()
        return [{**item, "type": "eip"} for item in response.get("Addresses", [])]

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        eip = {
            **self.eip,
        }
        return eip


def register() -> Any:
    """Register plugin"""
    factory.register("eip", AwsEip)
