# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetReportPlanResult',
    'AwaitableGetReportPlanResult',
    'get_report_plan',
    'get_report_plan_output',
]

@pulumi.output_type
class GetReportPlanResult:
    """
    A collection of values returned by getReportPlan.
    """
    def __init__(__self__, arn=None, creation_time=None, deployment_status=None, description=None, id=None, name=None, report_delivery_channels=None, report_settings=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if deployment_status and not isinstance(deployment_status, str):
            raise TypeError("Expected argument 'deployment_status' to be a str")
        pulumi.set(__self__, "deployment_status", deployment_status)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if report_delivery_channels and not isinstance(report_delivery_channels, list):
            raise TypeError("Expected argument 'report_delivery_channels' to be a list")
        pulumi.set(__self__, "report_delivery_channels", report_delivery_channels)
        if report_settings and not isinstance(report_settings, list):
            raise TypeError("Expected argument 'report_settings' to be a list")
        pulumi.set(__self__, "report_settings", report_settings)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the backup report plan.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        The date and time that a report plan is created, in Unix format and Coordinated Universal Time (UTC).
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> str:
        """
        The deployment status of a report plan. The statuses are: `CREATE_IN_PROGRESS` | `UPDATE_IN_PROGRESS` | `DELETE_IN_PROGRESS` | `COMPLETED`.
        """
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the report plan.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="reportDeliveryChannels")
    def report_delivery_channels(self) -> Sequence['outputs.GetReportPlanReportDeliveryChannelResult']:
        """
        An object that contains information about where and how to deliver your reports, specifically your Amazon S3 bucket name, S3 key prefix, and the formats of your reports. Detailed below.
        """
        return pulumi.get(self, "report_delivery_channels")

    @property
    @pulumi.getter(name="reportSettings")
    def report_settings(self) -> Sequence['outputs.GetReportPlanReportSettingResult']:
        """
        An object that identifies the report template for the report. Reports are built using a report template. Detailed below.
        """
        return pulumi.get(self, "report_settings")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Metadata that you can assign to help organize the report plans you create.
        """
        return pulumi.get(self, "tags")


class AwaitableGetReportPlanResult(GetReportPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReportPlanResult(
            arn=self.arn,
            creation_time=self.creation_time,
            deployment_status=self.deployment_status,
            description=self.description,
            id=self.id,
            name=self.name,
            report_delivery_channels=self.report_delivery_channels,
            report_settings=self.report_settings,
            tags=self.tags)


def get_report_plan(name: Optional[str] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReportPlanResult:
    """
    Use this data source to get information on an existing backup report plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_report_plan(name="tf_example_backup_report_plan_name")
    ```


    :param str name: The backup report plan name.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the report plans you create.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:backup/getReportPlan:getReportPlan', __args__, opts=opts, typ=GetReportPlanResult).value

    return AwaitableGetReportPlanResult(
        arn=__ret__.arn,
        creation_time=__ret__.creation_time,
        deployment_status=__ret__.deployment_status,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        report_delivery_channels=__ret__.report_delivery_channels,
        report_settings=__ret__.report_settings,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_report_plan)
def get_report_plan_output(name: Optional[pulumi.Input[str]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetReportPlanResult]:
    """
    Use this data source to get information on an existing backup report plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_report_plan(name="tf_example_backup_report_plan_name")
    ```


    :param str name: The backup report plan name.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the report plans you create.
    """
    ...
