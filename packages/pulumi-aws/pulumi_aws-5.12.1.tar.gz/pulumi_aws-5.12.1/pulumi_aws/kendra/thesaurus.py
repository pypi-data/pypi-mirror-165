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

__all__ = ['ThesaurusArgs', 'Thesaurus']

@pulumi.input_type
class ThesaurusArgs:
    def __init__(__self__, *,
                 index_id: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 source_s3_path: pulumi.Input['ThesaurusSourceS3PathArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Thesaurus resource.
        :param pulumi.Input[str] index_id: The identifier of the index for a thesaurus.
        :param pulumi.Input[str] role_arn: The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        :param pulumi.Input['ThesaurusSourceS3PathArgs'] source_s3_path: The S3 path where your thesaurus file sits in S3. Detailed below.
        :param pulumi.Input[str] description: The description for a thesaurus.
        :param pulumi.Input[str] name: The name for the thesaurus.
        """
        pulumi.set(__self__, "index_id", index_id)
        pulumi.set(__self__, "role_arn", role_arn)
        pulumi.set(__self__, "source_s3_path", source_s3_path)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="indexId")
    def index_id(self) -> pulumi.Input[str]:
        """
        The identifier of the index for a thesaurus.
        """
        return pulumi.get(self, "index_id")

    @index_id.setter
    def index_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "index_id", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="sourceS3Path")
    def source_s3_path(self) -> pulumi.Input['ThesaurusSourceS3PathArgs']:
        """
        The S3 path where your thesaurus file sits in S3. Detailed below.
        """
        return pulumi.get(self, "source_s3_path")

    @source_s3_path.setter
    def source_s3_path(self, value: pulumi.Input['ThesaurusSourceS3PathArgs']):
        pulumi.set(self, "source_s3_path", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for a thesaurus.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the thesaurus.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ThesaurusState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 source_s3_path: Optional[pulumi.Input['ThesaurusSourceS3PathArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thesaurus_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Thesaurus resources.
        :param pulumi.Input[str] arn: ARN of the thesaurus.
        :param pulumi.Input[str] description: The description for a thesaurus.
        :param pulumi.Input[str] index_id: The identifier of the index for a thesaurus.
        :param pulumi.Input[str] name: The name for the thesaurus.
        :param pulumi.Input[str] role_arn: The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        :param pulumi.Input['ThesaurusSourceS3PathArgs'] source_s3_path: The S3 path where your thesaurus file sits in S3. Detailed below.
        :param pulumi.Input[str] status: The current status of the thesaurus.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if index_id is not None:
            pulumi.set(__self__, "index_id", index_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if source_s3_path is not None:
            pulumi.set(__self__, "source_s3_path", source_s3_path)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if thesaurus_id is not None:
            pulumi.set(__self__, "thesaurus_id", thesaurus_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the thesaurus.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for a thesaurus.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="indexId")
    def index_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the index for a thesaurus.
        """
        return pulumi.get(self, "index_id")

    @index_id.setter
    def index_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "index_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the thesaurus.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="sourceS3Path")
    def source_s3_path(self) -> Optional[pulumi.Input['ThesaurusSourceS3PathArgs']]:
        """
        The S3 path where your thesaurus file sits in S3. Detailed below.
        """
        return pulumi.get(self, "source_s3_path")

    @source_s3_path.setter
    def source_s3_path(self, value: Optional[pulumi.Input['ThesaurusSourceS3PathArgs']]):
        pulumi.set(self, "source_s3_path", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current status of the thesaurus.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="thesaurusId")
    def thesaurus_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "thesaurus_id")

    @thesaurus_id.setter
    def thesaurus_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thesaurus_id", value)


class Thesaurus(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 source_s3_path: Optional[pulumi.Input[pulumi.InputType['ThesaurusSourceS3PathArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.kendra.Thesaurus("example",
            index_id=aws_kendra_index["example"]["id"],
            role_arn=aws_iam_role["example"]["arn"],
            source_s3_path=aws.kendra.ThesaurusSourceS3PathArgs(
                bucket=aws_s3_bucket["example"]["id"],
                key=aws_s3_object["example"]["key"],
            ),
            tags={
                "Name": "Example Kendra Thesaurus",
            })
        ```

        ## Import

        `aws_kendra_thesaurus` can be imported using the unique identifiers of the thesaurus and index separated by a slash (`/`), e.g.,

        ```sh
         $ pulumi import aws:kendra/thesaurus:Thesaurus example thesaurus-123456780/idx-8012925589
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description for a thesaurus.
        :param pulumi.Input[str] index_id: The identifier of the index for a thesaurus.
        :param pulumi.Input[str] name: The name for the thesaurus.
        :param pulumi.Input[str] role_arn: The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        :param pulumi.Input[pulumi.InputType['ThesaurusSourceS3PathArgs']] source_s3_path: The S3 path where your thesaurus file sits in S3. Detailed below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ThesaurusArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.kendra.Thesaurus("example",
            index_id=aws_kendra_index["example"]["id"],
            role_arn=aws_iam_role["example"]["arn"],
            source_s3_path=aws.kendra.ThesaurusSourceS3PathArgs(
                bucket=aws_s3_bucket["example"]["id"],
                key=aws_s3_object["example"]["key"],
            ),
            tags={
                "Name": "Example Kendra Thesaurus",
            })
        ```

        ## Import

        `aws_kendra_thesaurus` can be imported using the unique identifiers of the thesaurus and index separated by a slash (`/`), e.g.,

        ```sh
         $ pulumi import aws:kendra/thesaurus:Thesaurus example thesaurus-123456780/idx-8012925589
        ```

        :param str resource_name: The name of the resource.
        :param ThesaurusArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ThesaurusArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 source_s3_path: Optional[pulumi.Input[pulumi.InputType['ThesaurusSourceS3PathArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ThesaurusArgs.__new__(ThesaurusArgs)

            __props__.__dict__["description"] = description
            if index_id is None and not opts.urn:
                raise TypeError("Missing required property 'index_id'")
            __props__.__dict__["index_id"] = index_id
            __props__.__dict__["name"] = name
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            if source_s3_path is None and not opts.urn:
                raise TypeError("Missing required property 'source_s3_path'")
            __props__.__dict__["source_s3_path"] = source_s3_path
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["thesaurus_id"] = None
        super(Thesaurus, __self__).__init__(
            'aws:kendra/thesaurus:Thesaurus',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            index_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            source_s3_path: Optional[pulumi.Input[pulumi.InputType['ThesaurusSourceS3PathArgs']]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            thesaurus_id: Optional[pulumi.Input[str]] = None) -> 'Thesaurus':
        """
        Get an existing Thesaurus resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the thesaurus.
        :param pulumi.Input[str] description: The description for a thesaurus.
        :param pulumi.Input[str] index_id: The identifier of the index for a thesaurus.
        :param pulumi.Input[str] name: The name for the thesaurus.
        :param pulumi.Input[str] role_arn: The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        :param pulumi.Input[pulumi.InputType['ThesaurusSourceS3PathArgs']] source_s3_path: The S3 path where your thesaurus file sits in S3. Detailed below.
        :param pulumi.Input[str] status: The current status of the thesaurus.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ThesaurusState.__new__(_ThesaurusState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["index_id"] = index_id
        __props__.__dict__["name"] = name
        __props__.__dict__["role_arn"] = role_arn
        __props__.__dict__["source_s3_path"] = source_s3_path
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["thesaurus_id"] = thesaurus_id
        return Thesaurus(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the thesaurus.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description for a thesaurus.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="indexId")
    def index_id(self) -> pulumi.Output[str]:
        """
        The identifier of the index for a thesaurus.
        """
        return pulumi.get(self, "index_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name for the thesaurus.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The IAM (Identity and Access Management) role used to access the thesaurus file in S3.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="sourceS3Path")
    def source_s3_path(self) -> pulumi.Output['outputs.ThesaurusSourceS3Path']:
        """
        The S3 path where your thesaurus file sits in S3. Detailed below.
        """
        return pulumi.get(self, "source_s3_path")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The current status of the thesaurus.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="thesaurusId")
    def thesaurus_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "thesaurus_id")

