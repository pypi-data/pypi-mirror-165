# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsUserGroup(BaseProvider):
    """AWS user group plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct user group service
        """

        super().__init__(**kwargs, client_type="iam")
        self.user_groups = resource

    def get_inventory(self) -> Any:
        """Get inventory assets"""

        response = self.conn.list_groups()
        Policies = self.conn.list_policies(Scope="Local").get("Policies")
        Policies = [policy.get("Arn") for policy in Policies]
        users = [
            {**item, "UserPoliciesArn": Policies, "type": "user_groups"}
            for item in response.get("Groups", [])
        ]
        return users

    def get_resources(self) -> Any:
        """
        Fetches user groups

        Args:
        return: dictionary object.
        """
        group = {**self.user_groups}
        finalttachedPolicies = []
        try:
            AttachedPolicies = self.conn.list_attached_group_policies(
                GroupName=group.get("GroupName")
            ).get("AttachedPolicies")
            for group_policy in AttachedPolicies:
                if group_policy.get("PolicyArn") in group.get("UserPoliciesArn"):
                    policy_detail = self.conn.get_policy(
                        PolicyArn=group_policy.get("PolicyArn")
                    ).get("Policy")
                    policy_version = self.conn.get_policy_version(
                        PolicyArn=group_policy.get("PolicyArn"),
                        VersionId=policy_detail.get("DefaultVersionId"),
                    ).get("PolicyVersion")
                    finalttachedPolicies.append(
                        {
                            **group_policy,
                            **policy_detail,
                            "PolicyVersion": policy_version,
                        }
                    )
        except Exception as ex:
            logger.error(f"Error {ex}")
            finalttachedPolicies = []
        final_group = group.copy()
        final_group.pop("UserPoliciesArn", [])
        return {**final_group, "AttachedPolicies": finalttachedPolicies}


def register() -> None:
    """Register plugin"""
    factory.register("user_groups", AwsUserGroup)
