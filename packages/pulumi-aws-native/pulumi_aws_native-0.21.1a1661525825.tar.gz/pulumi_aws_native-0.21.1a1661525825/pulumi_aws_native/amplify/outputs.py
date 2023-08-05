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
    'AppAutoBranchCreationConfig',
    'AppBasicAuthConfig',
    'AppCustomRule',
    'AppEnvironmentVariable',
    'AppTag',
    'BranchBasicAuthConfig',
    'BranchEnvironmentVariable',
    'BranchTag',
    'DomainSubDomainSetting',
]

@pulumi.output_type
class AppAutoBranchCreationConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoBranchCreationPatterns":
            suggest = "auto_branch_creation_patterns"
        elif key == "basicAuthConfig":
            suggest = "basic_auth_config"
        elif key == "buildSpec":
            suggest = "build_spec"
        elif key == "enableAutoBranchCreation":
            suggest = "enable_auto_branch_creation"
        elif key == "enableAutoBuild":
            suggest = "enable_auto_build"
        elif key == "enablePerformanceMode":
            suggest = "enable_performance_mode"
        elif key == "enablePullRequestPreview":
            suggest = "enable_pull_request_preview"
        elif key == "environmentVariables":
            suggest = "environment_variables"
        elif key == "pullRequestEnvironmentName":
            suggest = "pull_request_environment_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppAutoBranchCreationConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppAutoBranchCreationConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppAutoBranchCreationConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_branch_creation_patterns: Optional[Sequence[str]] = None,
                 basic_auth_config: Optional['outputs.AppBasicAuthConfig'] = None,
                 build_spec: Optional[str] = None,
                 enable_auto_branch_creation: Optional[bool] = None,
                 enable_auto_build: Optional[bool] = None,
                 enable_performance_mode: Optional[bool] = None,
                 enable_pull_request_preview: Optional[bool] = None,
                 environment_variables: Optional[Sequence['outputs.AppEnvironmentVariable']] = None,
                 pull_request_environment_name: Optional[str] = None,
                 stage: Optional['AppAutoBranchCreationConfigStage'] = None):
        if auto_branch_creation_patterns is not None:
            pulumi.set(__self__, "auto_branch_creation_patterns", auto_branch_creation_patterns)
        if basic_auth_config is not None:
            pulumi.set(__self__, "basic_auth_config", basic_auth_config)
        if build_spec is not None:
            pulumi.set(__self__, "build_spec", build_spec)
        if enable_auto_branch_creation is not None:
            pulumi.set(__self__, "enable_auto_branch_creation", enable_auto_branch_creation)
        if enable_auto_build is not None:
            pulumi.set(__self__, "enable_auto_build", enable_auto_build)
        if enable_performance_mode is not None:
            pulumi.set(__self__, "enable_performance_mode", enable_performance_mode)
        if enable_pull_request_preview is not None:
            pulumi.set(__self__, "enable_pull_request_preview", enable_pull_request_preview)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if pull_request_environment_name is not None:
            pulumi.set(__self__, "pull_request_environment_name", pull_request_environment_name)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter(name="autoBranchCreationPatterns")
    def auto_branch_creation_patterns(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "auto_branch_creation_patterns")

    @property
    @pulumi.getter(name="basicAuthConfig")
    def basic_auth_config(self) -> Optional['outputs.AppBasicAuthConfig']:
        return pulumi.get(self, "basic_auth_config")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter(name="enableAutoBranchCreation")
    def enable_auto_branch_creation(self) -> Optional[bool]:
        return pulumi.get(self, "enable_auto_branch_creation")

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[bool]:
        return pulumi.get(self, "enable_auto_build")

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[bool]:
        return pulumi.get(self, "enable_performance_mode")

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[bool]:
        return pulumi.get(self, "enable_pull_request_preview")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.AppEnvironmentVariable']]:
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[str]:
        return pulumi.get(self, "pull_request_environment_name")

    @property
    @pulumi.getter
    def stage(self) -> Optional['AppAutoBranchCreationConfigStage']:
        return pulumi.get(self, "stage")


@pulumi.output_type
class AppBasicAuthConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "enableBasicAuth":
            suggest = "enable_basic_auth"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppBasicAuthConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppBasicAuthConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppBasicAuthConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enable_basic_auth: Optional[bool] = None,
                 password: Optional[str] = None,
                 username: Optional[str] = None):
        if enable_basic_auth is not None:
            pulumi.set(__self__, "enable_basic_auth", enable_basic_auth)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="enableBasicAuth")
    def enable_basic_auth(self) -> Optional[bool]:
        return pulumi.get(self, "enable_basic_auth")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        return pulumi.get(self, "username")


@pulumi.output_type
class AppCustomRule(dict):
    def __init__(__self__, *,
                 source: str,
                 target: str,
                 condition: Optional[str] = None,
                 status: Optional[str] = None):
        pulumi.set(__self__, "source", source)
        pulumi.set(__self__, "target", target)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def source(self) -> str:
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def target(self) -> str:
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def condition(self) -> Optional[str]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


@pulumi.output_type
class AppEnvironmentVariable(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class AppTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
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


@pulumi.output_type
class BranchBasicAuthConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "enableBasicAuth":
            suggest = "enable_basic_auth"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BranchBasicAuthConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BranchBasicAuthConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BranchBasicAuthConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 password: str,
                 username: str,
                 enable_basic_auth: Optional[bool] = None):
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)
        if enable_basic_auth is not None:
            pulumi.set(__self__, "enable_basic_auth", enable_basic_auth)

    @property
    @pulumi.getter
    def password(self) -> str:
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> str:
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="enableBasicAuth")
    def enable_basic_auth(self) -> Optional[bool]:
        return pulumi.get(self, "enable_basic_auth")


@pulumi.output_type
class BranchEnvironmentVariable(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class BranchTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
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


@pulumi.output_type
class DomainSubDomainSetting(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "branchName":
            suggest = "branch_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainSubDomainSetting. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainSubDomainSetting.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainSubDomainSetting.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 branch_name: str,
                 prefix: str):
        pulumi.set(__self__, "branch_name", branch_name)
        pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> str:
        return pulumi.get(self, "branch_name")

    @property
    @pulumi.getter
    def prefix(self) -> str:
        return pulumi.get(self, "prefix")


