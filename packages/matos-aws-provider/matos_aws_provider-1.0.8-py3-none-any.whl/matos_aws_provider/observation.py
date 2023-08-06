# -*- coding: utf-8 -*-
# pylint: disable-all
import json
import string
import random
from datetime import datetime
from datetime import timedelta

from matos_aws_provider.lib.auth import Connection
from matos_aws_provider.config import AWSConfig
from matos_aws_provider.lib.utils import Joiners


class AWSObservation(Connection):

    METRIC_CONFIG = None

    def __init__(self, **kwargs) -> None:
        """"""

        super().__init__(**kwargs)
        self.cw_client = self.client("cloudwatch")

        self._metric_map = None

    @property
    def cw_config(self):
        """
        fetch configs of metrics from cloudwatch
        """

        if self.METRIC_CONFIG is not None:
            return self.METRIC_CONFIG

        self.METRIC_CONFIG = self.get_metric_details()

        return self.METRIC_CONFIG

    @property
    def metric_map(self):
        """
        load local json file which contain mapping of
        cloudmatos_metric name to cloud provider metric name
        i.e. node.cpu.utilization -> GCP/AWS specific configuration
        """

        if self._metric_map is not None:
            return self._metric_map

        self._metric_map = self.read_metrics_file()

        return self._metric_map

    def build_dimensions(
        self,
        filters: dict,
    ) -> list:
        """
        AWS filters given in metrics are called dimensions,
        which are created as a list of dicts here.
        """

        return [{"Name": k, "Value": v} for k, v in filters.items()]

    def get_metric_details(self):
        """
        extracts usable fileds from cloudmatos metrics details data
        """

        resp_metrics = self.cw_client.list_metrics()
        metrics = resp_metrics["Metrics"]

        details = {}

        for metric in metrics:
            namespace, metric_name = metric["Namespace"], metric["MetricName"]
            namespace_details = details.get(namespace, {})
            metric_details = namespace_details.get(metric_name, {})
            metric_details.update({x["Name"]: x["Value"] for x in metric["Dimensions"]})
            namespace_details[metric_name] = metric_details
            details[namespace] = namespace_details

        return details

    def read_metrics_file(
        self,
        filename: str = "common/assets/metrics.json",
    ) -> dict:
        """
        read local config file.
        """

        with open(filename, "r") as f:
            data = json.load(f)

        metric_map = {}

        for cloudmatos_metric, source_info in data.items():

            if "aws" not in source_info["providers"]:
                continue

            aws_metric = source_info["providers"]["aws"]
            metric_map[cloudmatos_metric] = aws_metric

        return metric_map

    def get_time_interval(self, t: int) -> tuple:
        """
        create start and end time object
        """

        end = datetime.utcnow()
        start = end - timedelta(seconds=t)

        return start, end

    def convert_filter_names(
        self,
        filters: dict,
    ) -> dict:
        """
        convert cloudmatos generic filter names to aws specific names
        """

        return {AWSConfig.filter_name_map.get(k, k): v for k, v in filters.items()}

    def extract_values(self, metric_data: dict) -> dict:
        """
        take compact data whats going to be used only, from metrics data
        """

        return {
            "values": metric_data["Values"],
            "label": metric_data["Label"],
            "id": metric_data["Id"],
        }

    def parse_values(
        self,
        metric_with_filters,
        metrics_data,
        id_to_metric,
        align=True,
        aligner="mean",
    ):
        """
        Parsed the values from a time series, and return either list of values
        or a single value, depending on if align is True.
        """

        metric_map_inverted = {  # noqa
            (v["namespace"], v["metric"]): k for k, v in self.metric_map.items()
        }

        metric_name_to_data = {}

        for metric in metrics_data:

            metric_data = self.extract_values(metric)

            id = metric_data["id"]
            name = metric_data["label"]
            values = metric_data["values"]

            cloudmatos_metric = id_to_metric.get(id)
            retdict = {
                "metric": cloudmatos_metric or id,
                "name": name,
            }

            if align and values:
                aligner_method = getattr(Joiners, aligner)
                retdict.update(value=aligner_method(values))
            else:
                retdict.update(values=values)

            filters = metric_with_filters.get(cloudmatos_metric, {})
            retdict.update(filters)
            data = metric_name_to_data.get(cloudmatos_metric, [])
            data.append(retdict)
            metric_name_to_data[cloudmatos_metric] = data

        return metric_name_to_data

    def build_metric_query(
        self,
        namespace,
        metric,
        dimensions=[],
        stat="Average",
        resource_update_period=60,
    ):
        """
        creates the metric query that is used in self.get_metric_data
        AWS can take multiple queries at once, so it's possible to build many
        queires and fetch all at once using self.get_metric_data
        """

        def generate_id(length):
            chars = string.ascii_uppercase + string.ascii_lowercase
            rest = "".join(random.choice(chars) for _ in range(length - 1))
            first = random.choice(string.ascii_lowercase)
            return first + rest

        return {
            "Id": generate_id(24),
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric,
                    "Dimensions": dimensions,
                },
                "Period": resource_update_period,
                "Stat": stat,
            },
            "ReturnData": True,
        }

    def get_metric_data(
        self,
        metric_queries,
        time_period=60,
    ) -> dict:
        """
        takes metric_queries build by self.build_metric_query and
        calls cloudwatch API for that.
        """

        start_t, end_t = self.get_time_interval(time_period)

        response = self.cw_client.get_metric_data(
            MetricDataQueries=metric_queries,
            StartTime=start_t,
            EndTime=end_t,
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("cloudwatch request failed")

        return response["MetricDataResults"]

    def parse_cloudmatos_metric(
        self,
        cloudmatos_metric,
        filters,
    ):
        """
        parses metrics from cloudwatch into cloudmatos generic type
        """

        if cloudmatos_metric not in self.metric_map:
            raise Exception("Undefined metric")

        metric_details = self.metric_map[cloudmatos_metric]
        namespace, metric = metric_details["namespace"], metric_details["metric"]

        if namespace not in self.cw_config:
            raise Exception(f"Given namespace [{namespace}] not in cloudwatch")
        if metric not in self.cw_config[namespace]:
            raise Exception(
                f"Given metric [{metric}]" f"not in namespace [{namespace}]"
            )

        dimensions = []

        if filters:
            filters = self.convert_filter_names(filters)
            dimensions = self.build_dimensions(filters)

        return {
            "namespace": namespace,
            "metric": metric,
            "dimensions": dimensions,
            "resource_update_period": metric_details.get("resource_update_period", 60),
        }

    def get_metrics_observation(
        self,
        metric_with_filters,
        time_period=300,
    ):
        """
        takes a list of metric with filters i.e.
        { "instance" : {"instance_id" : "some_id" }}
        and fetched metrics for that.
        """

        metric_queries = []

        id_to_metric = {}

        for cloudmatos_metric, filters in metric_with_filters.items():

            parsed_metric_details = self.parse_cloudmatos_metric(
                cloudmatos_metric, filters
            )

            query = self.build_metric_query(**parsed_metric_details)
            id_to_metric[query["Id"]] = cloudmatos_metric
            metric_queries.append(query)

        response = self.get_metric_data(metric_queries, time_period)

        retval = self.parse_values(
            metric_with_filters=metric_with_filters,
            metrics_data=response,
            id_to_metric=id_to_metric,
        )

        return retval
