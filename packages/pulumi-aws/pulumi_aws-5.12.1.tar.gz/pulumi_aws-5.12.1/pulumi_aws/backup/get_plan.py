# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetPlanResult',
    'AwaitableGetPlanResult',
    'get_plan',
    'get_plan_output',
]

@pulumi.output_type
class GetPlanResult:
    """
    A collection of values returned by getPlan.
    """
    def __init__(__self__, arn=None, id=None, name=None, plan_id=None, tags=None, version=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if plan_id and not isinstance(plan_id, str):
            raise TypeError("Expected argument 'plan_id' to be a str")
        pulumi.set(__self__, "plan_id", plan_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the backup plan.
        """
        return pulumi.get(self, "arn")

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
        """
        The display name of a backup plan.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> str:
        return pulumi.get(self, "plan_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Metadata that you can assign to help organize the plans you create.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Unique, randomly generated, Unicode, UTF-8 encoded string that serves as the version ID of the backup plan.
        """
        return pulumi.get(self, "version")


class AwaitableGetPlanResult(GetPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPlanResult(
            arn=self.arn,
            id=self.id,
            name=self.name,
            plan_id=self.plan_id,
            tags=self.tags,
            version=self.version)


def get_plan(plan_id: Optional[str] = None,
             tags: Optional[Mapping[str, str]] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPlanResult:
    """
    Use this data source to get information on an existing backup plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_plan(plan_id="tf_example_backup_plan_id")
    ```


    :param str plan_id: The backup plan ID.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the plans you create.
    """
    __args__ = dict()
    __args__['planId'] = plan_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:backup/getPlan:getPlan', __args__, opts=opts, typ=GetPlanResult).value

    return AwaitableGetPlanResult(
        arn=__ret__.arn,
        id=__ret__.id,
        name=__ret__.name,
        plan_id=__ret__.plan_id,
        tags=__ret__.tags,
        version=__ret__.version)


@_utilities.lift_output_func(get_plan)
def get_plan_output(plan_id: Optional[pulumi.Input[str]] = None,
                    tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPlanResult]:
    """
    Use this data source to get information on an existing backup plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_plan(plan_id="tf_example_backup_plan_id")
    ```


    :param str plan_id: The backup plan ID.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the plans you create.
    """
    ...
