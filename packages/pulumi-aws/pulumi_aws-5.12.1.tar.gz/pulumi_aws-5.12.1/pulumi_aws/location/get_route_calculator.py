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
    'GetRouteCalculatorResult',
    'AwaitableGetRouteCalculatorResult',
    'get_route_calculator',
    'get_route_calculator_output',
]

@pulumi.output_type
class GetRouteCalculatorResult:
    """
    A collection of values returned by getRouteCalculator.
    """
    def __init__(__self__, calculator_arn=None, calculator_name=None, create_time=None, data_source=None, description=None, id=None, tags=None, update_time=None):
        if calculator_arn and not isinstance(calculator_arn, str):
            raise TypeError("Expected argument 'calculator_arn' to be a str")
        pulumi.set(__self__, "calculator_arn", calculator_arn)
        if calculator_name and not isinstance(calculator_name, str):
            raise TypeError("Expected argument 'calculator_name' to be a str")
        pulumi.set(__self__, "calculator_name", calculator_name)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if data_source and not isinstance(data_source, str):
            raise TypeError("Expected argument 'data_source' to be a str")
        pulumi.set(__self__, "data_source", data_source)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="calculatorArn")
    def calculator_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) for the Route calculator resource. Use the ARN when you specify a resource across AWS.
        """
        return pulumi.get(self, "calculator_arn")

    @property
    @pulumi.getter(name="calculatorName")
    def calculator_name(self) -> str:
        return pulumi.get(self, "calculator_name")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The timestamp for when the route calculator resource was created in ISO 8601 format.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="dataSource")
    def data_source(self) -> str:
        """
        The data provider of traffic and road network data.
        """
        return pulumi.get(self, "data_source")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The optional description of the route calculator resource.
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
    def tags(self) -> Mapping[str, str]:
        """
        Key-value map of resource tags for the route calculator.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The timestamp for when the route calculator resource was last updated in ISO 8601 format.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetRouteCalculatorResult(GetRouteCalculatorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRouteCalculatorResult(
            calculator_arn=self.calculator_arn,
            calculator_name=self.calculator_name,
            create_time=self.create_time,
            data_source=self.data_source,
            description=self.description,
            id=self.id,
            tags=self.tags,
            update_time=self.update_time)


def get_route_calculator(calculator_name: Optional[str] = None,
                         tags: Optional[Mapping[str, str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRouteCalculatorResult:
    """
    Retrieve information about a Location Service Route Calculator.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.location.get_route_calculator(calculator_name="example")
    ```


    :param str calculator_name: The name of the route calculator resource.
    :param Mapping[str, str] tags: Key-value map of resource tags for the route calculator.
    """
    __args__ = dict()
    __args__['calculatorName'] = calculator_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:location/getRouteCalculator:getRouteCalculator', __args__, opts=opts, typ=GetRouteCalculatorResult).value

    return AwaitableGetRouteCalculatorResult(
        calculator_arn=__ret__.calculator_arn,
        calculator_name=__ret__.calculator_name,
        create_time=__ret__.create_time,
        data_source=__ret__.data_source,
        description=__ret__.description,
        id=__ret__.id,
        tags=__ret__.tags,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_route_calculator)
def get_route_calculator_output(calculator_name: Optional[pulumi.Input[str]] = None,
                                tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRouteCalculatorResult]:
    """
    Retrieve information about a Location Service Route Calculator.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.location.get_route_calculator(calculator_name="example")
    ```


    :param str calculator_name: The name of the route calculator resource.
    :param Mapping[str, str] tags: Key-value map of resource tags for the route calculator.
    """
    ...
