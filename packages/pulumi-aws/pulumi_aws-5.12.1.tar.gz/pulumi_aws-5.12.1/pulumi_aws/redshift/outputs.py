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
    'ClusterClusterNode',
    'ClusterLogging',
    'ClusterSnapshotCopy',
    'EndpointAccessVpcEndpoint',
    'EndpointAccessVpcEndpointNetworkInterface',
    'ParameterGroupParameter',
    'ScheduledActionTargetAction',
    'ScheduledActionTargetActionPauseCluster',
    'ScheduledActionTargetActionResizeCluster',
    'ScheduledActionTargetActionResumeCluster',
    'SecurityGroupIngress',
    'GetClusterClusterNodeResult',
]

@pulumi.output_type
class ClusterClusterNode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nodeRole":
            suggest = "node_role"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "publicIpAddress":
            suggest = "public_ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterClusterNode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterClusterNode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterClusterNode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 node_role: Optional[str] = None,
                 private_ip_address: Optional[str] = None,
                 public_ip_address: Optional[str] = None):
        """
        :param str node_role: Whether the node is a leader node or a compute node
        :param str private_ip_address: The private IP address of a node within a cluster
        :param str public_ip_address: The public IP address of a node within a cluster
        """
        if node_role is not None:
            pulumi.set(__self__, "node_role", node_role)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if public_ip_address is not None:
            pulumi.set(__self__, "public_ip_address", public_ip_address)

    @property
    @pulumi.getter(name="nodeRole")
    def node_role(self) -> Optional[str]:
        """
        Whether the node is a leader node or a compute node
        """
        return pulumi.get(self, "node_role")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        The private IP address of a node within a cluster
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="publicIpAddress")
    def public_ip_address(self) -> Optional[str]:
        """
        The public IP address of a node within a cluster
        """
        return pulumi.get(self, "public_ip_address")


