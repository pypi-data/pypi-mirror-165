# -*- coding: utf-8 -*-
# pylint: disable=C1802, R0912
import json
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsEMR(BaseProvider):
    def __init__(
        self,
        resource: Dict,
        **kwargs,
    ) -> None:
        """
        Construct security hub service
        """
        super().__init__(**kwargs, client_type="emr")
        self.resource = resource if resource else {}
        try:
            self.ec2 = self.client("ec2")
        except Exception as ex:
            logging.error(ex)

    def get_inventory(self) -> Any:
        """
        Fetches resource details.
        """
        return [{"type": "emr"}]

    def get_resources(self) -> Any:
        """
        Fetches EMR cluster details.
        """
        resource = {**self.resource}
        resource["Clusters"] = self.get_clusters()
        for cluster in resource["Clusters"]:
            if cluster["Id"] != "j-1RTHLIJGR6I7C":
                continue
            cluster.update(
                **self.conn.describe_cluster(ClusterId=cluster["Id"]).get("Cluster", {})
            )
            security_groups = []
            ec2_instance_attr = cluster["Ec2InstanceAttributes"]
            emr_master_sg = ec2_instance_attr.get("EmrManagedMasterSecurityGroup")
            if emr_master_sg:
                security_groups.append(emr_master_sg)
            emr_slave_sg = ec2_instance_attr.get("EmrManagedSlaveSecurityGroup")
            if emr_slave_sg:
                security_groups.append(emr_slave_sg)
            addition_master_sgs = ec2_instance_attr.get(
                "AdditionalMasterSecurityGroups", []
            )
            for sg in addition_master_sgs:
                security_groups.append(sg)
            addition_slave_sgs = ec2_instance_attr.get(
                "AdditionalSlaveSecurityGroups", []
            )
            for sg in addition_slave_sgs:
                security_groups.append(sg)
            if len(security_groups):
                sg_dict = self.describe_security_groups(security_groups)
                if emr_master_sg:
                    ec2_instance_attr["EmrManagedMasterSecurityGroupDetails"] = sg_dict[
                        emr_master_sg
                    ]
                if emr_slave_sg:
                    ec2_instance_attr["EmrManagedSlaveSecurityGroupDetails"] = sg_dict[
                        emr_slave_sg
                    ]
                for sg in addition_master_sgs:
                    if "AdditionalMasterSecurityGroupsDetails" not in ec2_instance_attr:
                        ec2_instance_attr["AdditionalMasterSecurityGroupsDetails"] = []
                    ec2_instance_attr["AdditionalMasterSecurityGroupsDetails"].append(
                        sg_dict[sg]
                    )
                for sg in addition_slave_sgs:
                    if "AdditionalSlaveSecurityGroupsDetails" not in ec2_instance_attr:
                        ec2_instance_attr["AdditionalSlaveSecurityGroupsDetails"] = []
                    ec2_instance_attr["AdditionalSlaveSecurityGroupsDetails"].append(
                        sg_dict[sg]
                    )
                if cluster.get("SecurityConfiguration"):
                    cluster[
                        "SecurityConfigurationDetails"
                    ] = self.get_security_configuration(
                        cluster.get("SecurityConfiguration")
                    )

            if cluster.get("InstanceCollectionType") == "INSTANCE_GROUP":
                cluster["GroupInstances"] = self.get_instance_groups(cluster["Id"])
                cluster["MasterInstances"] = self.list_group_instances(
                    cluster["Id"], ["MASTER"]
                )
            else:
                cluster["FleetInstances"] = self.get_instance_fleets(cluster["Id"])
                cluster["MasterInstances"] = self.list_fleet_instances(
                    cluster["Id"], "MASTER"
                )
        resource[
            "BlockPublicAccessConfiguration"
        ] = self.get_block_public_access_configuration()
        return resource

    def get_clusters(self):
        """Gem cluster method"""
        clusters = []

        def list_clusters(clusters, marker=None):
            if marker:
                response = self.conn.list_clusters(Marker=marker)
            else:
                response = self.conn.list_clusters()
            clusters += response.get("Clusters", [])
            if "Marker" in response:
                list_clusters(clusters, response["Marker"])

        list_clusters(clusters)
        return clusters

    def describe_security_groups(self, sgs):
        """describe secuirty groups method"""
        resp = self.ec2.describe_security_groups(GroupIds=sgs)
        sg_dict = {}
        for sg in resp.get("SecurityGroups"):
            sg_dict[sg["GroupId"]] = sg
        return sg_dict

    def get_block_public_access_configuration(self):
        """Get block public access config"""
        return self.conn.get_block_public_access_configuration()

    def get_security_configuration(self, security_configuration):
        """Get block public access config"""
        resp = self.conn.describe_security_configuration(Name=security_configuration)
        configuration = json.loads(resp["SecurityConfiguration"])
        return configuration

    def get_instance_groups(self, cluster_id):
        """Get instance groups"""
        return self.conn.list_instance_groups(ClusterId=cluster_id).get(
            "InstanceGroups", []
        )

    def get_instance_fleets(self, cluster_id):
        """Get instance fleets"""
        return self.conn.list_instance_fleets(ClusterId=cluster_id).get(
            "InstanceFleets", []
        )

    def list_group_instances(self, cluster_id, instance_group_types):
        """List group instances"""
        return self.conn.list_instances(
            ClusterId=cluster_id, InstanceGroupTypes=instance_group_types
        ).get("Instances", [])

    def list_fleet_instances(self, cluster_id, instance_fleet_type):
        """List fleet instances"""
        return self.conn.list_instances(
            ClusterId=cluster_id, InstanceFleetType=instance_fleet_type
        ).get("Instances", [])


def register() -> Any:
    """Register plugin"""
    factory.register("emr", AwsEMR)
