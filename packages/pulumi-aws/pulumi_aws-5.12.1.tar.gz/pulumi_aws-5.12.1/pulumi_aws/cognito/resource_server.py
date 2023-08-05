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
from ._inputs import *

__all__ = ['ResourceServerArgs', 'ResourceServer']

@pulumi.input_type
class ResourceServerArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 user_pool_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]] = None):
        """
        The set of arguments for constructing a ResourceServer resource.
        :param pulumi.Input[str] identifier: An identifier for the resource server.
        :param pulumi.Input[str] name: A name for the resource server.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]] scopes: A list of Authorization Scope.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "user_pool_id", user_pool_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if scopes is not None:
            pulumi.set(__self__, "scopes", scopes)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        An identifier for the resource server.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_pool_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the resource server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]]:
        """
        A list of Authorization Scope.
        """
        return pulumi.get(self, "scopes")

    @scopes.setter
    def scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]]):
        pulumi.set(self, "scopes", value)


@pulumi.input_type
class _ResourceServerState:
    def __init__(__self__, *,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scope_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResourceServer resources.
        :param pulumi.Input[str] identifier: An identifier for the resource server.
        :param pulumi.Input[str] name: A name for the resource server.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scope_identifiers: A list of all scopes configured for this resource server in the format identifier/scope_name.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]] scopes: A list of Authorization Scope.
        """
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if scope_identifiers is not None:
            pulumi.set(__self__, "scope_identifiers", scope_identifiers)
        if scopes is not None:
            pulumi.set(__self__, "scopes", scopes)
        if user_pool_id is not None:
            pulumi.set(__self__, "user_pool_id", user_pool_id)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        An identifier for the resource server.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the resource server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="scopeIdentifiers")
    def scope_identifiers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of all scopes configured for this resource server in the format identifier/scope_name.
        """
        return pulumi.get(self, "scope_identifiers")

    @scope_identifiers.setter
    def scope_identifiers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "scope_identifiers", value)

    @property
    @pulumi.getter
    def scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]]:
        """
        A list of Authorization Scope.
        """
        return pulumi.get(self, "scopes")

    @scopes.setter
    def scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceServerScopeArgs']]]]):
        pulumi.set(self, "scopes", value)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_pool_id", value)


class ResourceServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceServerScopeArgs']]]]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cognito Resource Server.

        ## Example Usage
        ### Create a basic resource server

        ```python
        import pulumi
        import pulumi_aws as aws

        pool = aws.cognito.UserPool("pool")
        resource = aws.cognito.ResourceServer("resource",
            identifier="https://example.com",
            user_pool_id=pool.id)
        ```
        ### Create a resource server with sample-scope

        ```python
        import pulumi
        import pulumi_aws as aws

        pool = aws.cognito.UserPool("pool")
        resource = aws.cognito.ResourceServer("resource",
            identifier="https://example.com",
            scopes=[aws.cognito.ResourceServerScopeArgs(
                scope_name="sample-scope",
                scope_description="a Sample Scope Description",
            )],
            user_pool_id=pool.id)
        ```

        ## Import

        `aws_cognito_resource_server` can be imported using their User Pool ID and Identifier, e.g.,

        ```sh
         $ pulumi import aws:cognito/resourceServer:ResourceServer example us-west-2_abc123:https://example.com
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identifier: An identifier for the resource server.
        :param pulumi.Input[str] name: A name for the resource server.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceServerScopeArgs']]]] scopes: A list of Authorization Scope.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cognito Resource Server.

        ## Example Usage
        ### Create a basic resource server

        ```python
        import pulumi
        import pulumi_aws as aws

        pool = aws.cognito.UserPool("pool")
        resource = aws.cognito.ResourceServer("resource",
            identifier="https://example.com",
            user_pool_id=pool.id)
        ```
        ### Create a resource server with sample-scope

        ```python
        import pulumi
        import pulumi_aws as aws

        pool = aws.cognito.UserPool("pool")
        resource = aws.cognito.ResourceServer("resource",
            identifier="https://example.com",
            scopes=[aws.cognito.ResourceServerScopeArgs(
                scope_name="sample-scope",
                scope_description="a Sample Scope Description",
            )],
            user_pool_id=pool.id)
        ```

        ## Import

        `aws_cognito_resource_server` can be imported using their User Pool ID and Identifier, e.g.,

        ```sh
         $ pulumi import aws:cognito/resourceServer:ResourceServer example us-west-2_abc123:https://example.com
        ```

        :param str resource_name: The name of the resource.
        :param ResourceServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceServerScopeArgs']]]]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceServerArgs.__new__(ResourceServerArgs)

            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["name"] = name
            __props__.__dict__["scopes"] = scopes
            if user_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_pool_id'")
            __props__.__dict__["user_pool_id"] = user_pool_id
            __props__.__dict__["scope_identifiers"] = None
        super(ResourceServer, __self__).__init__(
            'aws:cognito/resourceServer:ResourceServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            scope_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            scopes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceServerScopeArgs']]]]] = None,
            user_pool_id: Optional[pulumi.Input[str]] = None) -> 'ResourceServer':
        """
        Get an existing ResourceServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identifier: An identifier for the resource server.
        :param pulumi.Input[str] name: A name for the resource server.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scope_identifiers: A list of all scopes configured for this resource server in the format identifier/scope_name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceServerScopeArgs']]]] scopes: A list of Authorization Scope.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceServerState.__new__(_ResourceServerState)

        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["name"] = name
        __props__.__dict__["scope_identifiers"] = scope_identifiers
        __props__.__dict__["scopes"] = scopes
        __props__.__dict__["user_pool_id"] = user_pool_id
        return ResourceServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        An identifier for the resource server.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name for the resource server.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="scopeIdentifiers")
    def scope_identifiers(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of all scopes configured for this resource server in the format identifier/scope_name.
        """
        return pulumi.get(self, "scope_identifiers")

    @property
    @pulumi.getter
    def scopes(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceServerScope']]]:
        """
        A list of Authorization Scope.
        """
        return pulumi.get(self, "scopes")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "user_pool_id")

