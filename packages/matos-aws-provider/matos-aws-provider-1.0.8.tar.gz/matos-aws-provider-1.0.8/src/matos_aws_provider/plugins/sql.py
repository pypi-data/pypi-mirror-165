# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsSQL(BaseProvider):
    """AWS sql plugin"""

    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """Constructor method"""
        try:
            super().__init__(**kwargs, client_type="rds")
            self.database = resource

        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        response = self.conn.describe_db_instances()
        return [{**item, "type": "sql"} for item in response.get("DBInstances", [])]

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """

        self.database = {
            **self.database,
            "DBSnapshots": self.get_db_snapshots(
                instance_id=self.database.get("DBInstanceIdentifier")
            ),
            "DBCluster": None,
        }

        if self.database.get("DBClusterIdentifier"):
            db_cluster = self.get_db_cluster(self.database.get("DBClusterIdentifier"))
            if db_cluster:
                self.database["DBCluster"] = db_cluster

        return self.database

    def get_db_snapshots(self, instance_id):
        """Get db snapshots"""
        response = self.conn.describe_db_snapshots(DBInstanceIdentifier=instance_id)
        return response.get("DBSnapshots")

    def get_db_cluster(self, cluster_id):
        """Get db cluster"""

        def get_db_cluster_snapshot(c_id):
            resp = self.conn.describe_db_cluster_snapshots(DBClusterIdentifier=c_id)
            return resp.get("DBClusterSnapshots")

        filters = [{"Name": "db-cluster-id", "Values": [cluster_id]}]
        response = self.conn.describe_db_clusters(Filters=filters)

        clusters = response.get("DBClusters", [])

        clusters = [
            {
                **cluster,
                "Snapshots": get_db_cluster_snapshot(
                    c_id=cluster.get("DBClusterIdentifier")
                ),
            }
            for cluster in clusters
        ]

        return clusters[0] if clusters else None


def register() -> None:
    """Register plugin"""
    factory.register("sql", AwsSQL)
