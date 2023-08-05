# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SourceCredentialArgs', 'SourceCredential']

@pulumi.input_type
class SourceCredentialArgs:
    def __init__(__self__, *,
                 auth_type: pulumi.Input[str],
                 server_type: pulumi.Input[str],
                 token: pulumi.Input[str],
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SourceCredential resource.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        pulumi.set(__self__, "auth_type", auth_type)
        pulumi.set(__self__, "server_type", server_type)
        pulumi.set(__self__, "token", token)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> pulumi.Input[str]:
        """
        The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        """
        return pulumi.get(self, "auth_type")

    @auth_type.setter
    def auth_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "auth_type", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> pulumi.Input[str]:
        """
        The source provider used for this project.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def token(self) -> pulumi.Input[str]:
        """
        For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: pulumi.Input[str]):
        pulumi.set(self, "token", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


@pulumi.input_type
class _SourceCredentialState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 auth_type: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SourceCredential resources.
        :param pulumi.Input[str] arn: The ARN of Source Credential.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if auth_type is not None:
            pulumi.set(__self__, "auth_type", auth_type)
        if server_type is not None:
            pulumi.set(__self__, "server_type", server_type)
        if token is not None:
            pulumi.set(__self__, "token", token)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of Source Credential.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        """
        return pulumi.get(self, "auth_type")

    @auth_type.setter
    def auth_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_type", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> Optional[pulumi.Input[str]]:
        """
        The source provider used for this project.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class SourceCredential(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_type: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CodeBuild Source Credentials Resource.

        > **NOTE:**
        [Codebuild only allows a single credential per given server type in a given region](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_codebuild.GitHubSourceCredentials.html). Therefore, when you define `codebuild.SourceCredential`, `codebuild.Project` resource defined in the same module will use it.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.codebuild.SourceCredential("example",
            auth_type="PERSONAL_ACCESS_TOKEN",
            server_type="GITHUB",
            token="example")
        ```
        ### Bitbucket Server Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.codebuild.SourceCredential("example",
            auth_type="BASIC_AUTH",
            server_type="BITBUCKET",
            token="example",
            user_name="test-user")
        ```

        ## Import

        CodeBuild Source Credential can be imported using the CodeBuild Source Credential arn, e.g.,

        ```sh
         $ pulumi import aws:codebuild/sourceCredential:SourceCredential example arn:aws:codebuild:us-west-2:123456789:token:github
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SourceCredentialArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CodeBuild Source Credentials Resource.

        > **NOTE:**
        [Codebuild only allows a single credential per given server type in a given region](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_codebuild.GitHubSourceCredentials.html). Therefore, when you define `codebuild.SourceCredential`, `codebuild.Project` resource defined in the same module will use it.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.codebuild.SourceCredential("example",
            auth_type="PERSONAL_ACCESS_TOKEN",
            server_type="GITHUB",
            token="example")
        ```
        ### Bitbucket Server Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.codebuild.SourceCredential("example",
            auth_type="BASIC_AUTH",
            server_type="BITBUCKET",
            token="example",
            user_name="test-user")
        ```

        ## Import

        CodeBuild Source Credential can be imported using the CodeBuild Source Credential arn, e.g.,

        ```sh
         $ pulumi import aws:codebuild/sourceCredential:SourceCredential example arn:aws:codebuild:us-west-2:123456789:token:github
        ```

        :param str resource_name: The name of the resource.
        :param SourceCredentialArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SourceCredentialArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_type: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SourceCredentialArgs.__new__(SourceCredentialArgs)

            if auth_type is None and not opts.urn:
                raise TypeError("Missing required property 'auth_type'")
            __props__.__dict__["auth_type"] = auth_type
            if server_type is None and not opts.urn:
                raise TypeError("Missing required property 'server_type'")
            __props__.__dict__["server_type"] = server_type
            if token is None and not opts.urn:
                raise TypeError("Missing required property 'token'")
            __props__.__dict__["token"] = token
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["arn"] = None
        super(SourceCredential, __self__).__init__(
            'aws:codebuild/sourceCredential:SourceCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            auth_type: Optional[pulumi.Input[str]] = None,
            server_type: Optional[pulumi.Input[str]] = None,
            token: Optional[pulumi.Input[str]] = None,
            user_name: Optional[pulumi.Input[str]] = None) -> 'SourceCredential':
        """
        Get an existing SourceCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of Source Credential.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SourceCredentialState.__new__(_SourceCredentialState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["auth_type"] = auth_type
        __props__.__dict__["server_type"] = server_type
        __props__.__dict__["token"] = token
        __props__.__dict__["user_name"] = user_name
        return SourceCredential(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of Source Credential.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> pulumi.Output[str]:
        """
        The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        """
        return pulumi.get(self, "auth_type")

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> pulumi.Output[str]:
        """
        The source provider used for this project.
        """
        return pulumi.get(self, "server_type")

    @property
    @pulumi.getter
    def token(self) -> pulumi.Output[str]:
        """
        For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        """
        return pulumi.get(self, "token")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
        """
        return pulumi.get(self, "user_name")

