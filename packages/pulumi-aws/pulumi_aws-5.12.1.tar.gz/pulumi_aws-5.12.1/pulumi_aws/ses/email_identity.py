# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EmailIdentityArgs', 'EmailIdentity']

@pulumi.input_type
class EmailIdentityArgs:
    def __init__(__self__, *,
                 email: pulumi.Input[str]):
        """
        The set of arguments for constructing a EmailIdentity resource.
        :param pulumi.Input[str] email: The email address to assign to SES
        """
        pulumi.set(__self__, "email", email)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        """
        The email address to assign to SES
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)


@pulumi.input_type
class _EmailIdentityState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EmailIdentity resources.
        :param pulumi.Input[str] arn: The ARN of the email identity.
        :param pulumi.Input[str] email: The email address to assign to SES
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if email is not None:
            pulumi.set(__self__, "email", email)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the email identity.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The email address to assign to SES
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)


class EmailIdentity(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an SES email identity resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ses.EmailIdentity("example", email="email@example.com")
        ```

        ## Import

        SES email identities can be imported using the email address.

        ```sh
         $ pulumi import aws:ses/emailIdentity:EmailIdentity example email@example.com
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email: The email address to assign to SES
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailIdentityArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an SES email identity resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ses.EmailIdentity("example", email="email@example.com")
        ```

        ## Import

        SES email identities can be imported using the email address.

        ```sh
         $ pulumi import aws:ses/emailIdentity:EmailIdentity example email@example.com
        ```

        :param str resource_name: The name of the resource.
        :param EmailIdentityArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailIdentityArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EmailIdentityArgs.__new__(EmailIdentityArgs)

            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__.__dict__["email"] = email
            __props__.__dict__["arn"] = None
        super(EmailIdentity, __self__).__init__(
            'aws:ses/emailIdentity:EmailIdentity',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            email: Optional[pulumi.Input[str]] = None) -> 'EmailIdentity':
        """
        Get an existing EmailIdentity resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the email identity.
        :param pulumi.Input[str] email: The email address to assign to SES
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailIdentityState.__new__(_EmailIdentityState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["email"] = email
        return EmailIdentity(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the email identity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[str]:
        """
        The email address to assign to SES
        """
        return pulumi.get(self, "email")

