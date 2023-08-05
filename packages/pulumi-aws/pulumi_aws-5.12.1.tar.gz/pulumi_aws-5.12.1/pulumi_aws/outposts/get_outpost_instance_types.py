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
    'GetOutpostInstanceTypesResult',
    'AwaitableGetOutpostInstanceTypesResult',
    'get_outpost_instance_types',
    'get_outpost_instance_types_output',
]

@pulumi.output_type
class GetOutpostInstanceTypesResult:
    """
    A collection of values returned by getOutpostInstanceTypes.
    """
    def __init__(__self__, arn=None, id=None, instance_types=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_types and not isinstance(instance_types, list):
            raise TypeError("Expected argument 'instance_types' to be a list")
        pulumi.set(__self__, "instance_types", instance_types)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceTypes")
    def instance_types(self) -> Sequence[str]:
        """
        Set of instance types.
        """
        return pulumi.get(self, "instance_types")


class AwaitableGetOutpostInstanceTypesResult(GetOutpostInstanceTypesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOutpostInstanceTypesResult(
            arn=self.arn,
            id=self.id,
            instance_types=self.instance_types)


def get_outpost_instance_types(arn: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOutpostInstanceTypesResult:
    """
    Information about Outposts Instance Types.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.outposts.get_outpost_instance_types(arn=data["aws_outposts_outpost"]["example"]["arn"])
    ```


    :param str arn: Outpost Amazon Resource Name (ARN).
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:outposts/getOutpostInstanceTypes:getOutpostInstanceTypes', __args__, opts=opts, typ=GetOutpostInstanceTypesResult).value

    return AwaitableGetOutpostInstanceTypesResult(
        arn=__ret__.arn,
        id=__ret__.id,
        instance_types=__ret__.instance_types)


@_utilities.lift_output_func(get_outpost_instance_types)
def get_outpost_instance_types_output(arn: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOutpostInstanceTypesResult]:
    """
    Information about Outposts Instance Types.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.outposts.get_outpost_instance_types(arn=data["aws_outposts_outpost"]["example"]["arn"])
    ```


    :param str arn: Outpost Amazon Resource Name (ARN).
    """
    ...
