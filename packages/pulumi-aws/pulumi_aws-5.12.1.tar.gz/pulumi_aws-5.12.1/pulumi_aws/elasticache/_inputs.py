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
    'ClusterCacheNodeArgs',
    'ClusterLogDeliveryConfigurationArgs',
    'ParameterGroupParameterArgs',
    'ReplicationGroupClusterModeArgs',
    'ReplicationGroupLogDeliveryConfigurationArgs',
]

@pulumi.input_type
class ClusterCacheNodeArgs:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] availability_zone: Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        :param pulumi.Input[int] port: The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "availability_zone")

    @availability_zone.setter
    def availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_zone", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class ClusterLogDeliveryConfigurationArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input[str],
                 destination_type: pulumi.Input[str],
                 log_format: pulumi.Input[str],
                 log_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param pulumi.Input[str] destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param pulumi.Input[str] log_format: Valid values are `json` or `text`
        :param pulumi.Input[str] log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input[str]:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> pulumi.Input[str]:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @destination_type.setter
    def destination_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_type", value)

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> pulumi.Input[str]:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @log_format.setter
    def log_format(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_format", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class ParameterGroupParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the ElastiCache parameter.
        :param pulumi.Input[str] value: The value of the ElastiCache parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the ElastiCache parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the ElastiCache parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ReplicationGroupClusterModeArgs:
    def __init__(__self__, *,
                 num_node_groups: Optional[pulumi.Input[int]] = None,
                 replicas_per_node_group: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] num_node_groups: Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications. Required unless `global_replication_group_id` is set.
        :param pulumi.Input[int] replicas_per_node_group: Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        if num_node_groups is not None:
            warnings.warn("""Use root-level num_node_groups instead""", DeprecationWarning)
            pulumi.log.warn("""num_node_groups is deprecated: Use root-level num_node_groups instead""")
        if num_node_groups is not None:
            pulumi.set(__self__, "num_node_groups", num_node_groups)
        if replicas_per_node_group is not None:
            warnings.warn("""Use root-level replicas_per_node_group instead""", DeprecationWarning)
            pulumi.log.warn("""replicas_per_node_group is deprecated: Use root-level replicas_per_node_group instead""")
        if replicas_per_node_group is not None:
            pulumi.set(__self__, "replicas_per_node_group", replicas_per_node_group)

    @property
    @pulumi.getter(name="numNodeGroups")
    def num_node_groups(self) -> Optional[pulumi.Input[int]]:
        """
        Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications. Required unless `global_replication_group_id` is set.
        """
        return pulumi.get(self, "num_node_groups")

    @num_node_groups.setter
    def num_node_groups(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "num_node_groups", value)

    @property
    @pulumi.getter(name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> Optional[pulumi.Input[int]]:
        """
        Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        return pulumi.get(self, "replicas_per_node_group")

    @replicas_per_node_group.setter
    def replicas_per_node_group(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "replicas_per_node_group", value)


@pulumi.input_type
class ReplicationGroupLogDeliveryConfigurationArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input[str],
                 destination_type: pulumi.Input[str],
                 log_format: pulumi.Input[str],
                 log_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param pulumi.Input[str] destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param pulumi.Input[str] log_format: Valid values are `json` or `text`
        :param pulumi.Input[str] log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input[str]:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> pulumi.Input[str]:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @destination_type.setter
    def destination_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_type", value)

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> pulumi.Input[str]:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @log_format.setter
    def log_format(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_format", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)


