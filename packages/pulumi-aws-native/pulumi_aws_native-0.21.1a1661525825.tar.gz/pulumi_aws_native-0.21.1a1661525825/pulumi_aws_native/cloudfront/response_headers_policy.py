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
from ._inputs import *

__all__ = ['ResponseHeadersPolicyArgs', 'ResponseHeadersPolicy']

@pulumi.input_type
class ResponseHeadersPolicyArgs:
    def __init__(__self__, *,
                 response_headers_policy_config: pulumi.Input['ResponseHeadersPolicyConfigArgs']):
        """
        The set of arguments for constructing a ResponseHeadersPolicy resource.
        """
        pulumi.set(__self__, "response_headers_policy_config", response_headers_policy_config)

    @property
    @pulumi.getter(name="responseHeadersPolicyConfig")
    def response_headers_policy_config(self) -> pulumi.Input['ResponseHeadersPolicyConfigArgs']:
        return pulumi.get(self, "response_headers_policy_config")

    @response_headers_policy_config.setter
    def response_headers_policy_config(self, value: pulumi.Input['ResponseHeadersPolicyConfigArgs']):
        pulumi.set(self, "response_headers_policy_config", value)


class ResponseHeadersPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 response_headers_policy_config: Optional[pulumi.Input[pulumi.InputType['ResponseHeadersPolicyConfigArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::CloudFront::ResponseHeadersPolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResponseHeadersPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::CloudFront::ResponseHeadersPolicy

        :param str resource_name: The name of the resource.
        :param ResponseHeadersPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResponseHeadersPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 response_headers_policy_config: Optional[pulumi.Input[pulumi.InputType['ResponseHeadersPolicyConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResponseHeadersPolicyArgs.__new__(ResponseHeadersPolicyArgs)

            if response_headers_policy_config is None and not opts.urn:
                raise TypeError("Missing required property 'response_headers_policy_config'")
            __props__.__dict__["response_headers_policy_config"] = response_headers_policy_config
            __props__.__dict__["last_modified_time"] = None
        super(ResponseHeadersPolicy, __self__).__init__(
            'aws-native:cloudfront:ResponseHeadersPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResponseHeadersPolicy':
        """
        Get an existing ResponseHeadersPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResponseHeadersPolicyArgs.__new__(ResponseHeadersPolicyArgs)

        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["response_headers_policy_config"] = None
        return ResponseHeadersPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter(name="responseHeadersPolicyConfig")
    def response_headers_policy_config(self) -> pulumi.Output['outputs.ResponseHeadersPolicyConfig']:
        return pulumi.get(self, "response_headers_policy_config")