@pulumi.output_type
class ClusterLogging(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"
        elif key == "logDestinationType":
            suggest = "log_destination_type"
        elif key == "logExports":
            suggest = "log_exports"
        elif key == "s3KeyPrefix":
            suggest = "s3_key_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterLogging. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterLogging.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterLogging.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enable: bool,
                 bucket_name: Optional[str] = None,
                 log_destination_type: Optional[str] = None,
                 log_exports: Optional[Sequence[str]] = None,
                 s3_key_prefix: Optional[str] = None):
        """
        :param bool enable: Enables logging information such as queries and connection attempts, for the specified Amazon Redshift cluster.
        :param str bucket_name: The name of an existing S3 bucket where the log files are to be stored. Must be in the same region as the cluster and the cluster must have read bucket and put object permissions.
               For more information on the permissions required for the bucket, please read the AWS [documentation](http://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html#db-auditing-enable-logging)
        :param str log_destination_type: The log destination type. An enum with possible values of `s3` and `cloudwatch`.
        :param Sequence[str] log_exports: The collection of exported log types. Log types include the connection log, user log and user activity log. Required when `log_destination_type` is `cloudwatch`. Valid log types are `connectionlog`, `userlog`, and `useractivitylog`.
        :param str s3_key_prefix: The prefix applied to the log file names.
        """
        pulumi.set(__self__, "enable", enable)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if log_destination_type is not None:
            pulumi.set(__self__, "log_destination_type", log_destination_type)
        if log_exports is not None:
            pulumi.set(__self__, "log_exports", log_exports)
        if s3_key_prefix is not None:
            pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)

    @property
    @pulumi.getter
    def enable(self) -> bool:
        """
        Enables logging information such as queries and connection attempts, for the specified Amazon Redshift cluster.
        """
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[str]:
        """
        The name of an existing S3 bucket where the log files are to be stored. Must be in the same region as the cluster and the cluster must have read bucket and put object permissions.
        For more information on the permissions required for the bucket, please read the AWS [documentation](http://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html#db-auditing-enable-logging)
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="logDestinationType")
    def log_destination_type(self) -> Optional[str]:
        """
        The log destination type. An enum with possible values of `s3` and `cloudwatch`.
        """
        return pulumi.get(self, "log_destination_type")

    @property
    @pulumi.getter(name="logExports")
    def log_exports(self) -> Optional[Sequence[str]]:
        """
        The collection of exported log types. Log types include the connection log, user log and user activity log. Required when `log_destination_type` is `cloudwatch`. Valid log types are `connectionlog`, `userlog`, and `useractivitylog`.
        """
        return pulumi.get(self, "log_exports")

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> Optional[str]:
        """
        The prefix applied to the log file names.
        """
        return pulumi.get(self, "s3_key_prefix")


@pulumi.output_type
class ClusterSnapshotCopy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationRegion":
            suggest = "destination_region"
        elif key == "grantName":
            suggest = "grant_name"
        elif key == "retentionPeriod":
            suggest = "retention_period"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterSnapshotCopy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterSnapshotCopy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterSnapshotCopy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_region: str,
                 grant_name: Optional[str] = None,
                 retention_period: Optional[int] = None):
        """
        :param str destination_region: The destination region that you want to copy snapshots to.
        :param str grant_name: The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted cluster are copied to the destination region.
        :param int retention_period: The number of days to retain automated snapshots in the destination region after they are copied from the source region. Defaults to `7`.
        """
        pulumi.set(__self__, "destination_region", destination_region)
        if grant_name is not None:
            pulumi.set(__self__, "grant_name", grant_name)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)

    @property
    @pulumi.getter(name="destinationRegion")
    def destination_region(self) -> str:
        """
        The destination region that you want to copy snapshots to.
        """
        return pulumi.get(self, "destination_region")

    @property
    @pulumi.getter(name="grantName")
    def grant_name(self) -> Optional[str]:
        """
        The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted cluster are copied to the destination region.
        """
        return pulumi.get(self, "grant_name")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[int]:
        """
        The number of days to retain automated snapshots in the destination region after they are copied from the source region. Defaults to `7`.
        """
        return pulumi.get(self, "retention_period")


@pulumi.output_type
class EndpointAccessVpcEndpoint(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaces":
            suggest = "network_interfaces"
        elif key == "vpcEndpointId":
            suggest = "vpc_endpoint_id"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointAccessVpcEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointAccessVpcEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointAccessVpcEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interfaces: Optional[Sequence['outputs.EndpointAccessVpcEndpointNetworkInterface']] = None,
                 vpc_endpoint_id: Optional[str] = None,
                 vpc_id: Optional[str] = None):
        """
        :param Sequence['EndpointAccessVpcEndpointNetworkInterfaceArgs'] network_interfaces: One or more network interfaces of the endpoint. Also known as an interface endpoint. See details below.
        :param str vpc_endpoint_id: The connection endpoint ID for connecting an Amazon Redshift cluster through the proxy.
        :param str vpc_id: The VPC identifier that the endpoint is associated.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.EndpointAccessVpcEndpointNetworkInterface']]:
        """
        One or more network interfaces of the endpoint. Also known as an interface endpoint. See details below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[str]:
        """
        The connection endpoint ID for connecting an Amazon Redshift cluster through the proxy.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The VPC identifier that the endpoint is associated.
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class EndpointAccessVpcEndpointNetworkInterface(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"
        elif key == "networkInterfaceId":
            suggest = "network_interface_id"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointAccessVpcEndpointNetworkInterface. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointAccessVpcEndpointNetworkInterface.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointAccessVpcEndpointNetworkInterface.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 availability_zone: Optional[str] = None,
                 network_interface_id: Optional[str] = None,
                 private_ip_address: Optional[str] = None,
                 subnet_id: Optional[str] = None):
        """
        :param str availability_zone: The Availability Zone.
        :param str network_interface_id: The network interface identifier.
        :param str private_ip_address: The IPv4 address of the network interface within the subnet.
        :param str subnet_id: The subnet identifier.
        """
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        The Availability Zone.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[str]:
        """
        The network interface identifier.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        The IPv4 address of the network interface within the subnet.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The subnet identifier.
        """
        return pulumi.get(self, "subnet_id")


