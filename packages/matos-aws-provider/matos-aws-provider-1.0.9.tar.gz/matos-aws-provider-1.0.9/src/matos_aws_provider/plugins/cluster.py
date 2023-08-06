# -*- coding: utf-8 -*-
import time
import logging
from datetime import datetime, timedelta
from typing import Any, Dict
from kubernetes import client as kclient
from awscli.customizations.eks.get_token import (
    STSClientFactory,
    TokenGenerator,
    TOKEN_EXPIRATION_MINS,
)
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsCluster(BaseProvider):
    "Aws cluster plugin"

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """
        super().__init__(**kwargs, client_type="eks")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        return [{"type": "cluster"}]

    def get_resources(self) -> Any:
        """
        Fetches cluster details.

        Args:
        cluster_name: name of the eks instance.

        return: dictionary object.
        """
        cluster_details = self.get_cluster_details()
        return cluster_details

    def get_cluster_client(
        self,
        cluster_name,
        cluster_host,
    ):
        """Get cluster client"""
        work_session = self.session._session  # pylint: disable=W0212
        client_factory = STSClientFactory(work_session)

        def get_expiration_time():
            token_expiration = datetime.utcnow() + timedelta(
                minutes=TOKEN_EXPIRATION_MINS
            )
            return token_expiration.strftime("%Y-%m-%dT%H:%M:%SZ")

        def get_token(_cluster_name: str, role_arn: str = None) -> dict:
            sts_client = client_factory.get_sts_client(role_arn=role_arn)
            _token = TokenGenerator(sts_client).get_token(_cluster_name)
            return {
                "kind": "ExecCredential",
                "apiVersion": "client.authentication.k8s.io/v1alpha1",
                "spec": {},
                "status": {
                    "expirationTimestamp": get_expiration_time(),
                    "token": _token,
                },
            }

        token = get_token(cluster_name)["status"]["token"]
        conf = kclient.Configuration()

        conf.host = cluster_host + ":443"
        conf.verify_ssl = False
        conf.api_key = {"authorization": "Bearer " + token}
        k8s_client = kclient.ApiClient(conf)
        k8s_client_v1 = kclient.CoreV1Api(k8s_client)

        return k8s_client_v1

    def get_object_count(
        self,
        object_types,
        time_period=100 * 60,
        filters=None,
    ):
        """Get object count"""

        logs = self.client("logs")

        then = (datetime.utcnow() - timedelta(seconds=time_period)).timestamp()
        now = datetime.utcnow().timestamp()

        log_groups = [
            "/aws/containerinsights/wpcon/performance",
            "/aws/containerinsights/wpcon/host",
            "/aws/containerinsights/wpcon/application",
            "/aws/containerinsights/wpcon/dataplane",
        ]

        map1 = {
            "pod": "kubernetes.pod_name",
            "namespace": "kubernetes.namespace_name",
            "container": "kubernetes.container_name",
            "service": "kubernetes.service_name",
        }

        map2 = {
            "pod": "PodName",
            "namespace": "Namespace",
            "node": "NodeName",
            "cluster": "ClusterName",
        }

        object_names = [(map2.get(o) or map1.get(o) or o) for o in object_types]

        fields = ", ".join(object_names)
        field_query = f"fields {fields}"
        count_query = ", ".join([f"count_distinct({o})" for o in object_names])

        if filters:
            filter_queries = [
                f'filter({map2.get(x) or map1.get(x) or x}="{y}")'
                for x, y in filters.items()
            ]
            filter_string = " | ".join(filter_queries)
            query = f"{field_query} | {filter_string} | {count_query}"
        else:
            query = f"{field_query} | {count_query}"

        query_response = logs.start_query(
            startTime=int(then),
            endTime=int(now),
            queryString=query,
            logGroupNames=log_groups,
        )

        while True:
            query_result = logs.get_query_results(queryId=query_response["queryId"])
            if query_result["status"] == "Running":
                time.sleep(1)
                continue

            break

        rev = {x: y for y, x in map1.items()}
        rev.update({x: y for y, x in map2.items()})

        retdict = {}

        for res in query_result["results"][0]:
            o = res["field"][15:][:-1]
            o = rev.get(o) or o
            v = int(res["value"])
            retdict[o] = v

        return retdict

    def add_cluster_objects_from_k8s(
        self,
        cluster_details,
    ):
        """Add cluster objects from k8s"""

        name = cluster_details["name"]
        endpoint = cluster_details["endpoint"]
        k8s_client = self.get_cluster_client(name, endpoint)

        function_map = {
            "pod": k8s_client.list_pod_for_all_namespaces,
            "namespace": k8s_client.list_namespace,
            "node": k8s_client.list_node,
            "service": k8s_client.list_service_for_all_namespaces,
        }

        object_map = {}

        def append_objects(object_type, objects, cluster_name):

            for obj in objects.items:
                object_list = object_map.get(object_type, [])
                object_name = obj.metadata.name
                object_namespace = getattr(obj.metadata, "namespace", None)
                object_uid = getattr(obj.metadata, "uid", None)
                object_self_link = getattr(obj.metadata, "self_link", None)
                object_node_name = getattr(obj.spec, "node_name", None)
                if object_type == "pod":
                    object_container = [
                        {"name": c.name, "image_pull_policy": c.image_pull_policy}
                        for c in obj.spec.containers
                    ]
                else:
                    object_container = None

                object_details = {"name": object_name, "cluster_name": cluster_name}

                if object_namespace:
                    object_details.update(namespace=object_namespace)

                if object_self_link:
                    object_details.update(self_link=object_self_link)

                if object_self_link:
                    object_details.update(uid=object_uid)

                if object_node_name:
                    object_details.update(node=object_node_name)

                if object_container:
                    object_details.update(container=object_container)

                if object_type == "node":
                    try:
                        instance_id = obj.spec.provider_id.split("/")[-1]
                        object_details.update(instance_id=instance_id)
                    except Exception as e:
                        logger.error(e)

                object_list.append(object_details)
                object_map[object_type] = object_list

        for object_type, function in function_map.items():
            try:
                objects = function()
                append_objects(object_type, objects, name)

            except Exception as ex:
                logger.error(ex)

        cluster_details.update(object_map)

    def add_cluster_objects_from_cloudwatch(
        self,
        cluster_details,
    ):
        """Add cluster objects from cloud watch"""

        name = cluster_details["name"]

        object_list = ["pod", "namespace", "node", "container", "service"]

        object_count = self.get_object_count(object_list, filters={"cluster": name})

        for obj, count in object_count.items():
            cluster_details[f"{obj}_count"] = count

        return cluster_details

    def get_cluster_details(self, fetch_objects=True):
        """Get cluster details"""

        def add_objects(cluster_details):
            try:
                self.add_cluster_objects_from_k8s(cluster_details)
            except Exception as cluster_ex:
                logger.error(f"Error add object {cluster_ex}")
                try:
                    self.add_cluster_objects_from_cloudwatch(cluster_details)
                except Exception as cluster_cloud_ex:
                    logger.error(
                        f"Error add cluster objects from cloud watch {cluster_cloud_ex}"
                    )

        clusters = self.conn.list_clusters()
        clusters_details = []

        for name in clusters.get("clusters", []):
            data = self.conn.describe_cluster(name=name)
            cluster = data.get("cluster")
            if cluster and fetch_objects:
                add_objects(cluster)
            cluster["type"] = "cluster"
            clusters_details.append(cluster)

        return clusters_details


def register() -> Any:
    """Register plugins"""
    factory.register("cluster", AwsCluster)
