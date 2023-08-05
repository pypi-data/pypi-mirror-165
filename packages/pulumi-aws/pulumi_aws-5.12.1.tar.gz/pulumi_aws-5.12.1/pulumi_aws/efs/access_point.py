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

__all__ = ['AccessPointArgs', 'AccessPoint']

@pulumi.input_type
class AccessPointArgs:
    def __init__(__self__, *,
                 file_system_id: pulumi.Input[str],
                 posix_user: Optional[pulumi.Input['AccessPointPosixUserArgs']] = None,
                 root_directory: Optional[pulumi.Input['AccessPointRootDirectoryArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AccessPoint resource.
        :param pulumi.Input[str] file_system_id: ID of the file system for which the access point is intended.
        :param pulumi.Input['AccessPointPosixUserArgs'] posix_user: Operating system user and group applied to all file system requests made using the access point. Detailed below.
        :param pulumi.Input['AccessPointRootDirectoryArgs'] root_directory: Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        pulumi.set(__self__, "file_system_id", file_system_id)
        if posix_user is not None:
            pulumi.set(__self__, "posix_user", posix_user)
        if root_directory is not None:
            pulumi.set(__self__, "root_directory", root_directory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Input[str]:
        """
        ID of the file system for which the access point is intended.
        """
        return pulumi.get(self, "file_system_id")

    @file_system_id.setter
    def file_system_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "file_system_id", value)

    @property
    @pulumi.getter(name="posixUser")
    def posix_user(self) -> Optional[pulumi.Input['AccessPointPosixUserArgs']]:
        """
        Operating system user and group applied to all file system requests made using the access point. Detailed below.
        """
        return pulumi.get(self, "posix_user")

    @posix_user.setter
    def posix_user(self, value: Optional[pulumi.Input['AccessPointPosixUserArgs']]):
        pulumi.set(self, "posix_user", value)

    @property
    @pulumi.getter(name="rootDirectory")
    def root_directory(self) -> Optional[pulumi.Input['AccessPointRootDirectoryArgs']]:
        """
        Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        """
        return pulumi.get(self, "root_directory")

    @root_directory.setter
    def root_directory(self, value: Optional[pulumi.Input['AccessPointRootDirectoryArgs']]):
        pulumi.set(self, "root_directory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AccessPointState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 file_system_arn: Optional[pulumi.Input[str]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 posix_user: Optional[pulumi.Input['AccessPointPosixUserArgs']] = None,
                 root_directory: Optional[pulumi.Input['AccessPointRootDirectoryArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AccessPoint resources.
        :param pulumi.Input[str] arn: ARN of the access point.
        :param pulumi.Input[str] file_system_arn: ARN of the file system.
        :param pulumi.Input[str] file_system_id: ID of the file system for which the access point is intended.
        :param pulumi.Input['AccessPointPosixUserArgs'] posix_user: Operating system user and group applied to all file system requests made using the access point. Detailed below.
        :param pulumi.Input['AccessPointRootDirectoryArgs'] root_directory: Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if file_system_arn is not None:
            pulumi.set(__self__, "file_system_arn", file_system_arn)
        if file_system_id is not None:
            pulumi.set(__self__, "file_system_id", file_system_id)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if posix_user is not None:
            pulumi.set(__self__, "posix_user", posix_user)
        if root_directory is not None:
            pulumi.set(__self__, "root_directory", root_directory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the access point.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="fileSystemArn")
    def file_system_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the file system.
        """
        return pulumi.get(self, "file_system_arn")

    @file_system_arn.setter
    def file_system_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_arn", value)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the file system for which the access point is intended.
        """
        return pulumi.get(self, "file_system_id")

    @file_system_id.setter
    def file_system_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_id", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter(name="posixUser")
    def posix_user(self) -> Optional[pulumi.Input['AccessPointPosixUserArgs']]:
        """
        Operating system user and group applied to all file system requests made using the access point. Detailed below.
        """
        return pulumi.get(self, "posix_user")

    @posix_user.setter
    def posix_user(self, value: Optional[pulumi.Input['AccessPointPosixUserArgs']]):
        pulumi.set(self, "posix_user", value)

    @property
    @pulumi.getter(name="rootDirectory")
    def root_directory(self) -> Optional[pulumi.Input['AccessPointRootDirectoryArgs']]:
        """
        Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        """
        return pulumi.get(self, "root_directory")

    @root_directory.setter
    def root_directory(self, value: Optional[pulumi.Input['AccessPointRootDirectoryArgs']]):
        pulumi.set(self, "root_directory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
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


class AccessPoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 posix_user: Optional[pulumi.Input[pulumi.InputType['AccessPointPosixUserArgs']]] = None,
                 root_directory: Optional[pulumi.Input[pulumi.InputType['AccessPointRootDirectoryArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides an Elastic File System (EFS) access point.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.efs.AccessPoint("test", file_system_id=aws_efs_file_system["foo"]["id"])
        ```

        ## Import

        The EFS access points can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:efs/accessPoint:AccessPoint test fsap-52a643fb
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file_system_id: ID of the file system for which the access point is intended.
        :param pulumi.Input[pulumi.InputType['AccessPointPosixUserArgs']] posix_user: Operating system user and group applied to all file system requests made using the access point. Detailed below.
        :param pulumi.Input[pulumi.InputType['AccessPointRootDirectoryArgs']] root_directory: Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessPointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Elastic File System (EFS) access point.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.efs.AccessPoint("test", file_system_id=aws_efs_file_system["foo"]["id"])
        ```

        ## Import

        The EFS access points can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:efs/accessPoint:AccessPoint test fsap-52a643fb
        ```

        :param str resource_name: The name of the resource.
        :param AccessPointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessPointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 posix_user: Optional[pulumi.Input[pulumi.InputType['AccessPointPosixUserArgs']]] = None,
                 root_directory: Optional[pulumi.Input[pulumi.InputType['AccessPointRootDirectoryArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessPointArgs.__new__(AccessPointArgs)

            if file_system_id is None and not opts.urn:
                raise TypeError("Missing required property 'file_system_id'")
            __props__.__dict__["file_system_id"] = file_system_id
            __props__.__dict__["posix_user"] = posix_user
            __props__.__dict__["root_directory"] = root_directory
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["file_system_arn"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["tags_all"] = None
        super(AccessPoint, __self__).__init__(
            'aws:efs/accessPoint:AccessPoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            file_system_arn: Optional[pulumi.Input[str]] = None,
            file_system_id: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            posix_user: Optional[pulumi.Input[pulumi.InputType['AccessPointPosixUserArgs']]] = None,
            root_directory: Optional[pulumi.Input[pulumi.InputType['AccessPointRootDirectoryArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'AccessPoint':
        """
        Get an existing AccessPoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the access point.
        :param pulumi.Input[str] file_system_arn: ARN of the file system.
        :param pulumi.Input[str] file_system_id: ID of the file system for which the access point is intended.
        :param pulumi.Input[pulumi.InputType['AccessPointPosixUserArgs']] posix_user: Operating system user and group applied to all file system requests made using the access point. Detailed below.
        :param pulumi.Input[pulumi.InputType['AccessPointRootDirectoryArgs']] root_directory: Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessPointState.__new__(_AccessPointState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["file_system_arn"] = file_system_arn
        __props__.__dict__["file_system_id"] = file_system_id
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["posix_user"] = posix_user
        __props__.__dict__["root_directory"] = root_directory
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return AccessPoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the access point.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="fileSystemArn")
    def file_system_arn(self) -> pulumi.Output[str]:
        """
        ARN of the file system.
        """
        return pulumi.get(self, "file_system_arn")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Output[str]:
        """
        ID of the file system for which the access point is intended.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="posixUser")
    def posix_user(self) -> pulumi.Output[Optional['outputs.AccessPointPosixUser']]:
        """
        Operating system user and group applied to all file system requests made using the access point. Detailed below.
        """
        return pulumi.get(self, "posix_user")

    @property
    @pulumi.getter(name="rootDirectory")
    def root_directory(self) -> pulumi.Output['outputs.AccessPointRootDirectory']:
        """
        Directory on the Amazon EFS file system that the access point provides access to. Detailed below.
        """
        return pulumi.get(self, "root_directory")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

