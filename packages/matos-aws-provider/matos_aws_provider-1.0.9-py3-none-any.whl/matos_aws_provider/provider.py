import threading
from typing import List, Any
import logging
from matos_aws_provider.lib.auth import Connection
from matos_aws_provider.plugins import get_package
from matos_aws_provider.lib import factory, loader

logger = logging.getLogger(__name__)


class Provider(Connection):
    """Aws provider factory class

    Args:
        Connection (Connection): Aws connection class
    """

    def __init__(self, **kwargs) -> None:
        """
        Class constructor method
        """
        super().__init__(**kwargs)
        self.credentials = kwargs.get("credentials", None)
        self.application_id = kwargs.get("application_id", None)
        loader.load_plugins(get_package())
        self.service_factory = factory
        self.resource_type = kwargs.get("resource_type", None)

    def get_assets(self, **kwargs):
        """
        Discover aws resources
        """
        threads = []
        resources = []
        lock = threading.Lock()

        def fetch_discovery_details(rsc_type):
            service_discovery = self.service_factory.create(
                {
                    "type": rsc_type,
                    "credentials": self.credentials,
                    "application_id": self.application_id,
                }
            )
            try:
                result = service_discovery.get_inventory()
                if result is None:
                    return

                with lock:
                    if isinstance(result, list):
                        resources.extend(result)
                    else:
                        resources.append(result)
            except Exception as e:
                logger.error(f"{e}")

        service_map = self.service_factory.fetch_plugins()
        for rsc_type, _ in service_map.items():
            if self.resource_type and self.resource_type != rsc_type:
                continue
            thread = threading.Thread(target=fetch_discovery_details, args=(rsc_type,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return resources

    def get_resource_inventory(self, resource):
        """
        Get resource detail data
        """
        return self._get_assets_inventory(resource)

    def get_resource_inventories(self, resource_list: List[Any]):
        """
        Get resources data
        """
        resource_inventories = {}
        lock = threading.Lock()

        def fetch_resource_details(rsc):
            resource_type = rsc.get("type")
            try:
                detail = self._get_assets_inventory(rsc)
                with lock:
                    resource_inventories[resource_type] = (
                        [detail]
                        if resource_type not in resource_inventories
                        else [*resource_inventories[resource_type], detail]
                    )
            except Exception as e:
                logger.error(f"{e}")

        threads = []
        for resource in resource_list:
            if self.resource_type and self.resource_type != resource.get("type"):
                continue
            thread = threading.Thread(target=fetch_resource_details, args=(resource,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return resource_inventories

    def _get_assets_inventory(self, resource, **kwargs):
        resource.update({"credentials": self.credentials})
        resource.update({"application_id": self.application_id})
        cloud_resource = self.service_factory.create(resource)
        resource_details = cloud_resource.get_resources()
        if resource_details:
            resource.update(details=resource_details)
        resource.pop("credentials")
        resource.pop("application_id")
        return resource
