# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    def __init__(__self__, arn=None, availability_zones=None, cluster_discovery_endpoint=None, cluster_discovery_endpoint_url=None, description=None, id=None, notification_topic_arn=None, parameter_group_name=None, preferred_maintenance_window=None, replication_factor=None, security_group_ids=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if availability_zones and not isinstance(availability_zones, list):
            raise TypeError("Expected argument 'availability_zones' to be a list")
        pulumi.set(__self__, "availability_zones", availability_zones)
        if cluster_discovery_endpoint and not isinstance(cluster_discovery_endpoint, str):
            raise TypeError("Expected argument 'cluster_discovery_endpoint' to be a str")
        pulumi.set(__self__, "cluster_discovery_endpoint", cluster_discovery_endpoint)
        if cluster_discovery_endpoint_url and not isinstance(cluster_discovery_endpoint_url, str):
            raise TypeError("Expected argument 'cluster_discovery_endpoint_url' to be a str")
        pulumi.set(__self__, "cluster_discovery_endpoint_url", cluster_discovery_endpoint_url)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if notification_topic_arn and not isinstance(notification_topic_arn, str):
            raise TypeError("Expected argument 'notification_topic_arn' to be a str")
        pulumi.set(__self__, "notification_topic_arn", notification_topic_arn)
        if parameter_group_name and not isinstance(parameter_group_name, str):
            raise TypeError("Expected argument 'parameter_group_name' to be a str")
        pulumi.set(__self__, "parameter_group_name", parameter_group_name)
        if preferred_maintenance_window and not isinstance(preferred_maintenance_window, str):
            raise TypeError("Expected argument 'preferred_maintenance_window' to be a str")
        pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if replication_factor and not isinstance(replication_factor, int):
            raise TypeError("Expected argument 'replication_factor' to be a int")
        pulumi.set(__self__, "replication_factor", replication_factor)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="clusterDiscoveryEndpoint")
    def cluster_discovery_endpoint(self) -> Optional[str]:
        return pulumi.get(self, "cluster_discovery_endpoint")

    @property
    @pulumi.getter(name="clusterDiscoveryEndpointURL")
    def cluster_discovery_endpoint_url(self) -> Optional[str]:
        return pulumi.get(self, "cluster_discovery_endpoint_url")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="notificationTopicARN")
    def notification_topic_arn(self) -> Optional[str]:
        return pulumi.get(self, "notification_topic_arn")

    @property
    @pulumi.getter(name="parameterGroupName")
    def parameter_group_name(self) -> Optional[str]:
        return pulumi.get(self, "parameter_group_name")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> Optional[str]:
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="replicationFactor")
    def replication_factor(self) -> Optional[int]:
        return pulumi.get(self, "replication_factor")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            arn=self.arn,
            availability_zones=self.availability_zones,
            cluster_discovery_endpoint=self.cluster_discovery_endpoint,
            cluster_discovery_endpoint_url=self.cluster_discovery_endpoint_url,
            description=self.description,
            id=self.id,
            notification_topic_arn=self.notification_topic_arn,
            parameter_group_name=self.parameter_group_name,
            preferred_maintenance_window=self.preferred_maintenance_window,
            replication_factor=self.replication_factor,
            security_group_ids=self.security_group_ids,
            tags=self.tags)


def get_cluster(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Resource Type definition for AWS::DAX::Cluster
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:dax:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        arn=__ret__.arn,
        availability_zones=__ret__.availability_zones,
        cluster_discovery_endpoint=__ret__.cluster_discovery_endpoint,
        cluster_discovery_endpoint_url=__ret__.cluster_discovery_endpoint_url,
        description=__ret__.description,
        id=__ret__.id,
        notification_topic_arn=__ret__.notification_topic_arn,
        parameter_group_name=__ret__.parameter_group_name,
        preferred_maintenance_window=__ret__.preferred_maintenance_window,
        replication_factor=__ret__.replication_factor,
        security_group_ids=__ret__.security_group_ids,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_cluster)
def get_cluster_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Resource Type definition for AWS::DAX::Cluster
    """
    ...
