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
    'GetInstanceFleetConfigResult',
    'AwaitableGetInstanceFleetConfigResult',
    'get_instance_fleet_config',
    'get_instance_fleet_config_output',
]

@pulumi.output_type
class GetInstanceFleetConfigResult:
    def __init__(__self__, id=None, target_on_demand_capacity=None, target_spot_capacity=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if target_on_demand_capacity and not isinstance(target_on_demand_capacity, int):
            raise TypeError("Expected argument 'target_on_demand_capacity' to be a int")
        pulumi.set(__self__, "target_on_demand_capacity", target_on_demand_capacity)
        if target_spot_capacity and not isinstance(target_spot_capacity, int):
            raise TypeError("Expected argument 'target_spot_capacity' to be a int")
        pulumi.set(__self__, "target_spot_capacity", target_spot_capacity)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="targetOnDemandCapacity")
    def target_on_demand_capacity(self) -> Optional[int]:
        return pulumi.get(self, "target_on_demand_capacity")

    @property
    @pulumi.getter(name="targetSpotCapacity")
    def target_spot_capacity(self) -> Optional[int]:
        return pulumi.get(self, "target_spot_capacity")


class AwaitableGetInstanceFleetConfigResult(GetInstanceFleetConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceFleetConfigResult(
            id=self.id,
            target_on_demand_capacity=self.target_on_demand_capacity,
            target_spot_capacity=self.target_spot_capacity)


def get_instance_fleet_config(id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceFleetConfigResult:
    """
    Resource Type definition for AWS::EMR::InstanceFleetConfig
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:emr:getInstanceFleetConfig', __args__, opts=opts, typ=GetInstanceFleetConfigResult).value

    return AwaitableGetInstanceFleetConfigResult(
        id=__ret__.id,
        target_on_demand_capacity=__ret__.target_on_demand_capacity,
        target_spot_capacity=__ret__.target_spot_capacity)


@_utilities.lift_output_func(get_instance_fleet_config)
def get_instance_fleet_config_output(id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceFleetConfigResult]:
    """
    Resource Type definition for AWS::EMR::InstanceFleetConfig
    """
    ...
