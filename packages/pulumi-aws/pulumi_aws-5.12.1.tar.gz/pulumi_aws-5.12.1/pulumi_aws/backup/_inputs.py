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
    'FrameworkControlArgs',
    'FrameworkControlInputParameterArgs',
    'FrameworkControlScopeArgs',
    'PlanAdvancedBackupSettingArgs',
    'PlanRuleArgs',
    'PlanRuleCopyActionArgs',
    'PlanRuleCopyActionLifecycleArgs',
    'PlanRuleLifecycleArgs',
    'ReportPlanReportDeliveryChannelArgs',
    'ReportPlanReportSettingArgs',
    'SelectionConditionArgs',
    'SelectionConditionStringEqualArgs',
    'SelectionConditionStringLikeArgs',
    'SelectionConditionStringNotEqualArgs',
    'SelectionConditionStringNotLikeArgs',
    'SelectionSelectionTagArgs',
]

@pulumi.input_type
class FrameworkControlArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 input_parameters: Optional[pulumi.Input[Sequence[pulumi.Input['FrameworkControlInputParameterArgs']]]] = None,
                 scope: Optional[pulumi.Input['FrameworkControlScopeArgs']] = None):
        """
        :param pulumi.Input[str] name: The name of a parameter, for example, BackupPlanFrequency.
        :param pulumi.Input[Sequence[pulumi.Input['FrameworkControlInputParameterArgs']]] input_parameters: One or more input parameter blocks. An example of a control with two parameters is: "backup plan frequency is at least daily and the retention period is at least 1 year". The first parameter is daily. The second parameter is 1 year. Detailed below.
        :param pulumi.Input['FrameworkControlScopeArgs'] scope: The scope of a control. The control scope defines what the control will evaluate. Three examples of control scopes are: a specific backup plan, all backup plans with a specific tag, or all backup plans. Detailed below.
        """
        pulumi.set(__self__, "name", name)
        if input_parameters is not None:
            pulumi.set(__self__, "input_parameters", input_parameters)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of a parameter, for example, BackupPlanFrequency.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="inputParameters")
    def input_parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FrameworkControlInputParameterArgs']]]]:
        """
        One or more input parameter blocks. An example of a control with two parameters is: "backup plan frequency is at least daily and the retention period is at least 1 year". The first parameter is daily. The second parameter is 1 year. Detailed below.
        """
        return pulumi.get(self, "input_parameters")

    @input_parameters.setter
    def input_parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FrameworkControlInputParameterArgs']]]]):
        pulumi.set(self, "input_parameters", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['FrameworkControlScopeArgs']]:
        """
        The scope of a control. The control scope defines what the control will evaluate. Three examples of control scopes are: a specific backup plan, all backup plans with a specific tag, or all backup plans. Detailed below.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['FrameworkControlScopeArgs']]):
        pulumi.set(self, "scope", value)


@pulumi.input_type
class FrameworkControlInputParameterArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of a parameter, for example, BackupPlanFrequency.
        :param pulumi.Input[str] value: The value of parameter, for example, hourly.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of a parameter, for example, BackupPlanFrequency.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of parameter, for example, hourly.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class FrameworkControlScopeArgs:
    def __init__(__self__, *,
                 compliance_resource_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 compliance_resource_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] compliance_resource_ids: The ID of the only AWS resource that you want your control scope to contain. Minimum number of 1 item. Maximum number of 100 items.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] compliance_resource_types: Describes whether the control scope includes one or more types of resources, such as EFS or RDS.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tag key-value pair applied to those AWS resources that you want to trigger an evaluation for a rule. A maximum of one key-value pair can be provided.
        """
        if compliance_resource_ids is not None:
            pulumi.set(__self__, "compliance_resource_ids", compliance_resource_ids)
        if compliance_resource_types is not None:
            pulumi.set(__self__, "compliance_resource_types", compliance_resource_types)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="complianceResourceIds")
    def compliance_resource_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The ID of the only AWS resource that you want your control scope to contain. Minimum number of 1 item. Maximum number of 100 items.
        """
        return pulumi.get(self, "compliance_resource_ids")

    @compliance_resource_ids.setter
    def compliance_resource_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "compliance_resource_ids", value)

    @property
    @pulumi.getter(name="complianceResourceTypes")
    def compliance_resource_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Describes whether the control scope includes one or more types of resources, such as EFS or RDS.
        """
        return pulumi.get(self, "compliance_resource_types")

    @compliance_resource_types.setter
    def compliance_resource_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "compliance_resource_types", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tag key-value pair applied to those AWS resources that you want to trigger an evaluation for a rule. A maximum of one key-value pair can be provided.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class PlanAdvancedBackupSettingArgs:
    def __init__(__self__, *,
                 backup_options: pulumi.Input[Mapping[str, pulumi.Input[str]]],
                 resource_type: pulumi.Input[str]):
        """
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] backup_options: Specifies the backup option for a selected resource. This option is only available for Windows VSS backup jobs. Set to `{ WindowsVSS = "enabled" }` to enable Windows VSS backup option and create a VSS Windows backup.
        :param pulumi.Input[str] resource_type: The type of AWS resource to be backed up. For VSS Windows backups, the only supported resource type is Amazon EC2. Valid values: `EC2`.
        """
        pulumi.set(__self__, "backup_options", backup_options)
        pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter(name="backupOptions")
    def backup_options(self) -> pulumi.Input[Mapping[str, pulumi.Input[str]]]:
        """
        Specifies the backup option for a selected resource. This option is only available for Windows VSS backup jobs. Set to `{ WindowsVSS = "enabled" }` to enable Windows VSS backup option and create a VSS Windows backup.
        """
        return pulumi.get(self, "backup_options")

    @backup_options.setter
    def backup_options(self, value: pulumi.Input[Mapping[str, pulumi.Input[str]]]):
        pulumi.set(self, "backup_options", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        The type of AWS resource to be backed up. For VSS Windows backups, the only supported resource type is Amazon EC2. Valid values: `EC2`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)


