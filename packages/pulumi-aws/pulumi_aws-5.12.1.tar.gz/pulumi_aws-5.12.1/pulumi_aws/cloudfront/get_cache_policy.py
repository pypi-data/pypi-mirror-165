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

__all__ = [
    'GetCachePolicyResult',
    'AwaitableGetCachePolicyResult',
    'get_cache_policy',
    'get_cache_policy_output',
]

@pulumi.output_type
class GetCachePolicyResult:
    """
    A collection of values returned by getCachePolicy.
    """
    def __init__(__self__, comment=None, default_ttl=None, etag=None, id=None, max_ttl=None, min_ttl=None, name=None, parameters_in_cache_key_and_forwarded_to_origins=None):
        if comment and not isinstance(comment, str):
            raise TypeError("Expected argument 'comment' to be a str")
        pulumi.set(__self__, "comment", comment)
        if default_ttl and not isinstance(default_ttl, int):
            raise TypeError("Expected argument 'default_ttl' to be a int")
        pulumi.set(__self__, "default_ttl", default_ttl)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if max_ttl and not isinstance(max_ttl, int):
            raise TypeError("Expected argument 'max_ttl' to be a int")
        pulumi.set(__self__, "max_ttl", max_ttl)
        if min_ttl and not isinstance(min_ttl, int):
            raise TypeError("Expected argument 'min_ttl' to be a int")
        pulumi.set(__self__, "min_ttl", min_ttl)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters_in_cache_key_and_forwarded_to_origins and not isinstance(parameters_in_cache_key_and_forwarded_to_origins, list):
            raise TypeError("Expected argument 'parameters_in_cache_key_and_forwarded_to_origins' to be a list")
        pulumi.set(__self__, "parameters_in_cache_key_and_forwarded_to_origins", parameters_in_cache_key_and_forwarded_to_origins)

    @property
    @pulumi.getter
    def comment(self) -> str:
        """
        A comment to describe the cache policy.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> int:
        """
        The default amount of time, in seconds, that you want objects to stay in the CloudFront cache before CloudFront sends another request to the origin to see if the object has been updated.
        """
        return pulumi.get(self, "default_ttl")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        The current version of the cache policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> int:
        """
        The maximum amount of time, in seconds, that objects stay in the CloudFront cache before CloudFront sends another request to the origin to see if the object has been updated.
        """
        return pulumi.get(self, "max_ttl")

    @property
    @pulumi.getter(name="minTtl")
    def min_ttl(self) -> int:
        """
        The minimum amount of time, in seconds, that you want objects to stay in the CloudFront cache before CloudFront sends another request to the origin to see if the object has been updated.
        """
        return pulumi.get(self, "min_ttl")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parametersInCacheKeyAndForwardedToOrigins")
    def parameters_in_cache_key_and_forwarded_to_origins(self) -> Sequence['outputs.GetCachePolicyParametersInCacheKeyAndForwardedToOriginResult']:
        """
        The HTTP headers, cookies, and URL query strings to include in the cache key. See Parameters In Cache Key And Forwarded To Origin for more information.
        """
        return pulumi.get(self, "parameters_in_cache_key_and_forwarded_to_origins")


class AwaitableGetCachePolicyResult(GetCachePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCachePolicyResult(
            comment=self.comment,
            default_ttl=self.default_ttl,
            etag=self.etag,
            id=self.id,
            max_ttl=self.max_ttl,
            min_ttl=self.min_ttl,
            name=self.name,
            parameters_in_cache_key_and_forwarded_to_origins=self.parameters_in_cache_key_and_forwarded_to_origins)


def get_cache_policy(id: Optional[str] = None,
                     name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCachePolicyResult:
    """
    Use this data source to retrieve information about a CloudFront cache policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudfront.get_cache_policy(name="example-policy")
    ```


    :param str id: The identifier for the cache policy.
    :param str name: A unique name to identify the cache policy.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudfront/getCachePolicy:getCachePolicy', __args__, opts=opts, typ=GetCachePolicyResult).value

    return AwaitableGetCachePolicyResult(
        comment=__ret__.comment,
        default_ttl=__ret__.default_ttl,
        etag=__ret__.etag,
        id=__ret__.id,
        max_ttl=__ret__.max_ttl,
        min_ttl=__ret__.min_ttl,
        name=__ret__.name,
        parameters_in_cache_key_and_forwarded_to_origins=__ret__.parameters_in_cache_key_and_forwarded_to_origins)


@_utilities.lift_output_func(get_cache_policy)
def get_cache_policy_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                            name: Optional[pulumi.Input[Optional[str]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCachePolicyResult]:
    """
    Use this data source to retrieve information about a CloudFront cache policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudfront.get_cache_policy(name="example-policy")
    ```


    :param str id: The identifier for the cache policy.
    :param str name: A unique name to identify the cache policy.
    """
    ...
