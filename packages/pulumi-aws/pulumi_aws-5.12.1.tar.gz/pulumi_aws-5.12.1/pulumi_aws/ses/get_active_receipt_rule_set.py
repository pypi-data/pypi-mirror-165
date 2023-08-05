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
    'GetActiveReceiptRuleSetResult',
    'AwaitableGetActiveReceiptRuleSetResult',
    'get_active_receipt_rule_set',
]

@pulumi.output_type
class GetActiveReceiptRuleSetResult:
    """
    A collection of values returned by getActiveReceiptRuleSet.
    """
    def __init__(__self__, arn=None, id=None, rule_set_name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if rule_set_name and not isinstance(rule_set_name, str):
            raise TypeError("Expected argument 'rule_set_name' to be a str")
        pulumi.set(__self__, "rule_set_name", rule_set_name)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The SES receipt rule set ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ruleSetName")
    def rule_set_name(self) -> str:
        """
        The name of the rule set
        """
        return pulumi.get(self, "rule_set_name")


class AwaitableGetActiveReceiptRuleSetResult(GetActiveReceiptRuleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActiveReceiptRuleSetResult(
            arn=self.arn,
            id=self.id,
            rule_set_name=self.rule_set_name)


def get_active_receipt_rule_set(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActiveReceiptRuleSetResult:
    """
    Retrieve the active SES receipt rule set

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    main = aws.ses.get_active_receipt_rule_set()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ses/getActiveReceiptRuleSet:getActiveReceiptRuleSet', __args__, opts=opts, typ=GetActiveReceiptRuleSetResult).value

    return AwaitableGetActiveReceiptRuleSetResult(
        arn=__ret__.arn,
        id=__ret__.id,
        rule_set_name=__ret__.rule_set_name)
