# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetDBProxyEndpointResult',
    'AwaitableGetDBProxyEndpointResult',
    'get_db_proxy_endpoint',
    'get_db_proxy_endpoint_output',
]

@pulumi.output_type
class GetDBProxyEndpointResult:
    def __init__(__self__, d_b_proxy_endpoint_arn=None, endpoint=None, is_default=None, tags=None, vpc_id=None, vpc_security_group_ids=None):
        if d_b_proxy_endpoint_arn and not isinstance(d_b_proxy_endpoint_arn, str):
            raise TypeError("Expected argument 'd_b_proxy_endpoint_arn' to be a str")
        pulumi.set(__self__, "d_b_proxy_endpoint_arn", d_b_proxy_endpoint_arn)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if is_default and not isinstance(is_default, bool):
            raise TypeError("Expected argument 'is_default' to be a bool")
        pulumi.set(__self__, "is_default", is_default)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter(name="dBProxyEndpointArn")
    def d_b_proxy_endpoint_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the DB proxy endpoint.
        """
        return pulumi.get(self, "d_b_proxy_endpoint_arn")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        The endpoint that you can use to connect to the DB proxy. You include the endpoint value in the connection string for a database client application.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> Optional[bool]:
        """
        A value that indicates whether this endpoint is the default endpoint for the associated DB proxy. Default DB proxy endpoints always have read/write capability. Other endpoints that you associate with the DB proxy can be either read/write or read-only.
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.DBProxyEndpointTagFormat']]:
        """
        An optional set of key-value pairs to associate arbitrary data of your choosing with the DB proxy endpoint.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        VPC ID to associate with the new DB proxy endpoint.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Optional[Sequence[str]]:
        """
        VPC security group IDs to associate with the new DB proxy endpoint.
        """
        return pulumi.get(self, "vpc_security_group_ids")


class AwaitableGetDBProxyEndpointResult(GetDBProxyEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDBProxyEndpointResult(
            d_b_proxy_endpoint_arn=self.d_b_proxy_endpoint_arn,
            endpoint=self.endpoint,
            is_default=self.is_default,
            tags=self.tags,
            vpc_id=self.vpc_id,
            vpc_security_group_ids=self.vpc_security_group_ids)


def get_db_proxy_endpoint(d_b_proxy_endpoint_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDBProxyEndpointResult:
    """
    Resource schema for AWS::RDS::DBProxyEndpoint.


    :param str d_b_proxy_endpoint_name: The identifier for the DB proxy endpoint. This name must be unique for all DB proxy endpoints owned by your AWS account in the specified AWS Region.
    """
    __args__ = dict()
    __args__['dBProxyEndpointName'] = d_b_proxy_endpoint_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rds:getDBProxyEndpoint', __args__, opts=opts, typ=GetDBProxyEndpointResult).value

    return AwaitableGetDBProxyEndpointResult(
        d_b_proxy_endpoint_arn=__ret__.d_b_proxy_endpoint_arn,
        endpoint=__ret__.endpoint,
        is_default=__ret__.is_default,
        tags=__ret__.tags,
        vpc_id=__ret__.vpc_id,
        vpc_security_group_ids=__ret__.vpc_security_group_ids)


@_utilities.lift_output_func(get_db_proxy_endpoint)
def get_db_proxy_endpoint_output(d_b_proxy_endpoint_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDBProxyEndpointResult]:
    """
    Resource schema for AWS::RDS::DBProxyEndpoint.


    :param str d_b_proxy_endpoint_name: The identifier for the DB proxy endpoint. This name must be unique for all DB proxy endpoints owned by your AWS account in the specified AWS Region.
    """
    ...
