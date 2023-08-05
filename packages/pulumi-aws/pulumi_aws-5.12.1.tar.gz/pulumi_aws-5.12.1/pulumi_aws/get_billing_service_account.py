# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetBillingServiceAccountResult',
    'AwaitableGetBillingServiceAccountResult',
    'get_billing_service_account',
]

@pulumi.output_type
class GetBillingServiceAccountResult:
    """
    A collection of values returned by getBillingServiceAccount.
    """
    def __init__(__self__, arn=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the AWS billing service account.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetBillingServiceAccountResult(GetBillingServiceAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBillingServiceAccountResult(
            arn=self.arn,
            id=self.id)


def get_billing_service_account(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBillingServiceAccountResult:
    """
    Use this data source to get the Account ID of the [AWS Billing and Cost Management Service Account](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-getting-started.html#step-2) for the purpose of permitting in S3 bucket policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    main = aws.get_billing_service_account()
    billing_logs = aws.s3.BucketV2("billingLogs")
    billing_logs_acl = aws.s3.BucketAclV2("billingLogsAcl",
        bucket=billing_logs.id,
        acl="private")
    allow_billing_logging = aws.s3.BucketPolicy("allowBillingLogging",
        bucket=billing_logs.id,
        policy=f\"\"\"{{
      "Id": "Policy",
      "Version": "2012-10-17",
      "Statement": [
        {{
          "Action": [
            "s3:GetBucketAcl", "s3:GetBucketPolicy"
          ],
          "Effect": "Allow",
          "Resource": "arn:aws:s3:::my-billing-tf-test-bucket",
          "Principal": {{
            "AWS": [
              "{main.arn}"
            ]
          }}
        }},
        {{
          "Action": [
            "s3:PutObject"
          ],
          "Effect": "Allow",
          "Resource": "arn:aws:s3:::my-billing-tf-test-bucket/*",
          "Principal": {{
            "AWS": [
              "{main.arn}"
            ]
          }}
        }}
      ]
    }}
    \"\"\")
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:index/getBillingServiceAccount:getBillingServiceAccount', __args__, opts=opts, typ=GetBillingServiceAccountResult).value

    return AwaitableGetBillingServiceAccountResult(
        arn=__ret__.arn,
        id=__ret__.id)
