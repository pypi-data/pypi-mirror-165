# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsRestApi(BaseProvider):
    """AWS rest api plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct api gateway service
        """

        super().__init__(**kwargs, client_type="apigateway")
        self.resource = resource

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        response = self.conn.get_rest_apis()
        return [{**item, "type": "rest_api"} for item in response.get("items", [])]

    def get_resources(self) -> Any:
        """
        Fetches rest api gateways details.
        """
        finalStages = []

        stages = self.conn.get_stages(restApiId=self.resource.get("id")).get("item")
        resources = self.conn.get_resources(
            restApiId=self.resource.get("id"), embed=["methods"]
        ).get("items")
        try:
            for stage in stages:
                if stage.get("clientCertificateId"):
                    certificate_details = self.conn.get_client_certificate(
                        clientCertificateId=stage.get("clientCertificateId")
                    )
                    finalStages.append(
                        {
                            **stage,
                            "CertificateExpirationDate": certificate_details.get(
                                "expirationDate"
                            ),
                        }
                    )
                else:
                    finalStages.append(
                        {
                            **stage,
                        }
                    )
        except Exception as ex:
            logger.error("Error %s", ex)
            finalStages = []

        resource = {
            **self.resource,
            "stages": finalStages,
            "resources": resources,
            "region": self.region,
        }

        return resource


def register() -> Any:
    """Register plugin"""
    factory.register("rest_api", AwsRestApi)
