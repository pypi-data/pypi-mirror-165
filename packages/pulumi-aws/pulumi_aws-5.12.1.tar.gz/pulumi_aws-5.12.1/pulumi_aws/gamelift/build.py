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

__all__ = ['BuildArgs', 'Build']

@pulumi.input_type
class BuildArgs:
    def __init__(__self__, *,
                 operating_system: pulumi.Input[str],
                 storage_location: pulumi.Input['BuildStorageLocationArgs'],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Build resource.
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        :param pulumi.Input['BuildStorageLocationArgs'] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] version: Version that is associated with this build.
        """
        pulumi.set(__self__, "operating_system", operating_system)
        pulumi.set(__self__, "storage_location", storage_location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> pulumi.Input[str]:
        """
        Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        """
        return pulumi.get(self, "operating_system")

    @operating_system.setter
    def operating_system(self, value: pulumi.Input[str]):
        pulumi.set(self, "operating_system", value)

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> pulumi.Input['BuildStorageLocationArgs']:
        """
        Information indicating where your game build files are stored. See below.
        """
        return pulumi.get(self, "storage_location")

    @storage_location.setter
    def storage_location(self, value: pulumi.Input['BuildStorageLocationArgs']):
        pulumi.set(self, "storage_location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the build
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version that is associated with this build.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class _BuildState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input['BuildStorageLocationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Build resources.
        :param pulumi.Input[str] arn: GameLift Build ARN.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        :param pulumi.Input['BuildStorageLocationArgs'] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] version: Version that is associated with this build.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if operating_system is not None:
            pulumi.set(__self__, "operating_system", operating_system)
        if storage_location is not None:
            pulumi.set(__self__, "storage_location", storage_location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        GameLift Build ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the build
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> Optional[pulumi.Input[str]]:
        """
        Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        """
        return pulumi.get(self, "operating_system")

    @operating_system.setter
    def operating_system(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operating_system", value)

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> Optional[pulumi.Input['BuildStorageLocationArgs']]:
        """
        Information indicating where your game build files are stored. See below.
        """
        return pulumi.get(self, "storage_location")

    @storage_location.setter
    def storage_location(self, value: Optional[pulumi.Input['BuildStorageLocationArgs']]):
        pulumi.set(self, "storage_location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version that is associated with this build.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class Build(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[pulumi.InputType['BuildStorageLocationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an GameLift Build resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.gamelift.Build("test",
            operating_system="WINDOWS_2012",
            storage_location=aws.gamelift.BuildStorageLocationArgs(
                bucket=aws_s3_bucket["test"]["bucket"],
                key=aws_s3_object["test"]["key"],
                role_arn=aws_iam_role["test"]["arn"],
            ))
        ```

        ## Import

        GameLift Builds can be imported using the ID, e.g.,

        ```sh
         $ pulumi import aws:gamelift/build:Build example <build-id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        :param pulumi.Input[pulumi.InputType['BuildStorageLocationArgs']] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] version: Version that is associated with this build.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BuildArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an GameLift Build resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.gamelift.Build("test",
            operating_system="WINDOWS_2012",
            storage_location=aws.gamelift.BuildStorageLocationArgs(
                bucket=aws_s3_bucket["test"]["bucket"],
                key=aws_s3_object["test"]["key"],
                role_arn=aws_iam_role["test"]["arn"],
            ))
        ```

        ## Import

        GameLift Builds can be imported using the ID, e.g.,

        ```sh
         $ pulumi import aws:gamelift/build:Build example <build-id>
        ```

        :param str resource_name: The name of the resource.
        :param BuildArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BuildArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 operating_system: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[pulumi.InputType['BuildStorageLocationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BuildArgs.__new__(BuildArgs)

            __props__.__dict__["name"] = name
            if operating_system is None and not opts.urn:
                raise TypeError("Missing required property 'operating_system'")
            __props__.__dict__["operating_system"] = operating_system
            if storage_location is None and not opts.urn:
                raise TypeError("Missing required property 'storage_location'")
            __props__.__dict__["storage_location"] = storage_location
            __props__.__dict__["tags"] = tags
            __props__.__dict__["version"] = version
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Build, __self__).__init__(
            'aws:gamelift/build:Build',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            operating_system: Optional[pulumi.Input[str]] = None,
            storage_location: Optional[pulumi.Input[pulumi.InputType['BuildStorageLocationArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            version: Optional[pulumi.Input[str]] = None) -> 'Build':
        """
        Get an existing Build resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: GameLift Build ARN.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        :param pulumi.Input[pulumi.InputType['BuildStorageLocationArgs']] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] version: Version that is associated with this build.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BuildState.__new__(_BuildState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["name"] = name
        __props__.__dict__["operating_system"] = operating_system
        __props__.__dict__["storage_location"] = storage_location
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["version"] = version
        return Build(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        GameLift Build ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the build
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="operatingSystem")
    def operating_system(self) -> pulumi.Output[str]:
        """
        Operating system that the game server binaries are built to run onE.g., `WINDOWS_2012`, `AMAZON_LINUX` or `AMAZON_LINUX_2`.
        """
        return pulumi.get(self, "operating_system")

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> pulumi.Output['outputs.BuildStorageLocation']:
        """
        Information indicating where your game build files are stored. See below.
        """
        return pulumi.get(self, "storage_location")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        Version that is associated with this build.
        """
        return pulumi.get(self, "version")

