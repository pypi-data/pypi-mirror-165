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

__all__ = ['StageArgs', 'Stage']

@pulumi.input_type
class StageArgs:
    def __init__(__self__, *,
                 rest_api_id: pulumi.Input[str],
                 access_log_setting: Optional[pulumi.Input['StageAccessLogSettingArgs']] = None,
                 cache_cluster_enabled: Optional[pulumi.Input[bool]] = None,
                 cache_cluster_size: Optional[pulumi.Input[str]] = None,
                 canary_setting: Optional[pulumi.Input['StageCanarySettingArgs']] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 documentation_version: Optional[pulumi.Input[str]] = None,
                 method_settings: Optional[pulumi.Input[Sequence[pulumi.Input['StageMethodSettingArgs']]]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['StageTagArgs']]]] = None,
                 tracing_enabled: Optional[pulumi.Input[bool]] = None,
                 variables: Optional[Any] = None):
        """
        The set of arguments for constructing a Stage resource.
        :param pulumi.Input[str] rest_api_id: The ID of the RestApi resource that you're deploying with this stage.
        :param pulumi.Input['StageAccessLogSettingArgs'] access_log_setting: Specifies settings for logging access in this stage.
        :param pulumi.Input[bool] cache_cluster_enabled: Indicates whether cache clustering is enabled for the stage.
        :param pulumi.Input[str] cache_cluster_size: The stage's cache cluster size.
        :param pulumi.Input['StageCanarySettingArgs'] canary_setting: Specifies settings for the canary deployment in this stage.
        :param pulumi.Input[str] client_certificate_id: The ID of the client certificate that API Gateway uses to call your integration endpoints in the stage. 
        :param pulumi.Input[str] deployment_id: The ID of the deployment that the stage is associated with. This parameter is required to create a stage. 
        :param pulumi.Input[str] description: A description of the stage.
        :param pulumi.Input[str] documentation_version: The version ID of the API documentation snapshot.
        :param pulumi.Input[Sequence[pulumi.Input['StageMethodSettingArgs']]] method_settings: Settings for all methods in the stage.
        :param pulumi.Input[str] stage_name: The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).
        :param pulumi.Input[Sequence[pulumi.Input['StageTagArgs']]] tags: An array of arbitrary tags (key-value pairs) to associate with the stage.
        :param pulumi.Input[bool] tracing_enabled: Specifies whether active X-Ray tracing is enabled for this stage.
        :param Any variables: A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value.
        """
        pulumi.set(__self__, "rest_api_id", rest_api_id)
        if access_log_setting is not None:
            pulumi.set(__self__, "access_log_setting", access_log_setting)
        if cache_cluster_enabled is not None:
            pulumi.set(__self__, "cache_cluster_enabled", cache_cluster_enabled)
        if cache_cluster_size is not None:
            pulumi.set(__self__, "cache_cluster_size", cache_cluster_size)
        if canary_setting is not None:
            pulumi.set(__self__, "canary_setting", canary_setting)
        if client_certificate_id is not None:
            pulumi.set(__self__, "client_certificate_id", client_certificate_id)
        if deployment_id is not None:
            pulumi.set(__self__, "deployment_id", deployment_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if documentation_version is not None:
            pulumi.set(__self__, "documentation_version", documentation_version)
        if method_settings is not None:
            pulumi.set(__self__, "method_settings", method_settings)
        if stage_name is not None:
            pulumi.set(__self__, "stage_name", stage_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tracing_enabled is not None:
            pulumi.set(__self__, "tracing_enabled", tracing_enabled)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="restApiId")
    def rest_api_id(self) -> pulumi.Input[str]:
        """
        The ID of the RestApi resource that you're deploying with this stage.
        """
        return pulumi.get(self, "rest_api_id")

    @rest_api_id.setter
    def rest_api_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "rest_api_id", value)

    @property
    @pulumi.getter(name="accessLogSetting")
    def access_log_setting(self) -> Optional[pulumi.Input['StageAccessLogSettingArgs']]:
        """
        Specifies settings for logging access in this stage.
        """
        return pulumi.get(self, "access_log_setting")

    @access_log_setting.setter
    def access_log_setting(self, value: Optional[pulumi.Input['StageAccessLogSettingArgs']]):
        pulumi.set(self, "access_log_setting", value)

    @property
    @pulumi.getter(name="cacheClusterEnabled")
    def cache_cluster_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether cache clustering is enabled for the stage.
        """
        return pulumi.get(self, "cache_cluster_enabled")

    @cache_cluster_enabled.setter
    def cache_cluster_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cache_cluster_enabled", value)

    @property
    @pulumi.getter(name="cacheClusterSize")
    def cache_cluster_size(self) -> Optional[pulumi.Input[str]]:
        """
        The stage's cache cluster size.
        """
        return pulumi.get(self, "cache_cluster_size")

    @cache_cluster_size.setter
    def cache_cluster_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_cluster_size", value)

    @property
    @pulumi.getter(name="canarySetting")
    def canary_setting(self) -> Optional[pulumi.Input['StageCanarySettingArgs']]:
        """
        Specifies settings for the canary deployment in this stage.
        """
        return pulumi.get(self, "canary_setting")

    @canary_setting.setter
    def canary_setting(self, value: Optional[pulumi.Input['StageCanarySettingArgs']]):
        pulumi.set(self, "canary_setting", value)

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the client certificate that API Gateway uses to call your integration endpoints in the stage. 
        """
        return pulumi.get(self, "client_certificate_id")

    @client_certificate_id.setter
    def client_certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_certificate_id", value)

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the deployment that the stage is associated with. This parameter is required to create a stage. 
        """
        return pulumi.get(self, "deployment_id")

    @deployment_id.setter
    def deployment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the stage.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="documentationVersion")
    def documentation_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version ID of the API documentation snapshot.
        """
        return pulumi.get(self, "documentation_version")

    @documentation_version.setter
    def documentation_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "documentation_version", value)

    @property
    @pulumi.getter(name="methodSettings")
    def method_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StageMethodSettingArgs']]]]:
        """
        Settings for all methods in the stage.
        """
        return pulumi.get(self, "method_settings")

    @method_settings.setter
    def method_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StageMethodSettingArgs']]]]):
        pulumi.set(self, "method_settings", value)

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).
        """
        return pulumi.get(self, "stage_name")

    @stage_name.setter
    def stage_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StageTagArgs']]]]:
        """
        An array of arbitrary tags (key-value pairs) to associate with the stage.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StageTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tracingEnabled")
    def tracing_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether active X-Ray tracing is enabled for this stage.
        """
        return pulumi.get(self, "tracing_enabled")

    @tracing_enabled.setter
    def tracing_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tracing_enabled", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[Any]:
        """
        A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value.
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[Any]):
        pulumi.set(self, "variables", value)


