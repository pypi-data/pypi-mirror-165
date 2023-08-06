# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
import botocore
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsDax(BaseProvider):
    """Aws dax plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """

        super().__init__(**kwargs, client_type="dax")
        self.dax = resource

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        try:
            response = self.conn.describe_clusters()
            resources = response.get("Clusters", {})
        except botocore.exceptions.ClientError as e:
            logger.error(f"Error getting cluster {e}")
            return []
        return [{**resource, "type": "dax"} for resource in resources]

    def get_resources(self) -> Any:
        """
        Fetches dax details.
        """

        dax = {**self.dax}

        return dax


def register() -> Any:
    """Register plugin"""
    factory.register("dax", AwsDax)
