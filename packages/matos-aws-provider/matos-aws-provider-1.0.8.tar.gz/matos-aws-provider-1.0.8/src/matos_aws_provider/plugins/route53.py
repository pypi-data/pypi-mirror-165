# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsRoute53(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """
        Constructor method
        """
        super().__init__(**kwargs, client_type="route53")
        self.resource = resource if resource else {}

    def get_inventory(self):
        """Get service inventory resource"""
        response = self.conn.list_hosted_zones()
        return [{**item, "type": "route53"} for item in response.get("HostedZones", [])]

    def get_resources(self):
        """
        Fetches resource details.
        """
        query_logging_configs = self.conn.list_query_logging_configs(
            HostedZoneId=self.resource.get("Id")
        ).get("QueryLoggingConfigs")
        resource = {**self.resource, "QueryLoggingConfig": query_logging_configs}
        return resource


def register() -> Any:
    """Register plugin"""
    factory.register("route53", AwsRoute53)
