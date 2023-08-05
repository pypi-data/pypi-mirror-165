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
    'GetConnectorResult',
    'AwaitableGetConnectorResult',
    'get_connector',
    'get_connector_output',
]

@pulumi.output_type
class GetConnectorResult:
    """
    A collection of values returned by getConnector.
    """
    def __init__(__self__, arn=None, description=None, id=None, name=None, version=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the connector.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A summary description of the connector.
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
    @pulumi.getter
    def version(self) -> str:
        """
        The current version of the connector.
        """
        return pulumi.get(self, "version")


class AwaitableGetConnectorResult(GetConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectorResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            name=self.name,
            version=self.version)


def get_connector(name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectorResult:
    """
    Get information on an Amazon MSK Connect Connector.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.mskconnect.get_connector(name="example-mskconnector")
    ```


    :param str name: Name of the connector.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:mskconnect/getConnector:getConnector', __args__, opts=opts, typ=GetConnectorResult).value

    return AwaitableGetConnectorResult(
        arn=__ret__.arn,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        version=__ret__.version)


@_utilities.lift_output_func(get_connector)
def get_connector_output(name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectorResult]:
    """
    Get information on an Amazon MSK Connect Connector.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.mskconnect.get_connector(name="example-mskconnector")
    ```


    :param str name: Name of the connector.
    """
    ...
