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
    'GetConnectionResult',
    'AwaitableGetConnectionResult',
    'get_connection',
    'get_connection_output',
]

@pulumi.output_type
class GetConnectionResult:
    """
    A collection of values returned by getConnection.
    """
    def __init__(__self__, arn=None, catalog_id=None, connection_properties=None, connection_type=None, description=None, id=None, match_criterias=None, name=None, physical_connection_requirements=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if catalog_id and not isinstance(catalog_id, str):
            raise TypeError("Expected argument 'catalog_id' to be a str")
        pulumi.set(__self__, "catalog_id", catalog_id)
        if connection_properties and not isinstance(connection_properties, dict):
            raise TypeError("Expected argument 'connection_properties' to be a dict")
        pulumi.set(__self__, "connection_properties", connection_properties)
        if connection_type and not isinstance(connection_type, str):
            raise TypeError("Expected argument 'connection_type' to be a str")
        pulumi.set(__self__, "connection_type", connection_type)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if match_criterias and not isinstance(match_criterias, list):
            raise TypeError("Expected argument 'match_criterias' to be a list")
        pulumi.set(__self__, "match_criterias", match_criterias)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if physical_connection_requirements and not isinstance(physical_connection_requirements, list):
            raise TypeError("Expected argument 'physical_connection_requirements' to be a list")
        pulumi.set(__self__, "physical_connection_requirements", physical_connection_requirements)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the Glue Connection.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> str:
        """
        The catalog ID of the Glue Connection.
        """
        return pulumi.get(self, "catalog_id")

    @property
    @pulumi.getter(name="connectionProperties")
    def connection_properties(self) -> Mapping[str, str]:
        return pulumi.get(self, "connection_properties")

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> str:
        """
        The type of Glue Connection.
        """
        return pulumi.get(self, "connection_type")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the connection.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="matchCriterias")
    def match_criterias(self) -> Sequence[str]:
        """
        A list of criteria that can be used in selecting this connection.
        """
        return pulumi.get(self, "match_criterias")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Glue Connection.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="physicalConnectionRequirements")
    def physical_connection_requirements(self) -> Sequence['outputs.GetConnectionPhysicalConnectionRequirementResult']:
        """
        A map of physical connection requirements, such as VPC and SecurityGroup.
        """
        return pulumi.get(self, "physical_connection_requirements")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        The tags assigned to the resource
        """
        return pulumi.get(self, "tags")


class AwaitableGetConnectionResult(GetConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectionResult(
            arn=self.arn,
            catalog_id=self.catalog_id,
            connection_properties=self.connection_properties,
            connection_type=self.connection_type,
            description=self.description,
            id=self.id,
            match_criterias=self.match_criterias,
            name=self.name,
            physical_connection_requirements=self.physical_connection_requirements,
            tags=self.tags)


def get_connection(id: Optional[str] = None,
                   tags: Optional[Mapping[str, str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectionResult:
    """
    This data source can be used to fetch information about a specific Glue Connection.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_connection(id="123456789123:connection")
    ```


    :param str id: A concatenation of the catalog ID and connection name. For example, if your account ID is
           `123456789123` and the connection name is `conn` then the ID is `123456789123:conn`.
    :param Mapping[str, str] tags: The tags assigned to the resource
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:glue/getConnection:getConnection', __args__, opts=opts, typ=GetConnectionResult).value

    return AwaitableGetConnectionResult(
        arn=__ret__.arn,
        catalog_id=__ret__.catalog_id,
        connection_properties=__ret__.connection_properties,
        connection_type=__ret__.connection_type,
        description=__ret__.description,
        id=__ret__.id,
        match_criterias=__ret__.match_criterias,
        name=__ret__.name,
        physical_connection_requirements=__ret__.physical_connection_requirements,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_connection)
def get_connection_output(id: Optional[pulumi.Input[str]] = None,
                          tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectionResult]:
    """
    This data source can be used to fetch information about a specific Glue Connection.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_connection(id="123456789123:connection")
    ```


    :param str id: A concatenation of the catalog ID and connection name. For example, if your account ID is
           `123456789123` and the connection name is `conn` then the ID is `123456789123:conn`.
    :param Mapping[str, str] tags: The tags assigned to the resource
    """
    ...
