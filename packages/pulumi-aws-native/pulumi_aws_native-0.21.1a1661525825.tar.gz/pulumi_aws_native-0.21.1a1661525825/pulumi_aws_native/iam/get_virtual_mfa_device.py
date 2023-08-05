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
    'GetVirtualMFADeviceResult',
    'AwaitableGetVirtualMFADeviceResult',
    'get_virtual_mfa_device',
    'get_virtual_mfa_device_output',
]

@pulumi.output_type
class GetVirtualMFADeviceResult:
    def __init__(__self__, serial_number=None, tags=None, users=None):
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[str]:
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.VirtualMFADeviceTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "users")


class AwaitableGetVirtualMFADeviceResult(GetVirtualMFADeviceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMFADeviceResult(
            serial_number=self.serial_number,
            tags=self.tags,
            users=self.users)


def get_virtual_mfa_device(serial_number: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMFADeviceResult:
    """
    Resource Type definition for AWS::IAM::VirtualMFADevice
    """
    __args__ = dict()
    __args__['serialNumber'] = serial_number
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iam:getVirtualMFADevice', __args__, opts=opts, typ=GetVirtualMFADeviceResult).value

    return AwaitableGetVirtualMFADeviceResult(
        serial_number=__ret__.serial_number,
        tags=__ret__.tags,
        users=__ret__.users)


@_utilities.lift_output_func(get_virtual_mfa_device)
def get_virtual_mfa_device_output(serial_number: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualMFADeviceResult]:
    """
    Resource Type definition for AWS::IAM::VirtualMFADevice
    """
    ...
