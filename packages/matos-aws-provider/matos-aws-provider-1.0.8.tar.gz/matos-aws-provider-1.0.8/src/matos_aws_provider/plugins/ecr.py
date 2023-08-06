# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict
import botocore
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


logger = logging.getLogger(__name__)


class AwsECR(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """ """
        try:
            super().__init__(**kwargs, client_type="ecr")
            self.resource = resource if resource else {}
            self.ecr_public = self.client("ecr-public")
        except Exception as ex:
            logger.error(ex)

    def get_inventory(self) -> Any:
        """
        Fetches ecs details.
        """
        return [{"type": "ecr"}]

    def get_resources(self) -> Any:
        """
        Fetches ecr details.
        """
        private_repos = self.get_repositories()
        resource = {}
        resource["repositories"] = [
            {**private_repo, "repo_type": "private"} for private_repo in private_repos
        ]
        priv_registry = self.get_registry_details()
        for repo in resource["repositories"]:
            repo["registry"] = priv_registry
            policy = self.get_lifecylce_policy(
                repo["registryId"], repo["repositoryName"]
            )
            if policy:
                repo["LifecyclePolicy"] = policy
        pub_repos = self.get_public_repositories()
        pub_repos = [{**pub_repos, "repo_type": "public"} for pub_repos in pub_repos]
        pub_registries = self.get_public_registries()
        for repo in pub_repos:
            repo["registry"] = self.find_registry_details(
                pub_registries, repo["registryId"]
            )
        resource["repositories"] += pub_repos
        return resource

    def get_repositories(self):
        """
        Get private ECR repositories
        """
        return self.conn.describe_repositories().get("repositories", [])

    def get_registry_details(self):
        """
        Get private ECR repository details
        """
        reg = self.conn.describe_registry()
        if "ResponseMetadata" in reg:
            del reg["ResponseMetadata"]
        scan_config = self.conn.get_registry_scanning_configuration()
        if "ResponseMetadata" in reg:
            del scan_config["ResponseMetadata"]
        reg["scanningConfiguration"] = scan_config["scanningConfiguration"]
        return reg

    def get_lifecylce_policy(self, registry_id, repository_name):
        """
        Get lifecylce policy of an ECR repository
        """
        try:
            return self.conn.get_lifecycle_policy(
                registryId=registry_id, repositoryName=repository_name
            )
        except Exception as error:
            logger.error(f"Boto3 client error {error}")
        return None

    def get_public_repositories(self):
        """
        Get ECR public repositories
        """
        try:
            return self.ecr_public.describe_repositories().get("repositories", [])
        except botocore.exceptions.EndpointConnectionError as error:
            logger.error(f"Boto3 client error {error}")
        return []

    def get_public_registries(self):
        """
        Get ECR public registries
        """
        try:
            return self.ecr_public.describe_registries().get("registries", [])
        except botocore.exceptions.EndpointConnectionError as error:
            logger.error(f"Boto3 client error {error}")
        return []

    def find_registry_details(self, registries, registry_id):
        """
        Find ECR registry details
        """
        for registry in registries:
            if registry["registryId"] == registry_id:
                return registry
        return {}


def register() -> Any:
    """Register class method

    Returns:
        Any: register class
    """
    factory.register("ecr", AwsECR)
