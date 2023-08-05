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
    'LogGroupTag',
    'MetricFilterDimension',
    'MetricFilterMetricTransformation',
]

@pulumi.output_type
class LogGroupTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., :, /, =, +, - and @.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., :, /, =, +, - and @.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., :, /, =, +, - and @.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., :, /, =, +, - and @.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class MetricFilterDimension(dict):
    """
    the key-value pairs that further define a metric.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        the key-value pairs that further define a metric.
        :param str key: The key of the dimension. Maximum length of 255.
        :param str value: The value of the dimension. Maximum length of 255.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key of the dimension. Maximum length of 255.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the dimension. Maximum length of 255.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class MetricFilterMetricTransformation(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"
        elif key == "metricNamespace":
            suggest = "metric_namespace"
        elif key == "metricValue":
            suggest = "metric_value"
        elif key == "defaultValue":
            suggest = "default_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricFilterMetricTransformation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricFilterMetricTransformation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricFilterMetricTransformation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_name: str,
                 metric_namespace: str,
                 metric_value: str,
                 default_value: Optional[float] = None,
                 dimensions: Optional[Sequence['outputs.MetricFilterDimension']] = None,
                 unit: Optional['MetricFilterMetricTransformationUnit'] = None):
        """
        :param str metric_name: The name of the CloudWatch metric. Metric name must be in ASCII format.
        :param str metric_namespace: The namespace of the CloudWatch metric.
        :param str metric_value: The value to publish to the CloudWatch metric when a filter pattern matches a log event.
        :param float default_value: The value to emit when a filter pattern does not match a log event. This value can be null.
        :param Sequence['MetricFilterDimension'] dimensions: Dimensions are the key-value pairs that further define a metric
        :param 'MetricFilterMetricTransformationUnit' unit: The unit to assign to the metric. If you omit this, the unit is set as None.
        """
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "metric_namespace", metric_namespace)
        pulumi.set(__self__, "metric_value", metric_value)
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        The name of the CloudWatch metric. Metric name must be in ASCII format.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter(name="metricNamespace")
    def metric_namespace(self) -> str:
        """
        The namespace of the CloudWatch metric.
        """
        return pulumi.get(self, "metric_namespace")

    @property
    @pulumi.getter(name="metricValue")
    def metric_value(self) -> str:
        """
        The value to publish to the CloudWatch metric when a filter pattern matches a log event.
        """
        return pulumi.get(self, "metric_value")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[float]:
        """
        The value to emit when a filter pattern does not match a log event. This value can be null.
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.MetricFilterDimension']]:
        """
        Dimensions are the key-value pairs that further define a metric
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter
    def unit(self) -> Optional['MetricFilterMetricTransformationUnit']:
        """
        The unit to assign to the metric. If you omit this, the unit is set as None.
        """
        return pulumi.get(self, "unit")