@pulumi.input_type
class PlanRuleArgs:
    def __init__(__self__, *,
                 rule_name: pulumi.Input[str],
                 target_vault_name: pulumi.Input[str],
                 completion_window: Optional[pulumi.Input[int]] = None,
                 copy_actions: Optional[pulumi.Input[Sequence[pulumi.Input['PlanRuleCopyActionArgs']]]] = None,
                 enable_continuous_backup: Optional[pulumi.Input[bool]] = None,
                 lifecycle: Optional[pulumi.Input['PlanRuleLifecycleArgs']] = None,
                 recovery_point_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_window: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] rule_name: An display name for a backup rule.
        :param pulumi.Input[str] target_vault_name: The name of a logical container where backups are stored.
        :param pulumi.Input[int] completion_window: The amount of time in minutes AWS Backup attempts a backup before canceling the job and returning an error.
        :param pulumi.Input[Sequence[pulumi.Input['PlanRuleCopyActionArgs']]] copy_actions: Configuration block(s) with copy operation settings. Detailed below.
        :param pulumi.Input[bool] enable_continuous_backup: Enable continuous backups for supported resources.
        :param pulumi.Input['PlanRuleLifecycleArgs'] lifecycle: The lifecycle defines when a protected resource is copied over to a backup vault and when it expires.  Fields documented above.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] recovery_point_tags: Metadata that you can assign to help organize the resources that you create.
        :param pulumi.Input[str] schedule: A CRON expression specifying when AWS Backup initiates a backup job.
        :param pulumi.Input[int] start_window: The amount of time in minutes before beginning a backup.
        """
        pulumi.set(__self__, "rule_name", rule_name)
        pulumi.set(__self__, "target_vault_name", target_vault_name)
        if completion_window is not None:
            pulumi.set(__self__, "completion_window", completion_window)
        if copy_actions is not None:
            pulumi.set(__self__, "copy_actions", copy_actions)
        if enable_continuous_backup is not None:
            pulumi.set(__self__, "enable_continuous_backup", enable_continuous_backup)
        if lifecycle is not None:
            pulumi.set(__self__, "lifecycle", lifecycle)
        if recovery_point_tags is not None:
            pulumi.set(__self__, "recovery_point_tags", recovery_point_tags)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if start_window is not None:
            pulumi.set(__self__, "start_window", start_window)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Input[str]:
        """
        An display name for a backup rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="targetVaultName")
    def target_vault_name(self) -> pulumi.Input[str]:
        """
        The name of a logical container where backups are stored.
        """
        return pulumi.get(self, "target_vault_name")

    @target_vault_name.setter
    def target_vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_vault_name", value)

    @property
    @pulumi.getter(name="completionWindow")
    def completion_window(self) -> Optional[pulumi.Input[int]]:
        """
        The amount of time in minutes AWS Backup attempts a backup before canceling the job and returning an error.
        """
        return pulumi.get(self, "completion_window")

    @completion_window.setter
    def completion_window(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "completion_window", value)

    @property
    @pulumi.getter(name="copyActions")
    def copy_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PlanRuleCopyActionArgs']]]]:
        """
        Configuration block(s) with copy operation settings. Detailed below.
        """
        return pulumi.get(self, "copy_actions")

    @copy_actions.setter
    def copy_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PlanRuleCopyActionArgs']]]]):
        pulumi.set(self, "copy_actions", value)

    @property
    @pulumi.getter(name="enableContinuousBackup")
    def enable_continuous_backup(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable continuous backups for supported resources.
        """
        return pulumi.get(self, "enable_continuous_backup")

    @enable_continuous_backup.setter
    def enable_continuous_backup(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_continuous_backup", value)

    @property
    @pulumi.getter
    def lifecycle(self) -> Optional[pulumi.Input['PlanRuleLifecycleArgs']]:
        """
        The lifecycle defines when a protected resource is copied over to a backup vault and when it expires.  Fields documented above.
        """
        return pulumi.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: Optional[pulumi.Input['PlanRuleLifecycleArgs']]):
        pulumi.set(self, "lifecycle", value)

    @property
    @pulumi.getter(name="recoveryPointTags")
    def recovery_point_tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Metadata that you can assign to help organize the resources that you create.
        """
        return pulumi.get(self, "recovery_point_tags")

    @recovery_point_tags.setter
    def recovery_point_tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "recovery_point_tags", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        A CRON expression specifying when AWS Backup initiates a backup job.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="startWindow")
    def start_window(self) -> Optional[pulumi.Input[int]]:
        """
        The amount of time in minutes before beginning a backup.
        """
        return pulumi.get(self, "start_window")

    @start_window.setter
    def start_window(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_window", value)


@pulumi.input_type
class PlanRuleCopyActionArgs:
    def __init__(__self__, *,
                 destination_vault_arn: pulumi.Input[str],
                 lifecycle: Optional[pulumi.Input['PlanRuleCopyActionLifecycleArgs']] = None):
        """
        :param pulumi.Input[str] destination_vault_arn: An Amazon Resource Name (ARN) that uniquely identifies the destination backup vault for the copied backup.
        :param pulumi.Input['PlanRuleCopyActionLifecycleArgs'] lifecycle: The lifecycle defines when a protected resource is copied over to a backup vault and when it expires.  Fields documented above.
        """
        pulumi.set(__self__, "destination_vault_arn", destination_vault_arn)
        if lifecycle is not None:
            pulumi.set(__self__, "lifecycle", lifecycle)

    @property
    @pulumi.getter(name="destinationVaultArn")
    def destination_vault_arn(self) -> pulumi.Input[str]:
        """
        An Amazon Resource Name (ARN) that uniquely identifies the destination backup vault for the copied backup.
        """
        return pulumi.get(self, "destination_vault_arn")

    @destination_vault_arn.setter
    def destination_vault_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_vault_arn", value)

    @property
    @pulumi.getter
    def lifecycle(self) -> Optional[pulumi.Input['PlanRuleCopyActionLifecycleArgs']]:
        """
        The lifecycle defines when a protected resource is copied over to a backup vault and when it expires.  Fields documented above.
        """
        return pulumi.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: Optional[pulumi.Input['PlanRuleCopyActionLifecycleArgs']]):
        pulumi.set(self, "lifecycle", value)


