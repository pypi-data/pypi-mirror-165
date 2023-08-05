# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SmsTemplateArgs', 'SmsTemplate']

@pulumi.input_type
class SmsTemplateArgs:
    def __init__(__self__, *,
                 body: pulumi.Input[str],
                 template_name: pulumi.Input[str],
                 default_substitutions: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 template_description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SmsTemplate resource.
        """
        pulumi.set(__self__, "body", body)
        pulumi.set(__self__, "template_name", template_name)
        if default_substitutions is not None:
            pulumi.set(__self__, "default_substitutions", default_substitutions)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_description is not None:
            pulumi.set(__self__, "template_description", template_description)

    @property
    @pulumi.getter
    def body(self) -> pulumi.Input[str]:
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: pulumi.Input[str]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "template_name")

    @template_name.setter
    def template_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "template_name", value)

    @property
    @pulumi.getter(name="defaultSubstitutions")
    def default_substitutions(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "default_substitutions")

    @default_substitutions.setter
    def default_substitutions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_substitutions", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateDescription")
    def template_description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "template_description")

    @template_description.setter
    def template_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_description", value)


warnings.warn("""SmsTemplate is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class SmsTemplate(pulumi.CustomResource):
    warnings.warn("""SmsTemplate is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 default_substitutions: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 template_description: Optional[pulumi.Input[str]] = None,
                 template_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Pinpoint::SmsTemplate

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SmsTemplateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Pinpoint::SmsTemplate

        :param str resource_name: The name of the resource.
        :param SmsTemplateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SmsTemplateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 default_substitutions: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 template_description: Optional[pulumi.Input[str]] = None,
                 template_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""SmsTemplate is deprecated: SmsTemplate is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SmsTemplateArgs.__new__(SmsTemplateArgs)

            if body is None and not opts.urn:
                raise TypeError("Missing required property 'body'")
            __props__.__dict__["body"] = body
            __props__.__dict__["default_substitutions"] = default_substitutions
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template_description"] = template_description
            if template_name is None and not opts.urn:
                raise TypeError("Missing required property 'template_name'")
            __props__.__dict__["template_name"] = template_name
            __props__.__dict__["arn"] = None
        super(SmsTemplate, __self__).__init__(
            'aws-native:pinpoint:SmsTemplate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SmsTemplate':
        """
        Get an existing SmsTemplate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SmsTemplateArgs.__new__(SmsTemplateArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["body"] = None
        __props__.__dict__["default_substitutions"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["template_description"] = None
        __props__.__dict__["template_name"] = None
        return SmsTemplate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def body(self) -> pulumi.Output[str]:
        return pulumi.get(self, "body")

    @property
    @pulumi.getter(name="defaultSubstitutions")
    def default_substitutions(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "default_substitutions")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateDescription")
    def template_description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "template_description")

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "template_name")

