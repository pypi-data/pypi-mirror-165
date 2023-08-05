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
    'GetCanonicalUserIdResult',
    'AwaitableGetCanonicalUserIdResult',
    'get_canonical_user_id',
]

warnings.warn("""aws.getCanonicalUserId has been deprecated in favor of aws.s3.getCanonicalUserId""", DeprecationWarning)

@pulumi.output_type
class GetCanonicalUserIdResult:
    """
    A collection of values returned by getCanonicalUserId.
    """
    def __init__(__self__, display_name=None, id=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The human-friendly name linked to the canonical user ID. The bucket owner's display name. **NOTE:** [This value](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTServiceGET.html) is only included in the response in the US East (N. Virginia), US West (N. California), US West (Oregon), Asia Pacific (Singapore), Asia Pacific (Sydney), Asia Pacific (Tokyo), EU (Ireland), and South America (São Paulo) regions.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetCanonicalUserIdResult(GetCanonicalUserIdResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCanonicalUserIdResult(
            display_name=self.display_name,
            id=self.id)


def get_canonical_user_id(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCanonicalUserIdResult:
    """
    The Canonical User ID data source allows access to the [canonical user ID](http://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html)
    for the effective account in which this provider is working.

    > **NOTE:** To use this data source, you must have the `s3:ListAllMyBuckets` permission.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.s3.get_canonical_user_id()
    pulumi.export("canonicalUserId", current.id)
    ```
    """
    pulumi.log.warn("""get_canonical_user_id is deprecated: aws.getCanonicalUserId has been deprecated in favor of aws.s3.getCanonicalUserId""")
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:index/getCanonicalUserId:getCanonicalUserId', __args__, opts=opts, typ=GetCanonicalUserIdResult).value

    return AwaitableGetCanonicalUserIdResult(
        display_name=__ret__.display_name,
        id=__ret__.id)