class Stage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_log_setting: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingArgs']]] = None,
                 cache_cluster_enabled: Optional[pulumi.Input[bool]] = None,
                 cache_cluster_size: Optional[pulumi.Input[str]] = None,
                 canary_setting: Optional[pulumi.Input[pulumi.InputType['StageCanarySettingArgs']]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 documentation_version: Optional[pulumi.Input[str]] = None,
                 method_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageMethodSettingArgs']]]]] = None,
                 rest_api_id: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageTagArgs']]]]] = None,
                 tracing_enabled: Optional[pulumi.Input[bool]] = None,
                 variables: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::ApiGateway::Stage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StageAccessLogSettingArgs']] access_log_setting: Specifies settings for logging access in this stage.
        :param pulumi.Input[bool] cache_cluster_enabled: Indicates whether cache clustering is enabled for the stage.
        :param pulumi.Input[str] cache_cluster_size: The stage's cache cluster size.
        :param pulumi.Input[pulumi.InputType['StageCanarySettingArgs']] canary_setting: Specifies settings for the canary deployment in this stage.
        :param pulumi.Input[str] client_certificate_id: The ID of the client certificate that API Gateway uses to call your integration endpoints in the stage. 
        :param pulumi.Input[str] deployment_id: The ID of the deployment that the stage is associated with. This parameter is required to create a stage. 
        :param pulumi.Input[str] description: A description of the stage.
        :param pulumi.Input[str] documentation_version: The version ID of the API documentation snapshot.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageMethodSettingArgs']]]] method_settings: Settings for all methods in the stage.
        :param pulumi.Input[str] rest_api_id: The ID of the RestApi resource that you're deploying with this stage.
        :param pulumi.Input[str] stage_name: The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageTagArgs']]]] tags: An array of arbitrary tags (key-value pairs) to associate with the stage.
        :param pulumi.Input[bool] tracing_enabled: Specifies whether active X-Ray tracing is enabled for this stage.
        :param Any variables: A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::ApiGateway::Stage

        :param str resource_name: The name of the resource.
        :param StageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_log_setting: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingArgs']]] = None,
                 cache_cluster_enabled: Optional[pulumi.Input[bool]] = None,
                 cache_cluster_size: Optional[pulumi.Input[str]] = None,
                 canary_setting: Optional[pulumi.Input[pulumi.InputType['StageCanarySettingArgs']]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 documentation_version: Optional[pulumi.Input[str]] = None,
                 method_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageMethodSettingArgs']]]]] = None,
                 rest_api_id: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageTagArgs']]]]] = None,
                 tracing_enabled: Optional[pulumi.Input[bool]] = None,
                 variables: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StageArgs.__new__(StageArgs)

            __props__.__dict__["access_log_setting"] = access_log_setting
            __props__.__dict__["cache_cluster_enabled"] = cache_cluster_enabled
            __props__.__dict__["cache_cluster_size"] = cache_cluster_size
            __props__.__dict__["canary_setting"] = canary_setting
            __props__.__dict__["client_certificate_id"] = client_certificate_id
            __props__.__dict__["deployment_id"] = deployment_id
            __props__.__dict__["description"] = description
            __props__.__dict__["documentation_version"] = documentation_version
            __props__.__dict__["method_settings"] = method_settings
            if rest_api_id is None and not opts.urn:
                raise TypeError("Missing required property 'rest_api_id'")
            __props__.__dict__["rest_api_id"] = rest_api_id
            __props__.__dict__["stage_name"] = stage_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tracing_enabled"] = tracing_enabled
            __props__.__dict__["variables"] = variables
        super(Stage, __self__).__init__(
            'aws-native:apigateway:Stage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Stage':
        """
        Get an existing Stage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StageArgs.__new__(StageArgs)

        __props__.__dict__["access_log_setting"] = None
        __props__.__dict__["cache_cluster_enabled"] = None
        __props__.__dict__["cache_cluster_size"] = None
        __props__.__dict__["canary_setting"] = None
        __props__.__dict__["client_certificate_id"] = None
        __props__.__dict__["deployment_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["documentation_version"] = None
        __props__.__dict__["method_settings"] = None
        __props__.__dict__["rest_api_id"] = None
        __props__.__dict__["stage_name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tracing_enabled"] = None
        __props__.__dict__["variables"] = None
        return Stage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessLogSetting")
    def access_log_setting(self) -> pulumi.Output[Optional['outputs.StageAccessLogSetting']]:
        """
        Specifies settings for logging access in this stage.
        """
        return pulumi.get(self, "access_log_setting")

    @property
    @pulumi.getter(name="cacheClusterEnabled")
    def cache_cluster_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether cache clustering is enabled for the stage.
        """
        return pulumi.get(self, "cache_cluster_enabled")

    @property
    @pulumi.getter(name="cacheClusterSize")
    def cache_cluster_size(self) -> pulumi.Output[Optional[str]]:
        """
        The stage's cache cluster size.
        """
        return pulumi.get(self, "cache_cluster_size")

    @property
    @pulumi.getter(name="canarySetting")
    def canary_setting(self) -> pulumi.Output[Optional['outputs.StageCanarySetting']]:
        """
        Specifies settings for the canary deployment in this stage.
        """
        return pulumi.get(self, "canary_setting")

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the client certificate that API Gateway uses to call your integration endpoints in the stage. 
        """
        return pulumi.get(self, "client_certificate_id")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the deployment that the stage is associated with. This parameter is required to create a stage. 
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the stage.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentationVersion")
    def documentation_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version ID of the API documentation snapshot.
        """
        return pulumi.get(self, "documentation_version")

    @property
    @pulumi.getter(name="methodSettings")
    def method_settings(self) -> pulumi.Output[Optional[Sequence['outputs.StageMethodSetting']]]:
        """
        Settings for all methods in the stage.
        """
        return pulumi.get(self, "method_settings")

    @property
    @pulumi.getter(name="restApiId")
    def rest_api_id(self) -> pulumi.Output[str]:
        """
        The ID of the RestApi resource that you're deploying with this stage.
        """
        return pulumi.get(self, "rest_api_id")

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).
        """
        return pulumi.get(self, "stage_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.StageTag']]]:
        """
        An array of arbitrary tags (key-value pairs) to associate with the stage.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tracingEnabled")
    def tracing_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether active X-Ray tracing is enabled for this stage.
        """
        return pulumi.get(self, "tracing_enabled")

    @property
    @pulumi.getter
    def variables(self) -> pulumi.Output[Optional[Any]]:
        """
        A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value.
        """
        return pulumi.get(self, "variables")

