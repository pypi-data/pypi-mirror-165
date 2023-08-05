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
    'GetTransitGatewayMulticastDomainAssociationResult',
    'AwaitableGetTransitGatewayMulticastDomainAssociationResult',
    'get_transit_gateway_multicast_domain_association',
    'get_transit_gateway_multicast_domain_association_output',
]

@pulumi.output_type
class GetTransitGatewayMulticastDomainAssociationResult:
    def __init__(__self__, resource_id=None, resource_type=None, state=None):
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The type of resource, for example a VPC attachment.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the subnet association.
        """
        return pulumi.get(self, "state")


class AwaitableGetTransitGatewayMulticastDomainAssociationResult(GetTransitGatewayMulticastDomainAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayMulticastDomainAssociationResult(
            resource_id=self.resource_id,
            resource_type=self.resource_type,
            state=self.state)


def get_transit_gateway_multicast_domain_association(subnet_id: Optional[str] = None,
                                                     transit_gateway_attachment_id: Optional[str] = None,
                                                     transit_gateway_multicast_domain_id: Optional[str] = None,
                                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayMulticastDomainAssociationResult:
    """
    The AWS::EC2::TransitGatewayMulticastDomainAssociation type


    :param str subnet_id: The IDs of the subnets to associate with the transit gateway multicast domain.
    :param str transit_gateway_attachment_id: The ID of the transit gateway attachment.
    :param str transit_gateway_multicast_domain_id: The ID of the transit gateway multicast domain.
    """
    __args__ = dict()
    __args__['subnetId'] = subnet_id
    __args__['transitGatewayAttachmentId'] = transit_gateway_attachment_id
    __args__['transitGatewayMulticastDomainId'] = transit_gateway_multicast_domain_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getTransitGatewayMulticastDomainAssociation', __args__, opts=opts, typ=GetTransitGatewayMulticastDomainAssociationResult).value

    return AwaitableGetTransitGatewayMulticastDomainAssociationResult(
        resource_id=__ret__.resource_id,
        resource_type=__ret__.resource_type,
        state=__ret__.state)


@_utilities.lift_output_func(get_transit_gateway_multicast_domain_association)
def get_transit_gateway_multicast_domain_association_output(subnet_id: Optional[pulumi.Input[str]] = None,
                                                            transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
                                                            transit_gateway_multicast_domain_id: Optional[pulumi.Input[str]] = None,
                                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayMulticastDomainAssociationResult]:
    """
    The AWS::EC2::TransitGatewayMulticastDomainAssociation type


    :param str subnet_id: The IDs of the subnets to associate with the transit gateway multicast domain.
    :param str transit_gateway_attachment_id: The ID of the transit gateway attachment.
    :param str transit_gateway_multicast_domain_id: The ID of the transit gateway multicast domain.
    """
    ...
