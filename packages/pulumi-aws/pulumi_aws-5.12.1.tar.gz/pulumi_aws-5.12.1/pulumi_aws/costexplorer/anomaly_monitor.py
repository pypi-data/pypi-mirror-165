# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AnomalyMonitorArgs', 'AnomalyMonitor']

@pulumi.input_type
class AnomalyMonitorArgs:
    def __init__(__self__, *,
                 monitor_type: pulumi.Input[str],
                 monitor_dimension: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AnomalyMonitor resource.
        :param pulumi.Input[str] monitor_type: The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        :param pulumi.Input[str] monitor_dimension: The dimensions to evaluate. Valid values: `SERVICE`.
        :param pulumi.Input[str] monitor_specification: A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        :param pulumi.Input[str] name: The name of the monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "monitor_type", monitor_type)
        if monitor_dimension is not None:
            pulumi.set(__self__, "monitor_dimension", monitor_dimension)
        if monitor_specification is not None:
            pulumi.set(__self__, "monitor_specification", monitor_specification)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="monitorType")
    def monitor_type(self) -> pulumi.Input[str]:
        """
        The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        """
        return pulumi.get(self, "monitor_type")

    @monitor_type.setter
    def monitor_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "monitor_type", value)

    @property
    @pulumi.getter(name="monitorDimension")
    def monitor_dimension(self) -> Optional[pulumi.Input[str]]:
        """
        The dimensions to evaluate. Valid values: `SERVICE`.
        """
        return pulumi.get(self, "monitor_dimension")

    @monitor_dimension.setter
    def monitor_dimension(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_dimension", value)

    @property
    @pulumi.getter(name="monitorSpecification")
    def monitor_specification(self) -> Optional[pulumi.Input[str]]:
        """
        A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        """
        return pulumi.get(self, "monitor_specification")

    @monitor_specification.setter
    def monitor_specification(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_specification", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AnomalyMonitorState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 monitor_dimension: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 monitor_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AnomalyMonitor resources.
        :param pulumi.Input[str] arn: ARN of the anomaly monitor.
        :param pulumi.Input[str] monitor_dimension: The dimensions to evaluate. Valid values: `SERVICE`.
        :param pulumi.Input[str] monitor_specification: A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        :param pulumi.Input[str] monitor_type: The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        :param pulumi.Input[str] name: The name of the monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if monitor_dimension is not None:
            pulumi.set(__self__, "monitor_dimension", monitor_dimension)
        if monitor_specification is not None:
            pulumi.set(__self__, "monitor_specification", monitor_specification)
        if monitor_type is not None:
            pulumi.set(__self__, "monitor_type", monitor_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the anomaly monitor.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="monitorDimension")
    def monitor_dimension(self) -> Optional[pulumi.Input[str]]:
        """
        The dimensions to evaluate. Valid values: `SERVICE`.
        """
        return pulumi.get(self, "monitor_dimension")

    @monitor_dimension.setter
    def monitor_dimension(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_dimension", value)

    @property
    @pulumi.getter(name="monitorSpecification")
    def monitor_specification(self) -> Optional[pulumi.Input[str]]:
        """
        A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        """
        return pulumi.get(self, "monitor_specification")

    @monitor_specification.setter
    def monitor_specification(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_specification", value)

    @property
    @pulumi.getter(name="monitorType")
    def monitor_type(self) -> Optional[pulumi.Input[str]]:
        """
        The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        """
        return pulumi.get(self, "monitor_type")

    @monitor_type.setter
    def monitor_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class AnomalyMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 monitor_dimension: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 monitor_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a CE Anomaly Monitor.

        ## Example Usage

        There are two main types of a Cost Anomaly Monitor: `DIMENSIONAL` and `CUSTOM`.
        ### Dimensional Example

        ```python
        import pulumi
        import pulumi_aws as aws

        service_monitor = aws.costexplorer.AnomalyMonitor("serviceMonitor",
            monitor_dimension="SERVICE",
            monitor_type="DIMENSIONAL")
        ```
        ### Custom Example

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.costexplorer.AnomalyMonitor("test",
            monitor_specification=\"\"\"{
        	"And": null,
        	"CostCategories": null,
        	"Dimensions": null,
        	"Not": null,
        	"Or": null,
        	"Tags": {
        		"Key": "CostCenter",
        		"MatchOptions": null,
        		"Values": [
        			"10000"
        		]
        	}
        }

        \"\"\",
            monitor_type="CUSTOM")
        ```

        ## Import

        `aws_ce_anomaly_monitor` can be imported using the `id`, e.g.

        ```sh
         $ pulumi import aws:costexplorer/anomalyMonitor:AnomalyMonitor example costAnomalyMonitorARN
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] monitor_dimension: The dimensions to evaluate. Valid values: `SERVICE`.
        :param pulumi.Input[str] monitor_specification: A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        :param pulumi.Input[str] monitor_type: The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        :param pulumi.Input[str] name: The name of the monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnomalyMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CE Anomaly Monitor.

        ## Example Usage

        There are two main types of a Cost Anomaly Monitor: `DIMENSIONAL` and `CUSTOM`.
        ### Dimensional Example

        ```python
        import pulumi
        import pulumi_aws as aws

        service_monitor = aws.costexplorer.AnomalyMonitor("serviceMonitor",
            monitor_dimension="SERVICE",
            monitor_type="DIMENSIONAL")
        ```
        ### Custom Example

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.costexplorer.AnomalyMonitor("test",
            monitor_specification=\"\"\"{
        	"And": null,
        	"CostCategories": null,
        	"Dimensions": null,
        	"Not": null,
        	"Or": null,
        	"Tags": {
        		"Key": "CostCenter",
        		"MatchOptions": null,
        		"Values": [
        			"10000"
        		]
        	}
        }

        \"\"\",
            monitor_type="CUSTOM")
        ```

        ## Import

        `aws_ce_anomaly_monitor` can be imported using the `id`, e.g.

        ```sh
         $ pulumi import aws:costexplorer/anomalyMonitor:AnomalyMonitor example costAnomalyMonitorARN
        ```

        :param str resource_name: The name of the resource.
        :param AnomalyMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnomalyMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 monitor_dimension: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 monitor_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AnomalyMonitorArgs.__new__(AnomalyMonitorArgs)

            __props__.__dict__["monitor_dimension"] = monitor_dimension
            __props__.__dict__["monitor_specification"] = monitor_specification
            if monitor_type is None and not opts.urn:
                raise TypeError("Missing required property 'monitor_type'")
            __props__.__dict__["monitor_type"] = monitor_type
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(AnomalyMonitor, __self__).__init__(
            'aws:costexplorer/anomalyMonitor:AnomalyMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            monitor_dimension: Optional[pulumi.Input[str]] = None,
            monitor_specification: Optional[pulumi.Input[str]] = None,
            monitor_type: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'AnomalyMonitor':
        """
        Get an existing AnomalyMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the anomaly monitor.
        :param pulumi.Input[str] monitor_dimension: The dimensions to evaluate. Valid values: `SERVICE`.
        :param pulumi.Input[str] monitor_specification: A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        :param pulumi.Input[str] monitor_type: The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        :param pulumi.Input[str] name: The name of the monitor.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AnomalyMonitorState.__new__(_AnomalyMonitorState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["monitor_dimension"] = monitor_dimension
        __props__.__dict__["monitor_specification"] = monitor_specification
        __props__.__dict__["monitor_type"] = monitor_type
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return AnomalyMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the anomaly monitor.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="monitorDimension")
    def monitor_dimension(self) -> pulumi.Output[Optional[str]]:
        """
        The dimensions to evaluate. Valid values: `SERVICE`.
        """
        return pulumi.get(self, "monitor_dimension")

    @property
    @pulumi.getter(name="monitorSpecification")
    def monitor_specification(self) -> pulumi.Output[Optional[str]]:
        """
        A valid JSON representation for the [Expression](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html) object.
        """
        return pulumi.get(self, "monitor_specification")

    @property
    @pulumi.getter(name="monitorType")
    def monitor_type(self) -> pulumi.Output[str]:
        """
        The possible type values. Valid values: `DIMENSIONAL` | `CUSTOM`.
        """
        return pulumi.get(self, "monitor_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

