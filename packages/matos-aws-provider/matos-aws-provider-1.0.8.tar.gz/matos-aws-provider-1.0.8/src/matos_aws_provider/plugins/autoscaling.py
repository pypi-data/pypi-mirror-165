# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsAutoscaling(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """
        Construct auto scalling resource
        """
        super().__init__(**kwargs, client_type="autoscaling")
        self.resource = resource if resource else {}
        try:
            self.ec2 = self.client("ec2")
        except Exception as ex:
            logging.error(ex)

    def get_inventory(self) -> Any:
        """
        Fetches resource details.
        """
        response = self.conn.describe_auto_scaling_groups()
        return [
            {**item, "type": "autoscaling"}
            for item in response.get("AutoScalingGroups", [])
        ]

    def get_resources(self) -> Any:
        """
        Fetches ASG details.
        """
        resource = {**self.resource}
        for instance in resource.get("Instances", []):
            instance["InstanceDetails"] = self.describe_instance(
                instance_id=instance["InstanceId"]
            )
        if resource.get("LaunchConfigurationName"):
            resource["LaunchConfigurationDetails"] = self.describe_launch_configuration(
                resource.get("LaunchConfigurationName")
            )
        if resource.get("LaunchTemplate", {}).get("LaunchTemplateId"):
            resource["LaunchTemplateDetails"] = self.describe_launch_template_version(
                resource.get("LaunchTemplate", {}).get("LaunchTemplateId"),
                resource.get("LaunchTemplate", {}).get("Version"),
            )
        return resource

    def describe_instance(self, instance_id):
        """describe instance method"""
        resp = self.ec2.describe_instances(InstanceIds=[instance_id])
        reservations = resp.get("Reservations", [])
        if len(reservations) and len(reservations[0].get("Instances", [])):
            return reservations[0]["Instances"][0]
        return {}

    def describe_launch_configuration(self, launch_configuration):
        """describe launch configuration"""
        resp = self.conn.describe_launch_configurations(
            LaunchConfigurationNames=[launch_configuration]
        )
        launch_configurations = resp.get("LaunchConfigurations", [])
        if len(launch_configurations):
            return launch_configurations[0]
        return {}

    def describe_launch_template_version(self, launch_template_id, version):
        """describe launch template version"""
        resp = self.ec2.describe_launch_template_versions(
            LaunchTemplateId=launch_template_id, Versions=[version]
        )
        if len(resp.get("LaunchTemplateVersions", [])):
            return resp.get("LaunchTemplateVersions")[0]
        return {}


def register() -> Any:
    """Register plugin"""
    factory.register("autoscaling", AwsAutoscaling)
