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
from ._inputs import *

__all__ = ['ResourceCollectionArgs', 'ResourceCollection']

@pulumi.input_type
class ResourceCollectionArgs:
    def __init__(__self__, *,
                 resource_collection_filter: pulumi.Input['ResourceCollectionFilterArgs']):
        """
        The set of arguments for constructing a ResourceCollection resource.
        """
        pulumi.set(__self__, "resource_collection_filter", resource_collection_filter)

    @property
    @pulumi.getter(name="resourceCollectionFilter")
    def resource_collection_filter(self) -> pulumi.Input['ResourceCollectionFilterArgs']:
        return pulumi.get(self, "resource_collection_filter")

    @resource_collection_filter.setter
    def resource_collection_filter(self, value: pulumi.Input['ResourceCollectionFilterArgs']):
        pulumi.set(self, "resource_collection_filter", value)


class ResourceCollection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 resource_collection_filter: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionFilterArgs']]] = None,
                 __props__=None):
        """
        This resource schema represents the ResourceCollection resource in the Amazon DevOps Guru.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceCollectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource schema represents the ResourceCollection resource in the Amazon DevOps Guru.

        :param str resource_name: The name of the resource.
        :param ResourceCollectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceCollectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 resource_collection_filter: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionFilterArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceCollectionArgs.__new__(ResourceCollectionArgs)

            if resource_collection_filter is None and not opts.urn:
                raise TypeError("Missing required property 'resource_collection_filter'")
            __props__.__dict__["resource_collection_filter"] = resource_collection_filter
            __props__.__dict__["resource_collection_type"] = None
        super(ResourceCollection, __self__).__init__(
            'aws-native:devopsguru:ResourceCollection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceCollection':
        """
        Get an existing ResourceCollection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceCollectionArgs.__new__(ResourceCollectionArgs)

        __props__.__dict__["resource_collection_filter"] = None
        __props__.__dict__["resource_collection_type"] = None
        return ResourceCollection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="resourceCollectionFilter")
    def resource_collection_filter(self) -> pulumi.Output['outputs.ResourceCollectionFilter']:
        return pulumi.get(self, "resource_collection_filter")

    @property
    @pulumi.getter(name="resourceCollectionType")
    def resource_collection_type(self) -> pulumi.Output['ResourceCollectionType']:
        """
        The type of ResourceCollection
        """
        return pulumi.get(self, "resource_collection_type")

