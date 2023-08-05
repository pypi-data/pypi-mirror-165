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
    'GetThesaurusResult',
    'AwaitableGetThesaurusResult',
    'get_thesaurus',
    'get_thesaurus_output',
]

@pulumi.output_type
class GetThesaurusResult:
    """
    A collection of values returned by getThesaurus.
    """
    def __init__(__self__, arn=None, created_at=None, description=None, error_message=None, file_size_bytes=None, id=None, index_id=None, name=None, role_arn=None, source_s3_paths=None, status=None, synonym_rule_count=None, tags=None, term_count=None, thesaurus_id=None, updated_at=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if error_message and not isinstance(error_message, str):
            raise TypeError("Expected argument 'error_message' to be a str")
        pulumi.set(__self__, "error_message", error_message)
        if file_size_bytes and not isinstance(file_size_bytes, int):
            raise TypeError("Expected argument 'file_size_bytes' to be a int")
        pulumi.set(__self__, "file_size_bytes", file_size_bytes)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if index_id and not isinstance(index_id, str):
            raise TypeError("Expected argument 'index_id' to be a str")
        pulumi.set(__self__, "index_id", index_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if source_s3_paths and not isinstance(source_s3_paths, list):
            raise TypeError("Expected argument 'source_s3_paths' to be a list")
        pulumi.set(__self__, "source_s3_paths", source_s3_paths)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if synonym_rule_count and not isinstance(synonym_rule_count, int):
            raise TypeError("Expected argument 'synonym_rule_count' to be a int")
        pulumi.set(__self__, "synonym_rule_count", synonym_rule_count)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if term_count and not isinstance(term_count, int):
            raise TypeError("Expected argument 'term_count' to be a int")
        pulumi.set(__self__, "term_count", term_count)
        if thesaurus_id and not isinstance(thesaurus_id, str):
            raise TypeError("Expected argument 'thesaurus_id' to be a str")
        pulumi.set(__self__, "thesaurus_id", thesaurus_id)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the Thesaurus.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The Unix datetime that the Thesaurus was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the Thesaurus.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="errorMessage")
    def error_message(self) -> str:
        """
        When the `status` field value is `FAILED`, this contains a message that explains why.
        """
        return pulumi.get(self, "error_message")

    @property
    @pulumi.getter(name="fileSizeBytes")
    def file_size_bytes(self) -> int:
        """
        The size of the Thesaurus file in bytes.
        """
        return pulumi.get(self, "file_size_bytes")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="indexId")
    def index_id(self) -> str:
        return pulumi.get(self, "index_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the Thesaurus.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the Thesaurus. For more information, see [IAM Roles for Amazon Kendra](https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html).
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="sourceS3Paths")
    def source_s3_paths(self) -> Sequence['outputs.GetThesaurusSourceS3PathResult']:
        """
        The S3 location of the Thesaurus input data. Detailed below.
        """
        return pulumi.get(self, "source_s3_paths")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the Thesaurus. It is ready to use when the status is `ACTIVE`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="synonymRuleCount")
    def synonym_rule_count(self) -> int:
        """
        The number of synonym rules in the Thesaurus file.
        """
        return pulumi.get(self, "synonym_rule_count")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Metadata that helps organize the Thesaurus you create.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="termCount")
    def term_count(self) -> int:
        """
        The number of unique terms in the Thesaurus file. For example, the synonyms `a,b,c` and `a=>d`, the term count would be 4.
        """
        return pulumi.get(self, "term_count")

    @property
    @pulumi.getter(name="thesaurusId")
    def thesaurus_id(self) -> str:
        return pulumi.get(self, "thesaurus_id")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The date and time that the Thesaurus was last updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetThesaurusResult(GetThesaurusResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetThesaurusResult(
            arn=self.arn,
            created_at=self.created_at,
            description=self.description,
            error_message=self.error_message,
            file_size_bytes=self.file_size_bytes,
            id=self.id,
            index_id=self.index_id,
            name=self.name,
            role_arn=self.role_arn,
            source_s3_paths=self.source_s3_paths,
            status=self.status,
            synonym_rule_count=self.synonym_rule_count,
            tags=self.tags,
            term_count=self.term_count,
            thesaurus_id=self.thesaurus_id,
            updated_at=self.updated_at)


def get_thesaurus(index_id: Optional[str] = None,
                  tags: Optional[Mapping[str, str]] = None,
                  thesaurus_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetThesaurusResult:
    """
    Provides details about a specific Amazon Kendra Thesaurus.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.kendra.get_thesaurus(index_id="12345678-1234-1234-1234-123456789123",
        thesaurus_id="87654321-1234-4321-4321-321987654321")
    ```


    :param str index_id: The identifier of the index that contains the Thesaurus.
    :param Mapping[str, str] tags: Metadata that helps organize the Thesaurus you create.
    :param str thesaurus_id: The identifier of the Thesaurus.
    """
    __args__ = dict()
    __args__['indexId'] = index_id
    __args__['tags'] = tags
    __args__['thesaurusId'] = thesaurus_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:kendra/getThesaurus:getThesaurus', __args__, opts=opts, typ=GetThesaurusResult).value

    return AwaitableGetThesaurusResult(
        arn=__ret__.arn,
        created_at=__ret__.created_at,
        description=__ret__.description,
        error_message=__ret__.error_message,
        file_size_bytes=__ret__.file_size_bytes,
        id=__ret__.id,
        index_id=__ret__.index_id,
        name=__ret__.name,
        role_arn=__ret__.role_arn,
        source_s3_paths=__ret__.source_s3_paths,
        status=__ret__.status,
        synonym_rule_count=__ret__.synonym_rule_count,
        tags=__ret__.tags,
        term_count=__ret__.term_count,
        thesaurus_id=__ret__.thesaurus_id,
        updated_at=__ret__.updated_at)


@_utilities.lift_output_func(get_thesaurus)
def get_thesaurus_output(index_id: Optional[pulumi.Input[str]] = None,
                         tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         thesaurus_id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetThesaurusResult]:
    """
    Provides details about a specific Amazon Kendra Thesaurus.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.kendra.get_thesaurus(index_id="12345678-1234-1234-1234-123456789123",
        thesaurus_id="87654321-1234-4321-4321-321987654321")
    ```


    :param str index_id: The identifier of the index that contains the Thesaurus.
    :param Mapping[str, str] tags: Metadata that helps organize the Thesaurus you create.
    :param str thesaurus_id: The identifier of the Thesaurus.
    """
    ...
