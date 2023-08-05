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
    'GetUserPoolsResult',
    'AwaitableGetUserPoolsResult',
    'get_user_pools',
    'get_user_pools_output',
]

@pulumi.output_type
class GetUserPoolsResult:
    """
    A collection of values returned by getUserPools.
    """
    def __init__(__self__, arns=None, id=None, ids=None, name=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        The set of cognito user pool Amazon Resource Names (ARNs).
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        The set of cognito user pool ids.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetUserPoolsResult(GetUserPoolsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserPoolsResult(
            arns=self.arns,
            id=self.id,
            ids=self.ids,
            name=self.name)


def get_user_pools(name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserPoolsResult:
    """
    Use this data source to get a list of cognito user pools.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    selected_rest_api = aws.apigateway.get_rest_api(name=var["api_gateway_name"])
    selected_user_pools = aws.cognito.get_user_pools(name=var["cognito_user_pool_name"])
    cognito = aws.apigateway.Authorizer("cognito",
        type="COGNITO_USER_POOLS",
        rest_api=selected_rest_api.id,
        provider_arns=selected_user_pools.arns)
    ```


    :param str name: Name of the cognito user pools. Name is not a unique attribute for cognito user pool, so multiple pools might be returned with given name. If the pool name is expected to be unique, you can reference the pool id via ```tolist(data.aws_cognito_user_pools.selected.ids)[0]```
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cognito/getUserPools:getUserPools', __args__, opts=opts, typ=GetUserPoolsResult).value

    return AwaitableGetUserPoolsResult(
        arns=__ret__.arns,
        id=__ret__.id,
        ids=__ret__.ids,
        name=__ret__.name)


@_utilities.lift_output_func(get_user_pools)
def get_user_pools_output(name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserPoolsResult]:
    """
    Use this data source to get a list of cognito user pools.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    selected_rest_api = aws.apigateway.get_rest_api(name=var["api_gateway_name"])
    selected_user_pools = aws.cognito.get_user_pools(name=var["cognito_user_pool_name"])
    cognito = aws.apigateway.Authorizer("cognito",
        type="COGNITO_USER_POOLS",
        rest_api=selected_rest_api.id,
        provider_arns=selected_user_pools.arns)
    ```


    :param str name: Name of the cognito user pools. Name is not a unique attribute for cognito user pool, so multiple pools might be returned with given name. If the pool name is expected to be unique, you can reference the pool id via ```tolist(data.aws_cognito_user_pools.selected.ids)[0]```
    """
    ...
