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

__all__ = ['BucketLifecycleConfigurationV2Args', 'BucketLifecycleConfigurationV2']

@pulumi.input_type
class BucketLifecycleConfigurationV2Args:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 rules: pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]],
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BucketLifecycleConfigurationV2 resource.
        :param pulumi.Input[str] bucket: The name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]] rules: List of configuration blocks describing the rules managing the replication documented below.
        :param pulumi.Input[str] expected_bucket_owner: The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "rules", rules)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        The name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]:
        """
        List of configuration blocks describing the rules managing the replication documented below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)


@pulumi.input_type
class _BucketLifecycleConfigurationV2State:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]] = None):
        """
        Input properties used for looking up and filtering BucketLifecycleConfigurationV2 resources.
        :param pulumi.Input[str] bucket: The name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]] rules: List of configuration blocks describing the rules managing the replication documented below.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]]:
        """
        List of configuration blocks describing the rules managing the replication documented below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]]):
        pulumi.set(self, "rules", value)


class BucketLifecycleConfigurationV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None,
                 __props__=None):
        """
        ## Import

        S3 bucket lifecycle configuration can be imported in one of two ways. If the owner (account ID) of the source bucket is the same account used to configure the Terraform AWS Provider, the S3 bucket lifecycle configuration resource should be imported using the `bucket` e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name
        ```

         If the owner (account ID) of the source bucket differs from the account used to configure the Terraform AWS Provider, the S3 bucket lifecycle configuration resource should be imported using the `bucket` and `expected_bucket_owner` separated by a comma (`,`) e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketLifecycleConfigurationV2Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        S3 bucket lifecycle configuration can be imported in one of two ways. If the owner (account ID) of the source bucket is the same account used to configure the Terraform AWS Provider, the S3 bucket lifecycle configuration resource should be imported using the `bucket` e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name
        ```

         If the owner (account ID) of the source bucket differs from the account used to configure the Terraform AWS Provider, the S3 bucket lifecycle configuration resource should be imported using the `bucket` and `expected_bucket_owner` separated by a comma (`,`) e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param BucketLifecycleConfigurationV2Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketLifecycleConfigurationV2Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketLifecycleConfigurationV2Args.__new__(BucketLifecycleConfigurationV2Args)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
        super(BucketLifecycleConfigurationV2, __self__).__init__(
            'aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            expected_bucket_owner: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None) -> 'BucketLifecycleConfigurationV2':
        """
        Get an existing BucketLifecycleConfigurationV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketLifecycleConfigurationV2State.__new__(_BucketLifecycleConfigurationV2State)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
        __props__.__dict__["rules"] = rules
        return BucketLifecycleConfigurationV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        The name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> pulumi.Output[Optional[str]]:
        """
        The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Sequence['outputs.BucketLifecycleConfigurationV2Rule']]:
        """
        List of configuration blocks describing the rules managing the replication documented below.
        """
        return pulumi.get(self, "rules")

