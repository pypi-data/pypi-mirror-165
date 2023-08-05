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
    'AcceleratorAttributesArgs',
    'AcceleratorIpSetArgs',
    'EndpointGroupEndpointConfigurationArgs',
    'EndpointGroupPortOverrideArgs',
    'ListenerPortRangeArgs',
]

@pulumi.input_type
class AcceleratorAttributesArgs:
    def __init__(__self__, *,
                 flow_logs_enabled: Optional[pulumi.Input[bool]] = None,
                 flow_logs_s3_bucket: Optional[pulumi.Input[str]] = None,
                 flow_logs_s3_prefix: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] flow_logs_enabled: Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        :param pulumi.Input[str] flow_logs_s3_bucket: The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        :param pulumi.Input[str] flow_logs_s3_prefix: The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        if flow_logs_enabled is not None:
            pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        if flow_logs_s3_bucket is not None:
            pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        if flow_logs_s3_prefix is not None:
            pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "flow_logs_enabled")

    @flow_logs_enabled.setter
    def flow_logs_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "flow_logs_enabled", value)

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_bucket")

    @flow_logs_s3_bucket.setter
    def flow_logs_s3_bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "flow_logs_s3_bucket", value)

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_prefix")

    @flow_logs_s3_prefix.setter
    def flow_logs_s3_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "flow_logs_s3_prefix", value)


@pulumi.input_type
class AcceleratorIpSetArgs:
    def __init__(__self__, *,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_family: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: A list of IP addresses in the IP address set.
        :param pulumi.Input[str] ip_family: The type of IP addresses included in this IP set.
        """
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_family is not None:
            pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IP addresses in the IP address set.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> Optional[pulumi.Input[str]]:
        """
        The type of IP addresses included in this IP set.
        """
        return pulumi.get(self, "ip_family")

    @ip_family.setter
    def ip_family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_family", value)


@pulumi.input_type
class EndpointGroupEndpointConfigurationArgs:
    def __init__(__self__, *,
                 client_ip_preservation_enabled: Optional[pulumi.Input[bool]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[bool] client_ip_preservation_enabled: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. See the [AWS documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html) for more details. The default value is `false`.
               **Note:** When client IP address preservation is enabled, the Global Accelerator service creates an EC2 Security Group in the VPC named `GlobalAccelerator` that must be deleted (potentially outside of the provider) before the VPC will successfully delete. If this EC2 Security Group is not deleted, the provider will retry the VPC deletion for a few minutes before reporting a `DependencyViolation` error. This cannot be resolved by re-running the provider.
        :param pulumi.Input[str] endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        :param pulumi.Input[int] weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        if client_ip_preservation_enabled is not None:
            pulumi.set(__self__, "client_ip_preservation_enabled", client_ip_preservation_enabled)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="clientIpPreservationEnabled")
    def client_ip_preservation_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. See the [AWS documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html) for more details. The default value is `false`.
        **Note:** When client IP address preservation is enabled, the Global Accelerator service creates an EC2 Security Group in the VPC named `GlobalAccelerator` that must be deleted (potentially outside of the provider) before the VPC will successfully delete. If this EC2 Security Group is not deleted, the provider will retry the VPC deletion for a few minutes before reporting a `DependencyViolation` error. This cannot be resolved by re-running the provider.
        """
        return pulumi.get(self, "client_ip_preservation_enabled")

    @client_ip_preservation_enabled.setter
    def client_ip_preservation_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "client_ip_preservation_enabled", value)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class EndpointGroupPortOverrideArgs:
    def __init__(__self__, *,
                 endpoint_port: pulumi.Input[int],
                 listener_port: pulumi.Input[int]):
        """
        :param pulumi.Input[int] endpoint_port: The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        :param pulumi.Input[int] listener_port: The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        pulumi.set(__self__, "endpoint_port", endpoint_port)
        pulumi.set(__self__, "listener_port", listener_port)

    @property
    @pulumi.getter(name="endpointPort")
    def endpoint_port(self) -> pulumi.Input[int]:
        """
        The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        """
        return pulumi.get(self, "endpoint_port")

    @endpoint_port.setter
    def endpoint_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "endpoint_port", value)

    @property
    @pulumi.getter(name="listenerPort")
    def listener_port(self) -> pulumi.Input[int]:
        """
        The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        return pulumi.get(self, "listener_port")

    @listener_port.setter
    def listener_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "listener_port", value)


@pulumi.input_type
class ListenerPortRangeArgs:
    def __init__(__self__, *,
                 from_port: Optional[pulumi.Input[int]] = None,
                 to_port: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] from_port: The first port in the range of ports, inclusive.
        :param pulumi.Input[int] to_port: The last port in the range of ports, inclusive.
        """
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[pulumi.Input[int]]:
        """
        The first port in the range of ports, inclusive.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[pulumi.Input[int]]:
        """
        The last port in the range of ports, inclusive.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "to_port", value)


