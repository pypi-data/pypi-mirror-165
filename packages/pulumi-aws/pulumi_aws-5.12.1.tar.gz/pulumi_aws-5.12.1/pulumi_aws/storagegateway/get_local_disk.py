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
    'GetLocalDiskResult',
    'AwaitableGetLocalDiskResult',
    'get_local_disk',
    'get_local_disk_output',
]

@pulumi.output_type
class GetLocalDiskResult:
    """
    A collection of values returned by getLocalDisk.
    """
    def __init__(__self__, disk_id=None, disk_node=None, disk_path=None, gateway_arn=None, id=None):
        if disk_id and not isinstance(disk_id, str):
            raise TypeError("Expected argument 'disk_id' to be a str")
        pulumi.set(__self__, "disk_id", disk_id)
        if disk_node and not isinstance(disk_node, str):
            raise TypeError("Expected argument 'disk_node' to be a str")
        pulumi.set(__self__, "disk_node", disk_node)
        if disk_path and not isinstance(disk_path, str):
            raise TypeError("Expected argument 'disk_path' to be a str")
        pulumi.set(__self__, "disk_path", disk_path)
        if gateway_arn and not isinstance(gateway_arn, str):
            raise TypeError("Expected argument 'gateway_arn' to be a str")
        pulumi.set(__self__, "gateway_arn", gateway_arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> str:
        """
        The disk identifierE.g., `pci-0000:03:00.0-scsi-0:0:0:0`
        """
        return pulumi.get(self, "disk_id")

    @property
    @pulumi.getter(name="diskNode")
    def disk_node(self) -> str:
        return pulumi.get(self, "disk_node")

    @property
    @pulumi.getter(name="diskPath")
    def disk_path(self) -> str:
        return pulumi.get(self, "disk_path")

    @property
    @pulumi.getter(name="gatewayArn")
    def gateway_arn(self) -> str:
        return pulumi.get(self, "gateway_arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetLocalDiskResult(GetLocalDiskResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocalDiskResult(
            disk_id=self.disk_id,
            disk_node=self.disk_node,
            disk_path=self.disk_path,
            gateway_arn=self.gateway_arn,
            id=self.id)


def get_local_disk(disk_node: Optional[str] = None,
                   disk_path: Optional[str] = None,
                   gateway_arn: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocalDiskResult:
    """
    Retrieve information about a Storage Gateway local disk. The disk identifier is useful for adding the disk as a cache or upload buffer to a gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.storagegateway.get_local_disk(disk_path=aws_volume_attachment["test"]["device_name"],
        gateway_arn=aws_storagegateway_gateway["test"]["arn"])
    ```


    :param str disk_node: The device node of the local disk to retrieve. For example, `/dev/sdb`.
    :param str disk_path: The device path of the local disk to retrieve. For example, `/dev/xvdb` or `/dev/nvme1n1`.
    :param str gateway_arn: The Amazon Resource Name (ARN) of the gateway.
    """
    __args__ = dict()
    __args__['diskNode'] = disk_node
    __args__['diskPath'] = disk_path
    __args__['gatewayArn'] = gateway_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:storagegateway/getLocalDisk:getLocalDisk', __args__, opts=opts, typ=GetLocalDiskResult).value

    return AwaitableGetLocalDiskResult(
        disk_id=__ret__.disk_id,
        disk_node=__ret__.disk_node,
        disk_path=__ret__.disk_path,
        gateway_arn=__ret__.gateway_arn,
        id=__ret__.id)


@_utilities.lift_output_func(get_local_disk)
def get_local_disk_output(disk_node: Optional[pulumi.Input[Optional[str]]] = None,
                          disk_path: Optional[pulumi.Input[Optional[str]]] = None,
                          gateway_arn: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLocalDiskResult]:
    """
    Retrieve information about a Storage Gateway local disk. The disk identifier is useful for adding the disk as a cache or upload buffer to a gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.storagegateway.get_local_disk(disk_path=aws_volume_attachment["test"]["device_name"],
        gateway_arn=aws_storagegateway_gateway["test"]["arn"])
    ```


    :param str disk_node: The device node of the local disk to retrieve. For example, `/dev/sdb`.
    :param str disk_path: The device path of the local disk to retrieve. For example, `/dev/xvdb` or `/dev/nvme1n1`.
    :param str gateway_arn: The Amazon Resource Name (ARN) of the gateway.
    """
    ...
