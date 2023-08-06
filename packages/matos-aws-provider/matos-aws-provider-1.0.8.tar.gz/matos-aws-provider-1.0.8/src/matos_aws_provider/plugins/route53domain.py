# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsRoute53Domain(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """
        Constructor method
        """
        super().__init__(**kwargs, client_type="route53domains")
        self.resource = resource if resource else {}

    def get_inventory(self):
        """Get service inventory resource"""
        response = self.conn.list_domains()
        return [
            {**item, "type": "route53domains"} for item in response.get("Domains", [])
        ]

    def get_resources(self):
        """
        Fetches resource details.
        """
        details = self.conn.get_domain_detail(
            DomainName=self.resource.get("DomainName")
        )
        resource = {**self.resource, **details}

        return resource


def register() -> Any:
    """Register plugin"""
    factory.register("route53domains", AwsRoute53Domain)
