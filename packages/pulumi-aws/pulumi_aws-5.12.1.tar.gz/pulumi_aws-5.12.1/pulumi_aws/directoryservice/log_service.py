# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LogServiceArgs', 'LogService']

@pulumi.input_type
class LogServiceArgs:
    def __init__(__self__, *,
                 directory_id: pulumi.Input[str],
                 log_group_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a LogService resource.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[str] log_group_name: Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        pulumi.set(__self__, "directory_id", directory_id)
        pulumi.set(__self__, "log_group_name", log_group_name)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Input[str]:
        """
        The id of directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)


@pulumi.input_type
class _LogServiceState:
    def __init__(__self__, *,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LogService resources.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[str] log_group_name: Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        if directory_id is not None:
            pulumi.set(__self__, "directory_id", directory_id)
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)


class LogService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Log subscription for AWS Directory Service that pushes logs to cloudwatch.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_log_group = aws.cloudwatch.LogGroup("exampleLogGroup", retention_in_days=14)
        ad_log_policy_policy_document = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            actions=[
                "logs:CreateLogStream",
                "logs:PutLogEvents",
            ],
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                identifiers=["ds.amazonaws.com"],
                type="Service",
            )],
            resources=[example_log_group.arn.apply(lambda arn: f"{arn}:*")],
            effect="Allow",
        )])
        ad_log_policy_log_resource_policy = aws.cloudwatch.LogResourcePolicy("ad-log-policyLogResourcePolicy",
            policy_document=ad_log_policy_policy_document.json,
            policy_name="ad-log-policy")
        example_log_service = aws.directoryservice.LogService("exampleLogService",
            directory_id=aws_directory_service_directory["example"]["id"],
            log_group_name=example_log_group.name)
        ```

        ## Import

        Directory Service Log Subscriptions can be imported using the directory id, e.g.,

        ```sh
         $ pulumi import aws:directoryservice/logService:LogService msad d-1234567890
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[str] log_group_name: Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LogServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Log subscription for AWS Directory Service that pushes logs to cloudwatch.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_log_group = aws.cloudwatch.LogGroup("exampleLogGroup", retention_in_days=14)
        ad_log_policy_policy_document = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            actions=[
                "logs:CreateLogStream",
                "logs:PutLogEvents",
            ],
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                identifiers=["ds.amazonaws.com"],
                type="Service",
            )],
            resources=[example_log_group.arn.apply(lambda arn: f"{arn}:*")],
            effect="Allow",
        )])
        ad_log_policy_log_resource_policy = aws.cloudwatch.LogResourcePolicy("ad-log-policyLogResourcePolicy",
            policy_document=ad_log_policy_policy_document.json,
            policy_name="ad-log-policy")
        example_log_service = aws.directoryservice.LogService("exampleLogService",
            directory_id=aws_directory_service_directory["example"]["id"],
            log_group_name=example_log_group.name)
        ```

        ## Import

        Directory Service Log Subscriptions can be imported using the directory id, e.g.,

        ```sh
         $ pulumi import aws:directoryservice/logService:LogService msad d-1234567890
        ```

        :param str resource_name: The name of the resource.
        :param LogServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogServiceArgs.__new__(LogServiceArgs)

            if directory_id is None and not opts.urn:
                raise TypeError("Missing required property 'directory_id'")
            __props__.__dict__["directory_id"] = directory_id
            if log_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'log_group_name'")
            __props__.__dict__["log_group_name"] = log_group_name
        super(LogService, __self__).__init__(
            'aws:directoryservice/logService:LogService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            directory_id: Optional[pulumi.Input[str]] = None,
            log_group_name: Optional[pulumi.Input[str]] = None) -> 'LogService':
        """
        Get an existing LogService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[str] log_group_name: Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogServiceState.__new__(_LogServiceState)

        __props__.__dict__["directory_id"] = directory_id
        __props__.__dict__["log_group_name"] = log_group_name
        return LogService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Output[str]:
        """
        The id of directory.
        """
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Output[str]:
        """
        Name of the cloudwatch log group to which the logs should be published. The log group should be already created and the directory service principal should be provided with required permission to create stream and publish logs. Changing this value would delete the current subscription and create a new one. A directory can only have one log subscription at a time.
        """
        return pulumi.get(self, "log_group_name")

