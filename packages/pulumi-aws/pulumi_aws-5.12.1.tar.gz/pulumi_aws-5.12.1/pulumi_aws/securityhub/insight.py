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

__all__ = ['InsightArgs', 'Insight']

@pulumi.input_type
class InsightArgs:
    def __init__(__self__, *,
                 filters: pulumi.Input['InsightFiltersArgs'],
                 group_by_attribute: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Insight resource.
        :param pulumi.Input['InsightFiltersArgs'] filters: A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        :param pulumi.Input[str] group_by_attribute: The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        :param pulumi.Input[str] name: The name of the custom insight.
        """
        pulumi.set(__self__, "filters", filters)
        pulumi.set(__self__, "group_by_attribute", group_by_attribute)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Input['InsightFiltersArgs']:
        """
        A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: pulumi.Input['InsightFiltersArgs']):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter(name="groupByAttribute")
    def group_by_attribute(self) -> pulumi.Input[str]:
        """
        The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        """
        return pulumi.get(self, "group_by_attribute")

    @group_by_attribute.setter
    def group_by_attribute(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_by_attribute", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the custom insight.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _InsightState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 filters: Optional[pulumi.Input['InsightFiltersArgs']] = None,
                 group_by_attribute: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Insight resources.
        :param pulumi.Input[str] arn: ARN of the insight.
        :param pulumi.Input['InsightFiltersArgs'] filters: A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        :param pulumi.Input[str] group_by_attribute: The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        :param pulumi.Input[str] name: The name of the custom insight.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if group_by_attribute is not None:
            pulumi.set(__self__, "group_by_attribute", group_by_attribute)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the insight.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input['InsightFiltersArgs']]:
        """
        A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: Optional[pulumi.Input['InsightFiltersArgs']]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter(name="groupByAttribute")
    def group_by_attribute(self) -> Optional[pulumi.Input[str]]:
        """
        The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        """
        return pulumi.get(self, "group_by_attribute")

    @group_by_attribute.setter
    def group_by_attribute(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_by_attribute", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the custom insight.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class Insight(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filters: Optional[pulumi.Input[pulumi.InputType['InsightFiltersArgs']]] = None,
                 group_by_attribute: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Security Hub custom insight resource. See the [Managing custom insights section](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-custom-insights.html) of the AWS User Guide for more information.

        ## Example Usage
        ### Filter by AWS account ID

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                aws_account_ids=[
                    aws.securityhub.InsightFiltersAwsAccountIdArgs(
                        comparison="EQUALS",
                        value="1234567890",
                    ),
                    aws.securityhub.InsightFiltersAwsAccountIdArgs(
                        comparison="EQUALS",
                        value="09876543210",
                    ),
                ],
            ),
            group_by_attribute="AwsAccountId",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by date range

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                created_ats=[aws.securityhub.InsightFiltersCreatedAtArgs(
                    date_range=aws.securityhub.InsightFiltersCreatedAtDateRangeArgs(
                        unit="DAYS",
                        value=5,
                    ),
                )],
            ),
            group_by_attribute="CreatedAt",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by destination IPv4 address

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                network_destination_ipv4s=[aws.securityhub.InsightFiltersNetworkDestinationIpv4Args(
                    cidr="10.0.0.0/16",
                )],
            ),
            group_by_attribute="NetworkDestinationIpV4",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by finding's confidence

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                confidences=[aws.securityhub.InsightFiltersConfidenceArgs(
                    gte="80",
                )],
            ),
            group_by_attribute="Confidence",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by resource tags

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                resource_tags=[aws.securityhub.InsightFiltersResourceTagArgs(
                    comparison="EQUALS",
                    key="Environment",
                    value="Production",
                )],
            ),
            group_by_attribute="ResourceTags",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```

        ## Import

        Security Hub insights can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:securityhub/insight:Insight example arn:aws:securityhub:us-west-2:1234567890:insight/1234567890/custom/91299ed7-abd0-4e44-a858-d0b15e37141a
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['InsightFiltersArgs']] filters: A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        :param pulumi.Input[str] group_by_attribute: The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        :param pulumi.Input[str] name: The name of the custom insight.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InsightArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Security Hub custom insight resource. See the [Managing custom insights section](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-custom-insights.html) of the AWS User Guide for more information.

        ## Example Usage
        ### Filter by AWS account ID

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                aws_account_ids=[
                    aws.securityhub.InsightFiltersAwsAccountIdArgs(
                        comparison="EQUALS",
                        value="1234567890",
                    ),
                    aws.securityhub.InsightFiltersAwsAccountIdArgs(
                        comparison="EQUALS",
                        value="09876543210",
                    ),
                ],
            ),
            group_by_attribute="AwsAccountId",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by date range

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                created_ats=[aws.securityhub.InsightFiltersCreatedAtArgs(
                    date_range=aws.securityhub.InsightFiltersCreatedAtDateRangeArgs(
                        unit="DAYS",
                        value=5,
                    ),
                )],
            ),
            group_by_attribute="CreatedAt",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by destination IPv4 address

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                network_destination_ipv4s=[aws.securityhub.InsightFiltersNetworkDestinationIpv4Args(
                    cidr="10.0.0.0/16",
                )],
            ),
            group_by_attribute="NetworkDestinationIpV4",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by finding's confidence

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                confidences=[aws.securityhub.InsightFiltersConfidenceArgs(
                    gte="80",
                )],
            ),
            group_by_attribute="Confidence",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```
        ### Filter by resource tags

        ```python
        import pulumi
        import pulumi_aws as aws

        example_account = aws.securityhub.Account("exampleAccount")
        example_insight = aws.securityhub.Insight("exampleInsight",
            filters=aws.securityhub.InsightFiltersArgs(
                resource_tags=[aws.securityhub.InsightFiltersResourceTagArgs(
                    comparison="EQUALS",
                    key="Environment",
                    value="Production",
                )],
            ),
            group_by_attribute="ResourceTags",
            opts=pulumi.ResourceOptions(depends_on=[example_account]))
        ```

        ## Import

        Security Hub insights can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:securityhub/insight:Insight example arn:aws:securityhub:us-west-2:1234567890:insight/1234567890/custom/91299ed7-abd0-4e44-a858-d0b15e37141a
        ```

        :param str resource_name: The name of the resource.
        :param InsightArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InsightArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filters: Optional[pulumi.Input[pulumi.InputType['InsightFiltersArgs']]] = None,
                 group_by_attribute: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InsightArgs.__new__(InsightArgs)

            if filters is None and not opts.urn:
                raise TypeError("Missing required property 'filters'")
            __props__.__dict__["filters"] = filters
            if group_by_attribute is None and not opts.urn:
                raise TypeError("Missing required property 'group_by_attribute'")
            __props__.__dict__["group_by_attribute"] = group_by_attribute
            __props__.__dict__["name"] = name
            __props__.__dict__["arn"] = None
        super(Insight, __self__).__init__(
            'aws:securityhub/insight:Insight',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            filters: Optional[pulumi.Input[pulumi.InputType['InsightFiltersArgs']]] = None,
            group_by_attribute: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'Insight':
        """
        Get an existing Insight resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the insight.
        :param pulumi.Input[pulumi.InputType['InsightFiltersArgs']] filters: A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        :param pulumi.Input[str] group_by_attribute: The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        :param pulumi.Input[str] name: The name of the custom insight.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InsightState.__new__(_InsightState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["filters"] = filters
        __props__.__dict__["group_by_attribute"] = group_by_attribute
        __props__.__dict__["name"] = name
        return Insight(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the insight.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Output['outputs.InsightFilters']:
        """
        A configuration block including one or more (up to 10 distinct) attributes used to filter the findings included in the insight. The insight only includes findings that match criteria defined in the filters. See filters below for more details.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="groupByAttribute")
    def group_by_attribute(self) -> pulumi.Output[str]:
        """
        The attribute used to group the findings for the insight e.g., if an insight is grouped by `ResourceId`, then the insight produces a list of resource identifiers.
        """
        return pulumi.get(self, "group_by_attribute")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the custom insight.
        """
        return pulumi.get(self, "name")

