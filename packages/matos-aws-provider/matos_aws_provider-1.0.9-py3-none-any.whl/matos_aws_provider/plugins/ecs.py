# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsECS(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """ """
        try:
            super().__init__(**kwargs, client_type="ecs")
            self.resource = resource if resource else {}
        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """
        Fetches ecs details.
        """
        return [{"type": "ecs"}]

    def get_resources(self) -> Any:
        """
        Fetches ecs details.
        """
        all_services, all_clusters, all_task_definitions = [], [], []
        cluster_arns = self.conn.list_clusters().get("clusterArns", [])
        task_definition_arns = self.conn.list_task_definitions().get(
            "taskDefinitionArns"
        )
        n = 10
        for arn in cluster_arns:
            services = self.conn.list_services(cluster=arn)
            service_arns = services.get("serviceArns", [])
            for i in range(0, len(service_arns), n):
                services = self.conn.describe_services(
                    cluster=arn, services=service_arns[i : i + n]
                ).get("services")
                all_services += services
        for i in range(0, len(cluster_arns), n):

            all_clusters += self.conn.describe_clusters(
                clusters=cluster_arns[i : i + n], include=["SETTINGS"]
            ).get("clusters", [])
        for arn in task_definition_arns:
            task = self.conn.describe_task_definition(taskDefinition=arn).get(
                "taskDefinition"
            )
            all_task_definitions.append(task)
        resource = {
            "clusters": all_clusters,
            "services": all_services,
            "task_definitions": all_task_definitions,
        }

        return resource


def register() -> Any:
    """Register class method

    Returns:
        Any: register class
    """
    factory.register("ecs", AwsECS)
