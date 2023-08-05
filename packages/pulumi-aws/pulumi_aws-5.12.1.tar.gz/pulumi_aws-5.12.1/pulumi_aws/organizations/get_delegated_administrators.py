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
    'GetDelegatedAdministratorsResult',
    'AwaitableGetDelegatedAdministratorsResult',
    'get_delegated_administrators',
    'get_delegated_administrators_output',
]

@pulumi.output_type
class GetDelegatedAdministratorsResult:
    """
    A collection of values returned by getDelegatedAdministrators.
    """
    def __init__(__self__, delegated_administrators=None, id=None, service_principal=None):
        if delegated_administrators and not isinstance(delegated_administrators, list):
            raise TypeError("Expected argument 'delegated_administrators' to be a list")
        pulumi.set(__self__, "delegated_administrators", delegated_administrators)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if service_principal and not isinstance(service_principal, str):
            raise TypeError("Expected argument 'service_principal' to be a str")
        pulumi.set(__self__, "service_principal", service_principal)

    @property
    @pulumi.getter(name="delegatedAdministrators")
    def delegated_administrators(self) -> Sequence['outputs.GetDelegatedAdministratorsDelegatedAdministratorResult']:
        """
        The list of delegated administrators in your organization, which have the following attributes:
        """
        return pulumi.get(self, "delegated_administrators")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="servicePrincipal")
    def service_principal(self) -> Optional[str]:
        return pulumi.get(self, "service_principal")


class AwaitableGetDelegatedAdministratorsResult(GetDelegatedAdministratorsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDelegatedAdministratorsResult(
            delegated_administrators=self.delegated_administrators,
            id=self.id,
            service_principal=self.service_principal)


def get_delegated_administrators(service_principal: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDelegatedAdministratorsResult:
    """
    Get a list the AWS accounts that are designated as delegated administrators in this organization

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.organizations.get_delegated_administrators(service_principal="SERVICE PRINCIPAL")
    ```


    :param str service_principal: Specifies a service principal name. If specified, then the operation lists the delegated administrators only for the specified service. If you don't specify a service principal, the operation lists all delegated administrators for all services in your organization.
    """
    __args__ = dict()
    __args__['servicePrincipal'] = service_principal
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:organizations/getDelegatedAdministrators:getDelegatedAdministrators', __args__, opts=opts, typ=GetDelegatedAdministratorsResult).value

    return AwaitableGetDelegatedAdministratorsResult(
        delegated_administrators=__ret__.delegated_administrators,
        id=__ret__.id,
        service_principal=__ret__.service_principal)


@_utilities.lift_output_func(get_delegated_administrators)
def get_delegated_administrators_output(service_principal: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDelegatedAdministratorsResult]:
    """
    Get a list the AWS accounts that are designated as delegated administrators in this organization

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.organizations.get_delegated_administrators(service_principal="SERVICE PRINCIPAL")
    ```


    :param str service_principal: Specifies a service principal name. If specified, then the operation lists the delegated administrators only for the specified service. If you don't specify a service principal, the operation lists all delegated administrators for all services in your organization.
    """
    ...
