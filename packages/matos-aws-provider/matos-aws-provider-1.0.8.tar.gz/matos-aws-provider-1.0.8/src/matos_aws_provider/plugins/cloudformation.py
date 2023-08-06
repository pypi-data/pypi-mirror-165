# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsCloudFormation(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """
        Constructor method
        """
        super().__init__(**kwargs, client_type="cloudformation")
        self.resource = resource if resource else {}

    def get_inventory(self):
        """Get service inventory resource"""
        response = self.conn.describe_stacks()

        return [
            {**item, "type": "cloudformation"} for item in response.get("Stacks", [])
        ]

    def get_resources(self):
        """
        Fetches CloudFormation details.
        """

        stack_policy_body = self.conn.get_stack_policy(
            StackName=self.resource.get("StackName")
        ).get("StackPolicyBody")
        stacks = self.conn.describe_stacks(
            StackName=self.resource.get("StackName")
        ).get("Stacks")
        return {**self.resource, "StackPolicyBody": stack_policy_body, "Stacks": stacks}


def register() -> Any:
    """Register plugin"""
    factory.register("cloudformation", AwsCloudFormation)
