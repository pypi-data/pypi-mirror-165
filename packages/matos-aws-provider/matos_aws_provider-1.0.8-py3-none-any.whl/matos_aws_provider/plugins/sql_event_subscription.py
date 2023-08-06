# -*- coding: utf-8 -*-
from typing import Any
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsSQLEventSubscription(BaseProvider):
    """AWS sql plugin"""

    def __init__(
        self,
        resource: Any,
        **kwargs,
    ) -> None:
        """Constructor method"""
        try:
            super().__init__(**kwargs, client_type="rds")
            self.sts = self.client("sts")
            self.resource = resource

        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        response = self.conn.describe_event_subscriptions()
        subscriptions = [
            {**item, "type": "sql_event_subscription"}
            for item in response.get("EventSubscriptionsList", [])
        ]
        return subscriptions

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        return: dictionary object.
        """
        aws_account_id = self.sts.get_caller_identity()["Account"]
        if isinstance(self.resource, dict):
            self.resource["aws_account_id"] = aws_account_id
        elif isinstance(self.resource, list):
            for item in self.resource:
                item["aws_account_id"] = aws_account_id
        return self.resource


def register() -> None:
    """Register plugin"""
    factory.register("sql_event_subscription", AwsSQLEventSubscription)
