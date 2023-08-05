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
from ._enums import *

__all__ = [
    'InstanceAccessControlAttributeConfigurationAccessControlAttribute',
    'InstanceAccessControlAttributeConfigurationAccessControlAttributeValue',
    'InstanceAccessControlAttributeConfigurationProperties',
    'PermissionSetCustomerManagedPolicyReference',
    'PermissionSetPermissionsBoundary',
    'PermissionSetTag',
]

@pulumi.output_type
class InstanceAccessControlAttributeConfigurationAccessControlAttribute(dict):
    def __init__(__self__, *,
                 key: str,
                 value: 'outputs.InstanceAccessControlAttributeConfigurationAccessControlAttributeValue'):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> 'outputs.InstanceAccessControlAttributeConfigurationAccessControlAttributeValue':
        return pulumi.get(self, "value")


@pulumi.output_type
class InstanceAccessControlAttributeConfigurationAccessControlAttributeValue(dict):
    def __init__(__self__, *,
                 source: Sequence[str]):
        pulumi.set(__self__, "source", source)

    @property
    @pulumi.getter
    def source(self) -> Sequence[str]:
        return pulumi.get(self, "source")


@pulumi.output_type
class InstanceAccessControlAttributeConfigurationProperties(dict):
    """
    The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes. We recomend that you use  AccessControlAttributes property instead.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessControlAttributes":
            suggest = "access_control_attributes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceAccessControlAttributeConfigurationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceAccessControlAttributeConfigurationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceAccessControlAttributeConfigurationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_control_attributes: Sequence['outputs.InstanceAccessControlAttributeConfigurationAccessControlAttribute']):
        """
        The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes. We recomend that you use  AccessControlAttributes property instead.
        """
        pulumi.set(__self__, "access_control_attributes", access_control_attributes)

    @property
    @pulumi.getter(name="accessControlAttributes")
    def access_control_attributes(self) -> Sequence['outputs.InstanceAccessControlAttributeConfigurationAccessControlAttribute']:
        return pulumi.get(self, "access_control_attributes")


@pulumi.output_type
class PermissionSetCustomerManagedPolicyReference(dict):
    def __init__(__self__, *,
                 name: str,
                 path: Optional[str] = None):
        pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        return pulumi.get(self, "path")


@pulumi.output_type
class PermissionSetPermissionsBoundary(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customerManagedPolicyReference":
            suggest = "customer_managed_policy_reference"
        elif key == "managedPolicyArn":
            suggest = "managed_policy_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PermissionSetPermissionsBoundary. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PermissionSetPermissionsBoundary.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PermissionSetPermissionsBoundary.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 customer_managed_policy_reference: Optional['outputs.PermissionSetCustomerManagedPolicyReference'] = None,
                 managed_policy_arn: Optional[str] = None):
        if customer_managed_policy_reference is not None:
            pulumi.set(__self__, "customer_managed_policy_reference", customer_managed_policy_reference)
        if managed_policy_arn is not None:
            pulumi.set(__self__, "managed_policy_arn", managed_policy_arn)

    @property
    @pulumi.getter(name="customerManagedPolicyReference")
    def customer_managed_policy_reference(self) -> Optional['outputs.PermissionSetCustomerManagedPolicyReference']:
        return pulumi.get(self, "customer_managed_policy_reference")

    @property
    @pulumi.getter(name="managedPolicyArn")
    def managed_policy_arn(self) -> Optional[str]:
        return pulumi.get(self, "managed_policy_arn")


@pulumi.output_type
class PermissionSetTag(dict):
    """
    The metadata that you apply to the permission set to help you categorize and organize them.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        The metadata that you apply to the permission set to help you categorize and organize them.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