@pulumi.output_type
class ParameterGroupParameter(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The name of the Redshift parameter.
        :param str value: The value of the Redshift parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Redshift parameter.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the Redshift parameter.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ScheduledActionTargetAction(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pauseCluster":
            suggest = "pause_cluster"
        elif key == "resizeCluster":
            suggest = "resize_cluster"
        elif key == "resumeCluster":
            suggest = "resume_cluster"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledActionTargetAction. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledActionTargetAction.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledActionTargetAction.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 pause_cluster: Optional['outputs.ScheduledActionTargetActionPauseCluster'] = None,
                 resize_cluster: Optional['outputs.ScheduledActionTargetActionResizeCluster'] = None,
                 resume_cluster: Optional['outputs.ScheduledActionTargetActionResumeCluster'] = None):
        """
        :param 'ScheduledActionTargetActionPauseClusterArgs' pause_cluster: An action that runs a `PauseCluster` API operation. Documented below.
        :param 'ScheduledActionTargetActionResizeClusterArgs' resize_cluster: An action that runs a `ResizeCluster` API operation. Documented below.
        :param 'ScheduledActionTargetActionResumeClusterArgs' resume_cluster: An action that runs a `ResumeCluster` API operation. Documented below.
        """
        if pause_cluster is not None:
            pulumi.set(__self__, "pause_cluster", pause_cluster)
        if resize_cluster is not None:
            pulumi.set(__self__, "resize_cluster", resize_cluster)
        if resume_cluster is not None:
            pulumi.set(__self__, "resume_cluster", resume_cluster)

    @property
    @pulumi.getter(name="pauseCluster")
    def pause_cluster(self) -> Optional['outputs.ScheduledActionTargetActionPauseCluster']:
        """
        An action that runs a `PauseCluster` API operation. Documented below.
        """
        return pulumi.get(self, "pause_cluster")

    @property
    @pulumi.getter(name="resizeCluster")
    def resize_cluster(self) -> Optional['outputs.ScheduledActionTargetActionResizeCluster']:
        """
        An action that runs a `ResizeCluster` API operation. Documented below.
        """
        return pulumi.get(self, "resize_cluster")

    @property
    @pulumi.getter(name="resumeCluster")
    def resume_cluster(self) -> Optional['outputs.ScheduledActionTargetActionResumeCluster']:
        """
        An action that runs a `ResumeCluster` API operation. Documented below.
        """
        return pulumi.get(self, "resume_cluster")


@pulumi.output_type
class ScheduledActionTargetActionPauseCluster(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterIdentifier":
            suggest = "cluster_identifier"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledActionTargetActionPauseCluster. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledActionTargetActionPauseCluster.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledActionTargetActionPauseCluster.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_identifier: str):
        """
        :param str cluster_identifier: The identifier of the cluster to be resumed.
        """
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """
        The identifier of the cluster to be resumed.
        """
        return pulumi.get(self, "cluster_identifier")


@pulumi.output_type
class ScheduledActionTargetActionResizeCluster(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterIdentifier":
            suggest = "cluster_identifier"
        elif key == "clusterType":
            suggest = "cluster_type"
        elif key == "nodeType":
            suggest = "node_type"
        elif key == "numberOfNodes":
            suggest = "number_of_nodes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledActionTargetActionResizeCluster. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledActionTargetActionResizeCluster.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledActionTargetActionResizeCluster.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_identifier: str,
                 classic: Optional[bool] = None,
                 cluster_type: Optional[str] = None,
                 node_type: Optional[str] = None,
                 number_of_nodes: Optional[int] = None):
        """
        :param str cluster_identifier: The identifier of the cluster to be resumed.
        :param bool classic: A boolean value indicating whether the resize operation is using the classic resize process. Default: `false`.
        :param str cluster_type: The new cluster type for the specified cluster.
        :param str node_type: The new node type for the nodes you are adding.
        :param int number_of_nodes: The new number of nodes for the cluster.
        """
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        if classic is not None:
            pulumi.set(__self__, "classic", classic)
        if cluster_type is not None:
            pulumi.set(__self__, "cluster_type", cluster_type)
        if node_type is not None:
            pulumi.set(__self__, "node_type", node_type)
        if number_of_nodes is not None:
            pulumi.set(__self__, "number_of_nodes", number_of_nodes)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """
        The identifier of the cluster to be resumed.
        """
        return pulumi.get(self, "cluster_identifier")

    @property
    @pulumi.getter
    def classic(self) -> Optional[bool]:
        """
        A boolean value indicating whether the resize operation is using the classic resize process. Default: `false`.
        """
        return pulumi.get(self, "classic")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> Optional[str]:
        """
        The new cluster type for the specified cluster.
        """
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> Optional[str]:
        """
        The new node type for the nodes you are adding.
        """
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="numberOfNodes")
    def number_of_nodes(self) -> Optional[int]:
        """
        The new number of nodes for the cluster.
        """
        return pulumi.get(self, "number_of_nodes")


