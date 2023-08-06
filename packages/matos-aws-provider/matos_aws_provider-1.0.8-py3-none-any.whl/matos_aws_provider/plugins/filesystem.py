# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsFilesystem(BaseProvider):
    """Aws file system plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cloudtrail service
        """

        self.filesystem = resource
        self.filesystem_details = {}
        super().__init__(**kwargs, client_type="efs")

    def get_inventory(self) -> Any:
        """Get inventory"""

        resources = self.conn.describe_file_systems()
        files = resources["FileSystems"]

        filesystem_resources = []
        for file in files:
            filesystem_resources.append(
                {
                    "type": "filesystem",
                    **file,
                }
            )
        return filesystem_resources

    def get_resources(self) -> Any:
        """Get resources"""

        backup_policy = {}

        try:
            response = self.conn.describe_backup_policy(
                FileSystemId=self.filesystem["FileSystemId"]
            )
            backup_policy = response["BackupPolicy"]
        except Exception as ex:
            # PolicyNotFound
            logger.error(f"Policy not found {ex}")

        self.filesystem_details = {
            **self.filesystem,
            "BackupPolicy": backup_policy,
            "AccessPoints": self.get_access_points(self.filesystem["FileSystemId"]),
        }
        return self.filesystem_details

    def get_access_points(self, file_system_id):
        """
        Get access point corresponding to the file system id.
        Parameters:
        -file_system_id: Id of the file system
        """
        resp = self.conn.describe_access_points(FileSystemId=file_system_id)
        return resp.get("AccessPoints", [])


def register() -> None:
    "Register plugin"
    factory.register("filesystem", AwsFilesystem)
