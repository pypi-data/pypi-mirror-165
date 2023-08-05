# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserPolicyAttachmentArgs', 'UserPolicyAttachment']

@pulumi.input_type
class UserPolicyAttachmentArgs:
    def __init__(__self__, *,
                 policy_arn: pulumi.Input[str],
                 user: pulumi.Input[str]):
        """
        The set of arguments for constructing a UserPolicyAttachment resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] user: The user the policy should be applied to
        """
        pulumi.set(__self__, "policy_arn", policy_arn)
        pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        The user the policy should be applied to
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)


@pulumi.input_type
class _UserPolicyAttachmentState:
    def __init__(__self__, *,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserPolicyAttachment resources.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] user: The user the policy should be applied to
        """
        if policy_arn is not None:
            pulumi.set(__self__, "policy_arn", policy_arn)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The user the policy should be applied to
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class UserPolicyAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a Managed IAM Policy to an IAM user

        > **NOTE:** The usage of this resource conflicts with the `iam.PolicyAttachment` resource and will permanently show a difference if both are defined.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        user = aws.iam.User("user")
        policy = aws.iam.Policy("policy",
            description="A test policy",
            policy="{ ... policy JSON ... }")
        test_attach = aws.iam.UserPolicyAttachment("test-attach",
            user=user.name,
            policy_arn=policy.arn)
        ```

        ## Import

        IAM user policy attachments can be imported using the user name and policy arn separated by `/`.

        ```sh
         $ pulumi import aws:iam/userPolicyAttachment:UserPolicyAttachment test-attach test-user/arn:aws:iam::xxxxxxxxxxxx:policy/test-policy
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] user: The user the policy should be applied to
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserPolicyAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a Managed IAM Policy to an IAM user

        > **NOTE:** The usage of this resource conflicts with the `iam.PolicyAttachment` resource and will permanently show a difference if both are defined.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        user = aws.iam.User("user")
        policy = aws.iam.Policy("policy",
            description="A test policy",
            policy="{ ... policy JSON ... }")
        test_attach = aws.iam.UserPolicyAttachment("test-attach",
            user=user.name,
            policy_arn=policy.arn)
        ```

        ## Import

        IAM user policy attachments can be imported using the user name and policy arn separated by `/`.

        ```sh
         $ pulumi import aws:iam/userPolicyAttachment:UserPolicyAttachment test-attach test-user/arn:aws:iam::xxxxxxxxxxxx:policy/test-policy
        ```

        :param str resource_name: The name of the resource.
        :param UserPolicyAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserPolicyAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserPolicyAttachmentArgs.__new__(UserPolicyAttachmentArgs)

            if policy_arn is None and not opts.urn:
                raise TypeError("Missing required property 'policy_arn'")
            __props__.__dict__["policy_arn"] = policy_arn
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
        super(UserPolicyAttachment, __self__).__init__(
            'aws:iam/userPolicyAttachment:UserPolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy_arn: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'UserPolicyAttachment':
        """
        Get an existing UserPolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] user: The user the policy should be applied to
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserPolicyAttachmentState.__new__(_UserPolicyAttachmentState)

        __props__.__dict__["policy_arn"] = policy_arn
        __props__.__dict__["user"] = user
        return UserPolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        The user the policy should be applied to
        """
        return pulumi.get(self, "user")