@pulumi.output_type
class ScheduledActionTargetActionResumeCluster(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterIdentifier":
            suggest = "cluster_identifier"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledActionTargetActionResumeCluster. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledActionTargetActionResumeCluster.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledActionTargetActionResumeCluster.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_identifier: str):
        """
        :param str cluster_identifier: The identifier of the cluster to be resumed.
        """
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """
        The identifier of the cluster to be resumed.
        """
        return pulumi.get(self, "cluster_identifier")


@pulumi.output_type
class SecurityGroupIngress(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroupName":
            suggest = "security_group_name"
        elif key == "securityGroupOwnerId":
            suggest = "security_group_owner_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityGroupIngress. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityGroupIngress.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityGroupIngress.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cidr: Optional[str] = None,
                 security_group_name: Optional[str] = None,
                 security_group_owner_id: Optional[str] = None):
        """
        :param str cidr: The CIDR block to accept
        :param str security_group_name: The name of the security group to authorize
        :param str security_group_owner_id: The owner Id of the security group provided
               by `security_group_name`.
        """
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
        if security_group_name is not None:
            pulumi.set(__self__, "security_group_name", security_group_name)
        if security_group_owner_id is not None:
            pulumi.set(__self__, "security_group_owner_id", security_group_owner_id)

    @property
    @pulumi.getter
    def cidr(self) -> Optional[str]:
        """
        The CIDR block to accept
        """
        return pulumi.get(self, "cidr")

    @property
    @pulumi.getter(name="securityGroupName")
    def security_group_name(self) -> Optional[str]:
        """
        The name of the security group to authorize
        """
        return pulumi.get(self, "security_group_name")

    @property
    @pulumi.getter(name="securityGroupOwnerId")
    def security_group_owner_id(self) -> Optional[str]:
        """
        The owner Id of the security group provided
        by `security_group_name`.
        """
        return pulumi.get(self, "security_group_owner_id")


@pulumi.output_type
class GetClusterClusterNodeResult(dict):
    def __init__(__self__, *,
                 node_role: str,
                 private_ip_address: str,
                 public_ip_address: str):
        """
        :param str node_role: Whether the node is a leader node or a compute node
        :param str private_ip_address: The private IP address of a node within a cluster
        :param str public_ip_address: The public IP address of a node within a cluster
        """
        pulumi.set(__self__, "node_role", node_role)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        pulumi.set(__self__, "public_ip_address", public_ip_address)

    @property
    @pulumi.getter(name="nodeRole")
    def node_role(self) -> str:
        """
        Whether the node is a leader node or a compute node
        """
        return pulumi.get(self, "node_role")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        The private IP address of a node within a cluster
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="publicIpAddress")
    def public_ip_address(self) -> str:
        """
        The public IP address of a node within a cluster
        """
        return pulumi.get(self, "public_ip_address")


