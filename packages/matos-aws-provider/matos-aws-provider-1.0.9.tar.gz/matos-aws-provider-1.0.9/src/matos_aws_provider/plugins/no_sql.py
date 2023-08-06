# -*- coding: utf-8 -*-
from typing import Dict, Any
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsDynamoDB(BaseProvider):
    """AWS dynamodb plugin"""

    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """Constructor class"""
        super().__init__(**kwargs, client_type="dynamodb")

        try:
            self.application_autoscaling = self.client("application-autoscaling")
            self.ddb = resource

        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """Get inventory assets"""
        response = self.conn.list_tables()
        dynamodbs = [
            {"name": item, "type": "no_sql"} for item in response.get("TableNames", [])
        ]
        return dynamodbs

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        dynamo_db = {
            **self.conn.describe_table(TableName=self.ddb.get("name")).get("Table", {}),
            "TableAutoScalingDescription": self.get_table_replica_auto_scaling(),
            "ContinuousBackupsDescription": self.get_continuous_backups(),
            "ScalableTargets": self.get_autoscaling_scalable_targets(),
            "type": "no_sql",
        }

        return dynamo_db

    def get_table_replica_auto_scaling(self):
        """Get table replica for auto scaling"""
        try:
            resp = self.conn.describe_table_replica_auto_scaling(
                TableName=self.ddb.get("name")
            )
        except Exception as ex:
            logger.error("no sql auto scaling %s", str(ex))
            resp = {}
        return resp.get("TableAutoScalingDescription")

    def get_continuous_backups(self):
        """Get continous backup"""
        try:
            resp = self.conn.describe_continuous_backups(TableName=self.ddb.get("name"))
        except Exception as ex:
            logger.error("no sql continuous backups %s", str(ex))
            resp = {}
        return resp.get("ContinuousBackupsDescription")

    def get_autoscaling_scalable_targets(self):
        """Get autoscaling scalable targets."""
        try:
            resp = self.application_autoscaling.describe_scalable_targets(
                ServiceNamespace="dynamodb",
                ResourceIds=self.get_autoscaling_resources(),
            )
        except Exception as ex:
            logger.error(f" {ex} no sql continuous backups")
            resp = {}
        return resp.get("ScalableTargets", [])

    def get_autoscaling_resources(self):
        """Get autoscaling resources"""
        resources = [f"table/{self.ddb.get('name')}"]
        for index in self.ddb.get("GlobalSecondaryIndexes"):
            resources.append(f"table/{self.ddb.get('name')}/{index['IndexName']}")
        return resources


def register() -> None:
    """Register plugin"""
    factory.register("no_sql", AwsDynamoDB)
