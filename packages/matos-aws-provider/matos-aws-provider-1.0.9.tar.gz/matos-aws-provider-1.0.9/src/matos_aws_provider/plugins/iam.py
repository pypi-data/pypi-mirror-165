# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsIAM(BaseProvider):
    """AWS base account plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """

        super().__init__(**kwargs, client_type="iam")
        self.user = resource

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        response = self.conn.list_users()
        return [
            {**item, "type": "serviceAccount"} for item in response.get("Users", [])
        ]

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        pwd_enable_content = self.get_credential_report(self.user["UserName"])
        pwd_enable = pwd_enable_content[0] if pwd_enable_content else None

        users = self.conn.get_account_authorization_details().get("UserDetailList")
        users = [
            user for user in users if user.get("UserName") == self.user["UserName"]
        ]
        user = users[-1]
        custom_policy_list = self.conn.list_policies(Scope="Local").get("Policies")
        policy_details = []
        for policy in user.get("AttachedManagedPolicies", []):
            scope = (
                "Local"
                if [
                    p
                    for p in custom_policy_list
                    if p.get("Arn") == policy.get("PolicyArn")
                ]
                else "AWS"
            )
            policy_detail = self.conn.get_policy(PolicyArn=policy.get("PolicyArn")).get(
                "Policy"
            )
            policy_version = self.conn.get_policy_version(
                PolicyArn=policy.get("PolicyArn"),
                VersionId=policy_detail.get("DefaultVersionId"),
            ).get("PolicyVersion")
            policy_details.append(
                {**policy_detail, "PolicyVersion": policy_version, "Scope": scope}
            )

        access_keys = self.get_access_keys(self.user.get("UserName"))
        user_data = {
            **user,
            "PasswordEnable": pwd_enable,
            "AttachedManagedPolicies": policy_details,
            "GroupList": self.get_group_list(user.get("UserName")),
            "MFADevices": self.get_mfa_devices(user.get("UserName")),
            "PasswordLastUsed": self.get_password_last_used(user.get("UserName")),
        }

        if access_keys:
            user_data["AccessKeys"] = access_keys

        return user_data

    def get_access_keys(self, user_name):
        """Get access keys"""
        access_keys = None
        try:
            access_keys = self.conn.list_access_keys(UserName=user_name).get(
                "AccessKeyMetadata", []
            )
            access_keys = [
                {
                    **key,
                    "AccessKeyLastUsed": self.conn.get_access_key_last_used(
                        AccessKeyId=key.get("AccessKeyId")
                    )
                    .get("AccessKeyLastUsed", {})
                    .get("LastUsedDate"),
                }
                for key in access_keys
            ]
        except Exception as ex:
            logger.error("fetch list access key error %s", ex)

        return access_keys

    def get_credential_report(self, user_name):
        """Get credential report"""
        content = []
        try:
            response = self.conn.get_credential_report()
            origin_content = response.get("Content", "")
            content = [
                False
                if user.split(",")[3] in ["false"]
                else True
                if user.split(",")[3] in ["true"]
                else user.split(",")[3]
                for user in origin_content.decode("UTF-8").split("\n")
                if user.split(",")[0] == user_name
            ]
        except Exception as ex:
            logger.error("credential report %s", ex)

        return content

    def get_group_list(self, user_name):
        """Get group list"""
        try:
            groups = self.conn.list_groups_for_user(UserName=user_name).get("Groups")
        except Exception as ex:
            print("Error get list group %s", ex)
            groups = []
        group_list = []
        for group in groups:
            try:
                group_policies = self.conn.list_attached_group_policies(
                    GroupName=group.get("GroupName")
                ).get("AttachedPolicies")
            except Exception as ex:
                logger.error("Error get attach group %s", ex)
                group_policies = []
            group_list.append({**group, "AttachedPolicies": group_policies})

        return group_list

    def get_mfa_devices(self, user_name):
        """Get MFA devices"""
        try:
            mfa_devices = self.conn.list_mfa_devices(UserName=user_name).get(
                "MFADevices", []
            )
        except Exception as ex:
            logger.error("Error get list mfa devices %s", ex)
            mfa_devices = []

        return mfa_devices

    def get_password_last_used(self, user_name):
        """Get password last used"""
        return (
            self.conn.get_user(UserName=user_name).get("User").get("PasswordLastUsed")
        )


def register() -> Any:
    """Register plugin"""
    factory.register("serviceAccount", AwsIAM)
