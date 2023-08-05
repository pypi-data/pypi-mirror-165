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
    'GetReportDefinitionResult',
    'AwaitableGetReportDefinitionResult',
    'get_report_definition',
    'get_report_definition_output',
]

@pulumi.output_type
class GetReportDefinitionResult:
    """
    A collection of values returned by getReportDefinition.
    """
    def __init__(__self__, additional_artifacts=None, additional_schema_elements=None, compression=None, format=None, id=None, refresh_closed_reports=None, report_name=None, report_versioning=None, s3_bucket=None, s3_prefix=None, s3_region=None, time_unit=None):
        if additional_artifacts and not isinstance(additional_artifacts, list):
            raise TypeError("Expected argument 'additional_artifacts' to be a list")
        pulumi.set(__self__, "additional_artifacts", additional_artifacts)
        if additional_schema_elements and not isinstance(additional_schema_elements, list):
            raise TypeError("Expected argument 'additional_schema_elements' to be a list")
        pulumi.set(__self__, "additional_schema_elements", additional_schema_elements)
        if compression and not isinstance(compression, str):
            raise TypeError("Expected argument 'compression' to be a str")
        pulumi.set(__self__, "compression", compression)
        if format and not isinstance(format, str):
            raise TypeError("Expected argument 'format' to be a str")
        pulumi.set(__self__, "format", format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if refresh_closed_reports and not isinstance(refresh_closed_reports, bool):
            raise TypeError("Expected argument 'refresh_closed_reports' to be a bool")
        pulumi.set(__self__, "refresh_closed_reports", refresh_closed_reports)
        if report_name and not isinstance(report_name, str):
            raise TypeError("Expected argument 'report_name' to be a str")
        pulumi.set(__self__, "report_name", report_name)
        if report_versioning and not isinstance(report_versioning, str):
            raise TypeError("Expected argument 'report_versioning' to be a str")
        pulumi.set(__self__, "report_versioning", report_versioning)
        if s3_bucket and not isinstance(s3_bucket, str):
            raise TypeError("Expected argument 's3_bucket' to be a str")
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        if s3_prefix and not isinstance(s3_prefix, str):
            raise TypeError("Expected argument 's3_prefix' to be a str")
        pulumi.set(__self__, "s3_prefix", s3_prefix)
        if s3_region and not isinstance(s3_region, str):
            raise TypeError("Expected argument 's3_region' to be a str")
        pulumi.set(__self__, "s3_region", s3_region)
        if time_unit and not isinstance(time_unit, str):
            raise TypeError("Expected argument 'time_unit' to be a str")
        pulumi.set(__self__, "time_unit", time_unit)

    @property
    @pulumi.getter(name="additionalArtifacts")
    def additional_artifacts(self) -> Sequence[str]:
        """
        A list of additional artifacts.
        """
        return pulumi.get(self, "additional_artifacts")

    @property
    @pulumi.getter(name="additionalSchemaElements")
    def additional_schema_elements(self) -> Sequence[str]:
        """
        A list of schema elements.
        """
        return pulumi.get(self, "additional_schema_elements")

    @property
    @pulumi.getter
    def compression(self) -> str:
        """
        Preferred format for report.
        """
        return pulumi.get(self, "compression")

    @property
    @pulumi.getter
    def format(self) -> str:
        """
        Preferred compression format for report.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="refreshClosedReports")
    def refresh_closed_reports(self) -> bool:
        """
        If true reports are updated after they have been finalized.
        """
        return pulumi.get(self, "refresh_closed_reports")

    @property
    @pulumi.getter(name="reportName")
    def report_name(self) -> str:
        return pulumi.get(self, "report_name")

    @property
    @pulumi.getter(name="reportVersioning")
    def report_versioning(self) -> str:
        """
        Overwrite the previous version of each report or to deliver the report in addition to the previous versions.
        """
        return pulumi.get(self, "report_versioning")

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> str:
        """
        Name of customer S3 bucket.
        """
        return pulumi.get(self, "s3_bucket")

    @property
    @pulumi.getter(name="s3Prefix")
    def s3_prefix(self) -> str:
        """
        Preferred report path prefix.
        """
        return pulumi.get(self, "s3_prefix")

    @property
    @pulumi.getter(name="s3Region")
    def s3_region(self) -> str:
        """
        Region of customer S3 bucket.
        """
        return pulumi.get(self, "s3_region")

    @property
    @pulumi.getter(name="timeUnit")
    def time_unit(self) -> str:
        """
        The frequency on which report data are measured and displayed.
        """
        return pulumi.get(self, "time_unit")


class AwaitableGetReportDefinitionResult(GetReportDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReportDefinitionResult(
            additional_artifacts=self.additional_artifacts,
            additional_schema_elements=self.additional_schema_elements,
            compression=self.compression,
            format=self.format,
            id=self.id,
            refresh_closed_reports=self.refresh_closed_reports,
            report_name=self.report_name,
            report_versioning=self.report_versioning,
            s3_bucket=self.s3_bucket,
            s3_prefix=self.s3_prefix,
            s3_region=self.s3_region,
            time_unit=self.time_unit)


def get_report_definition(report_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReportDefinitionResult:
    """
    Use this data source to get information on an AWS Cost and Usage Report Definition.

    > *NOTE:* The AWS Cost and Usage Report service is only available in `us-east-1` currently.

    > *NOTE:* If AWS Organizations is enabled, only the master account can use this resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    report_definition = aws.cur.get_report_definition(report_name="example")
    ```


    :param str report_name: The name of the report definition to match.
    """
    __args__ = dict()
    __args__['reportName'] = report_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cur/getReportDefinition:getReportDefinition', __args__, opts=opts, typ=GetReportDefinitionResult).value

    return AwaitableGetReportDefinitionResult(
        additional_artifacts=__ret__.additional_artifacts,
        additional_schema_elements=__ret__.additional_schema_elements,
        compression=__ret__.compression,
        format=__ret__.format,
        id=__ret__.id,
        refresh_closed_reports=__ret__.refresh_closed_reports,
        report_name=__ret__.report_name,
        report_versioning=__ret__.report_versioning,
        s3_bucket=__ret__.s3_bucket,
        s3_prefix=__ret__.s3_prefix,
        s3_region=__ret__.s3_region,
        time_unit=__ret__.time_unit)


@_utilities.lift_output_func(get_report_definition)
def get_report_definition_output(report_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetReportDefinitionResult]:
    """
    Use this data source to get information on an AWS Cost and Usage Report Definition.

    > *NOTE:* The AWS Cost and Usage Report service is only available in `us-east-1` currently.

    > *NOTE:* If AWS Organizations is enabled, only the master account can use this resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    report_definition = aws.cur.get_report_definition(report_name="example")
    ```


    :param str report_name: The name of the report definition to match.
    """
    ...
