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
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
    'get_workspace_output',
]

@pulumi.output_type
class GetWorkspaceResult:
    """
    A collection of values returned by getWorkspace.
    """
    def __init__(__self__, account_access_type=None, arn=None, authentication_providers=None, created_date=None, data_sources=None, description=None, endpoint=None, grafana_version=None, id=None, last_updated_date=None, name=None, notification_destinations=None, organization_role_name=None, organizational_units=None, permission_type=None, role_arn=None, saml_configuration_status=None, stack_set_name=None, status=None, tags=None, workspace_id=None):
        if account_access_type and not isinstance(account_access_type, str):
            raise TypeError("Expected argument 'account_access_type' to be a str")
        pulumi.set(__self__, "account_access_type", account_access_type)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if authentication_providers and not isinstance(authentication_providers, list):
            raise TypeError("Expected argument 'authentication_providers' to be a list")
        pulumi.set(__self__, "authentication_providers", authentication_providers)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if data_sources and not isinstance(data_sources, list):
            raise TypeError("Expected argument 'data_sources' to be a list")
        pulumi.set(__self__, "data_sources", data_sources)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if grafana_version and not isinstance(grafana_version, str):
            raise TypeError("Expected argument 'grafana_version' to be a str")
        pulumi.set(__self__, "grafana_version", grafana_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notification_destinations and not isinstance(notification_destinations, list):
            raise TypeError("Expected argument 'notification_destinations' to be a list")
        pulumi.set(__self__, "notification_destinations", notification_destinations)
        if organization_role_name and not isinstance(organization_role_name, str):
            raise TypeError("Expected argument 'organization_role_name' to be a str")
        pulumi.set(__self__, "organization_role_name", organization_role_name)
        if organizational_units and not isinstance(organizational_units, list):
            raise TypeError("Expected argument 'organizational_units' to be a list")
        pulumi.set(__self__, "organizational_units", organizational_units)
        if permission_type and not isinstance(permission_type, str):
            raise TypeError("Expected argument 'permission_type' to be a str")
        pulumi.set(__self__, "permission_type", permission_type)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if saml_configuration_status and not isinstance(saml_configuration_status, str):
            raise TypeError("Expected argument 'saml_configuration_status' to be a str")
        pulumi.set(__self__, "saml_configuration_status", saml_configuration_status)
        if stack_set_name and not isinstance(stack_set_name, str):
            raise TypeError("Expected argument 'stack_set_name' to be a str")
        pulumi.set(__self__, "stack_set_name", stack_set_name)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="accountAccessType")
    def account_access_type(self) -> str:
        """
        (Required) The type of account access for the workspace. Valid values are `CURRENT_ACCOUNT` and `ORGANIZATION`. If `ORGANIZATION` is specified, then `organizational_units` must also be present.
        """
        return pulumi.get(self, "account_access_type")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the Grafana workspace.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authenticationProviders")
    def authentication_providers(self) -> Sequence[str]:
        """
        (Required) The authentication providers for the workspace. Valid values are `AWS_SSO`, `SAML`, or both.
        """
        return pulumi.get(self, "authentication_providers")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The creation date of the Grafana workspace.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="dataSources")
    def data_sources(self) -> Sequence[str]:
        """
        The data sources for the workspace.
        """
        return pulumi.get(self, "data_sources")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The workspace description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        The endpoint of the Grafana workspace.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="grafanaVersion")
    def grafana_version(self) -> str:
        """
        The version of Grafana running on the workspace.
        """
        return pulumi.get(self, "grafana_version")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> str:
        """
        The last updated date of the Grafana workspace.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The Grafana workspace name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notificationDestinations")
    def notification_destinations(self) -> Sequence[str]:
        """
        The notification destinations.
        """
        return pulumi.get(self, "notification_destinations")

    @property
    @pulumi.getter(name="organizationRoleName")
    def organization_role_name(self) -> str:
        """
        The role name that the workspace uses to access resources through Amazon Organizations.
        """
        return pulumi.get(self, "organization_role_name")

    @property
    @pulumi.getter(name="organizationalUnits")
    def organizational_units(self) -> Sequence[str]:
        """
        The Amazon Organizations organizational units that the workspace is authorized to use data sources from.
        """
        return pulumi.get(self, "organizational_units")

    @property
    @pulumi.getter(name="permissionType")
    def permission_type(self) -> str:
        """
        The permission type of the workspace.
        """
        return pulumi.get(self, "permission_type")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        The IAM role ARN that the workspace assumes.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="samlConfigurationStatus")
    def saml_configuration_status(self) -> str:
        return pulumi.get(self, "saml_configuration_status")

    @property
    @pulumi.getter(name="stackSetName")
    def stack_set_name(self) -> str:
        """
        The AWS CloudFormation stack set name that provisions IAM roles to be used by the workspace.
        """
        return pulumi.get(self, "stack_set_name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the Grafana workspace.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        The tags assigned to the resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        return pulumi.get(self, "workspace_id")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            account_access_type=self.account_access_type,
            arn=self.arn,
            authentication_providers=self.authentication_providers,
            created_date=self.created_date,
            data_sources=self.data_sources,
            description=self.description,
            endpoint=self.endpoint,
            grafana_version=self.grafana_version,
            id=self.id,
            last_updated_date=self.last_updated_date,
            name=self.name,
            notification_destinations=self.notification_destinations,
            organization_role_name=self.organization_role_name,
            organizational_units=self.organizational_units,
            permission_type=self.permission_type,
            role_arn=self.role_arn,
            saml_configuration_status=self.saml_configuration_status,
            stack_set_name=self.stack_set_name,
            status=self.status,
            tags=self.tags,
            workspace_id=self.workspace_id)


def get_workspace(tags: Optional[Mapping[str, str]] = None,
                  workspace_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    Provides an Amazon Managed Grafana workspace data source.

    ## Example Usage
    ### Basic configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.grafana.get_workspace(workspace_id="g-2054c75a02")
    ```


    :param Mapping[str, str] tags: The tags assigned to the resource
    :param str workspace_id: The Grafana workspace ID.
    """
    __args__ = dict()
    __args__['tags'] = tags
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:grafana/getWorkspace:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        account_access_type=__ret__.account_access_type,
        arn=__ret__.arn,
        authentication_providers=__ret__.authentication_providers,
        created_date=__ret__.created_date,
        data_sources=__ret__.data_sources,
        description=__ret__.description,
        endpoint=__ret__.endpoint,
        grafana_version=__ret__.grafana_version,
        id=__ret__.id,
        last_updated_date=__ret__.last_updated_date,
        name=__ret__.name,
        notification_destinations=__ret__.notification_destinations,
        organization_role_name=__ret__.organization_role_name,
        organizational_units=__ret__.organizational_units,
        permission_type=__ret__.permission_type,
        role_arn=__ret__.role_arn,
        saml_configuration_status=__ret__.saml_configuration_status,
        stack_set_name=__ret__.stack_set_name,
        status=__ret__.status,
        tags=__ret__.tags,
        workspace_id=__ret__.workspace_id)


@_utilities.lift_output_func(get_workspace)
def get_workspace_output(tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         workspace_id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspaceResult]:
    """
    Provides an Amazon Managed Grafana workspace data source.

    ## Example Usage
    ### Basic configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.grafana.get_workspace(workspace_id="g-2054c75a02")
    ```


    :param Mapping[str, str] tags: The tags assigned to the resource
    :param str workspace_id: The Grafana workspace ID.
    """
    ...