@pulumi.input_type
class PlanRuleCopyActionLifecycleArgs:
    def __init__(__self__, *,
                 cold_storage_after: Optional[pulumi.Input[int]] = None,
                 delete_after: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] cold_storage_after: Specifies the number of days after creation that a recovery point is moved to cold storage.
        :param pulumi.Input[int] delete_after: Specifies the number of days after creation that a recovery point is deleted. Must be 90 days greater than `cold_storage_after`.
        """
        if cold_storage_after is not None:
            pulumi.set(__self__, "cold_storage_after", cold_storage_after)
        if delete_after is not None:
            pulumi.set(__self__, "delete_after", delete_after)

    @property
    @pulumi.getter(name="coldStorageAfter")
    def cold_storage_after(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days after creation that a recovery point is moved to cold storage.
        """
        return pulumi.get(self, "cold_storage_after")

    @cold_storage_after.setter
    def cold_storage_after(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cold_storage_after", value)

    @property
    @pulumi.getter(name="deleteAfter")
    def delete_after(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days after creation that a recovery point is deleted. Must be 90 days greater than `cold_storage_after`.
        """
        return pulumi.get(self, "delete_after")

    @delete_after.setter
    def delete_after(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "delete_after", value)


@pulumi.input_type
class PlanRuleLifecycleArgs:
    def __init__(__self__, *,
                 cold_storage_after: Optional[pulumi.Input[int]] = None,
                 delete_after: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] cold_storage_after: Specifies the number of days after creation that a recovery point is moved to cold storage.
        :param pulumi.Input[int] delete_after: Specifies the number of days after creation that a recovery point is deleted. Must be 90 days greater than `cold_storage_after`.
        """
        if cold_storage_after is not None:
            pulumi.set(__self__, "cold_storage_after", cold_storage_after)
        if delete_after is not None:
            pulumi.set(__self__, "delete_after", delete_after)

    @property
    @pulumi.getter(name="coldStorageAfter")
    def cold_storage_after(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days after creation that a recovery point is moved to cold storage.
        """
        return pulumi.get(self, "cold_storage_after")

    @cold_storage_after.setter
    def cold_storage_after(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cold_storage_after", value)

    @property
    @pulumi.getter(name="deleteAfter")
    def delete_after(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days after creation that a recovery point is deleted. Must be 90 days greater than `cold_storage_after`.
        """
        return pulumi.get(self, "delete_after")

    @delete_after.setter
    def delete_after(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "delete_after", value)


@pulumi.input_type
class ReportPlanReportDeliveryChannelArgs:
    def __init__(__self__, *,
                 s3_bucket_name: pulumi.Input[str],
                 formats: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] s3_bucket_name: The unique name of the S3 bucket that receives your reports.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] formats: A list of the format of your reports: CSV, JSON, or both. If not specified, the default format is CSV.
        :param pulumi.Input[str] s3_key_prefix: The prefix for where Backup Audit Manager delivers your reports to Amazon S3. The prefix is this part of the following path: s3://your-bucket-name/prefix/Backup/us-west-2/year/month/day/report-name. If not specified, there is no prefix.
        """
        pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)
        if formats is not None:
            pulumi.set(__self__, "formats", formats)
        if s3_key_prefix is not None:
            pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> pulumi.Input[str]:
        """
        The unique name of the S3 bucket that receives your reports.
        """
        return pulumi.get(self, "s3_bucket_name")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket_name", value)

    @property
    @pulumi.getter
    def formats(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of the format of your reports: CSV, JSON, or both. If not specified, the default format is CSV.
        """
        return pulumi.get(self, "formats")

    @formats.setter
    def formats(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "formats", value)

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix for where Backup Audit Manager delivers your reports to Amazon S3. The prefix is this part of the following path: s3://your-bucket-name/prefix/Backup/us-west-2/year/month/day/report-name. If not specified, there is no prefix.
        """
        return pulumi.get(self, "s3_key_prefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_key_prefix", value)


@pulumi.input_type
class ReportPlanReportSettingArgs:
    def __init__(__self__, *,
                 report_template: pulumi.Input[str],
                 framework_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 number_of_frameworks: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] report_template: Identifies the report template for the report. Reports are built using a report template. The report templates are: `RESOURCE_COMPLIANCE_REPORT` | `CONTROL_COMPLIANCE_REPORT` | `BACKUP_JOB_REPORT` | `COPY_JOB_REPORT` | `RESTORE_JOB_REPORT`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] framework_arns: Specifies the Amazon Resource Names (ARNs) of the frameworks a report covers.
        :param pulumi.Input[int] number_of_frameworks: Specifies the number of frameworks a report covers.
        """
        pulumi.set(__self__, "report_template", report_template)
        if framework_arns is not None:
            pulumi.set(__self__, "framework_arns", framework_arns)
        if number_of_frameworks is not None:
            pulumi.set(__self__, "number_of_frameworks", number_of_frameworks)

    @property
    @pulumi.getter(name="reportTemplate")
    def report_template(self) -> pulumi.Input[str]:
        """
        Identifies the report template for the report. Reports are built using a report template. The report templates are: `RESOURCE_COMPLIANCE_REPORT` | `CONTROL_COMPLIANCE_REPORT` | `BACKUP_JOB_REPORT` | `COPY_JOB_REPORT` | `RESTORE_JOB_REPORT`.
        """
        return pulumi.get(self, "report_template")

    @report_template.setter
    def report_template(self, value: pulumi.Input[str]):
        pulumi.set(self, "report_template", value)

    @property
    @pulumi.getter(name="frameworkArns")
    def framework_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the Amazon Resource Names (ARNs) of the frameworks a report covers.
        """
        return pulumi.get(self, "framework_arns")

    @framework_arns.setter
    def framework_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "framework_arns", value)

    @property
    @pulumi.getter(name="numberOfFrameworks")
    def number_of_frameworks(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of frameworks a report covers.
        """
        return pulumi.get(self, "number_of_frameworks")

    @number_of_frameworks.setter
    def number_of_frameworks(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_frameworks", value)


@pulumi.input_type
class SelectionConditionArgs:
    def __init__(__self__, *,
                 string_equals: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringEqualArgs']]]] = None,
                 string_likes: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringLikeArgs']]]] = None,
                 string_not_equals: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotEqualArgs']]]] = None,
                 string_not_likes: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotLikeArgs']]]] = None):
        if string_equals is not None:
            pulumi.set(__self__, "string_equals", string_equals)
        if string_likes is not None:
            pulumi.set(__self__, "string_likes", string_likes)
        if string_not_equals is not None:
            pulumi.set(__self__, "string_not_equals", string_not_equals)
        if string_not_likes is not None:
            pulumi.set(__self__, "string_not_likes", string_not_likes)

    @property
    @pulumi.getter(name="stringEquals")
    def string_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringEqualArgs']]]]:
        return pulumi.get(self, "string_equals")

    @string_equals.setter
    def string_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringEqualArgs']]]]):
        pulumi.set(self, "string_equals", value)

    @property
    @pulumi.getter(name="stringLikes")
    def string_likes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringLikeArgs']]]]:
        return pulumi.get(self, "string_likes")

    @string_likes.setter
    def string_likes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringLikeArgs']]]]):
        pulumi.set(self, "string_likes", value)

    @property
    @pulumi.getter(name="stringNotEquals")
    def string_not_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotEqualArgs']]]]:
        return pulumi.get(self, "string_not_equals")

    @string_not_equals.setter
    def string_not_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotEqualArgs']]]]):
        pulumi.set(self, "string_not_equals", value)

    @property
    @pulumi.getter(name="stringNotLikes")
    def string_not_likes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotLikeArgs']]]]:
        return pulumi.get(self, "string_not_likes")

    @string_not_likes.setter
    def string_not_likes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionStringNotLikeArgs']]]]):
        pulumi.set(self, "string_not_likes", value)


@pulumi.input_type
class SelectionConditionStringEqualArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The key in a key-value pair.
        :param pulumi.Input[str] value: The value in a key-value pair.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key in a key-value pair.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value in a key-value pair.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SelectionConditionStringLikeArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The key in a key-value pair.
        :param pulumi.Input[str] value: The value in a key-value pair.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key in a key-value pair.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value in a key-value pair.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SelectionConditionStringNotEqualArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The key in a key-value pair.
        :param pulumi.Input[str] value: The value in a key-value pair.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key in a key-value pair.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value in a key-value pair.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SelectionConditionStringNotLikeArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The key in a key-value pair.
        :param pulumi.Input[str] value: The value in a key-value pair.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key in a key-value pair.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value in a key-value pair.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SelectionSelectionTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The key in a key-value pair.
        :param pulumi.Input[str] type: An operation, such as `StringEquals`, that is applied to a key-value pair used to filter resources in a selection.
        :param pulumi.Input[str] value: The value in a key-value pair.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key in a key-value pair.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        An operation, such as `StringEquals`, that is applied to a key-value pair used to filter resources in a selection.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value in a key-value pair.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


