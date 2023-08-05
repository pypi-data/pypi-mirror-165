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
    'ConnectorCapacity',
    'ConnectorCapacityAutoscaling',
    'ConnectorCapacityAutoscalingScaleInPolicy',
    'ConnectorCapacityAutoscalingScaleOutPolicy',
    'ConnectorCapacityProvisionedCapacity',
    'ConnectorKafkaCluster',
    'ConnectorKafkaClusterApacheKafkaCluster',
    'ConnectorKafkaClusterApacheKafkaClusterVpc',
    'ConnectorKafkaClusterClientAuthentication',
    'ConnectorKafkaClusterEncryptionInTransit',
    'ConnectorLogDelivery',
    'ConnectorLogDeliveryWorkerLogDelivery',
    'ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs',
    'ConnectorLogDeliveryWorkerLogDeliveryFirehose',
    'ConnectorLogDeliveryWorkerLogDeliveryS3',
    'ConnectorPlugin',
    'ConnectorPluginCustomPlugin',
    'ConnectorWorkerConfiguration',
    'CustomPluginLocation',
    'CustomPluginLocationS3',
]

@pulumi.output_type
class ConnectorCapacity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisionedCapacity":
            suggest = "provisioned_capacity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorCapacity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorCapacity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorCapacity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 autoscaling: Optional['outputs.ConnectorCapacityAutoscaling'] = None,
                 provisioned_capacity: Optional['outputs.ConnectorCapacityProvisionedCapacity'] = None):
        """
        :param 'ConnectorCapacityAutoscalingArgs' autoscaling: Information about the auto scaling parameters for the connector. See below.
        :param 'ConnectorCapacityProvisionedCapacityArgs' provisioned_capacity: Details about a fixed capacity allocated to a connector. See below.
        """
        if autoscaling is not None:
            pulumi.set(__self__, "autoscaling", autoscaling)
        if provisioned_capacity is not None:
            pulumi.set(__self__, "provisioned_capacity", provisioned_capacity)

    @property
    @pulumi.getter
    def autoscaling(self) -> Optional['outputs.ConnectorCapacityAutoscaling']:
        """
        Information about the auto scaling parameters for the connector. See below.
        """
        return pulumi.get(self, "autoscaling")

    @property
    @pulumi.getter(name="provisionedCapacity")
    def provisioned_capacity(self) -> Optional['outputs.ConnectorCapacityProvisionedCapacity']:
        """
        Details about a fixed capacity allocated to a connector. See below.
        """
        return pulumi.get(self, "provisioned_capacity")


@pulumi.output_type
class ConnectorCapacityAutoscaling(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxWorkerCount":
            suggest = "max_worker_count"
        elif key == "minWorkerCount":
            suggest = "min_worker_count"
        elif key == "mcuCount":
            suggest = "mcu_count"
        elif key == "scaleInPolicy":
            suggest = "scale_in_policy"
        elif key == "scaleOutPolicy":
            suggest = "scale_out_policy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorCapacityAutoscaling. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorCapacityAutoscaling.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorCapacityAutoscaling.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_worker_count: int,
                 min_worker_count: int,
                 mcu_count: Optional[int] = None,
                 scale_in_policy: Optional['outputs.ConnectorCapacityAutoscalingScaleInPolicy'] = None,
                 scale_out_policy: Optional['outputs.ConnectorCapacityAutoscalingScaleOutPolicy'] = None):
        """
        :param int max_worker_count: The maximum number of workers allocated to the connector.
        :param int min_worker_count: The minimum number of workers allocated to the connector.
        :param int mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. Valid values: `1`, `2`, `4`, `8`. The default value is `1`.
        :param 'ConnectorCapacityAutoscalingScaleInPolicyArgs' scale_in_policy: The scale-in policy for the connector. See below.
        :param 'ConnectorCapacityAutoscalingScaleOutPolicyArgs' scale_out_policy: The scale-out policy for the connector. See below.
        """
        pulumi.set(__self__, "max_worker_count", max_worker_count)
        pulumi.set(__self__, "min_worker_count", min_worker_count)
        if mcu_count is not None:
            pulumi.set(__self__, "mcu_count", mcu_count)
        if scale_in_policy is not None:
            pulumi.set(__self__, "scale_in_policy", scale_in_policy)
        if scale_out_policy is not None:
            pulumi.set(__self__, "scale_out_policy", scale_out_policy)

    @property
    @pulumi.getter(name="maxWorkerCount")
    def max_worker_count(self) -> int:
        """
        The maximum number of workers allocated to the connector.
        """
        return pulumi.get(self, "max_worker_count")

    @property
    @pulumi.getter(name="minWorkerCount")
    def min_worker_count(self) -> int:
        """
        The minimum number of workers allocated to the connector.
        """
        return pulumi.get(self, "min_worker_count")

    @property
    @pulumi.getter(name="mcuCount")
    def mcu_count(self) -> Optional[int]:
        """
        The number of microcontroller units (MCUs) allocated to each connector worker. Valid values: `1`, `2`, `4`, `8`. The default value is `1`.
        """
        return pulumi.get(self, "mcu_count")

    @property
    @pulumi.getter(name="scaleInPolicy")
    def scale_in_policy(self) -> Optional['outputs.ConnectorCapacityAutoscalingScaleInPolicy']:
        """
        The scale-in policy for the connector. See below.
        """
        return pulumi.get(self, "scale_in_policy")

    @property
    @pulumi.getter(name="scaleOutPolicy")
    def scale_out_policy(self) -> Optional['outputs.ConnectorCapacityAutoscalingScaleOutPolicy']:
        """
        The scale-out policy for the connector. See below.
        """
        return pulumi.get(self, "scale_out_policy")


@pulumi.output_type
class ConnectorCapacityAutoscalingScaleInPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cpuUtilizationPercentage":
            suggest = "cpu_utilization_percentage"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorCapacityAutoscalingScaleInPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorCapacityAutoscalingScaleInPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorCapacityAutoscalingScaleInPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu_utilization_percentage: Optional[int] = None):
        """
        :param int cpu_utilization_percentage: The CPU utilization percentage threshold at which you want connector scale out to be triggered.
        """
        if cpu_utilization_percentage is not None:
            pulumi.set(__self__, "cpu_utilization_percentage", cpu_utilization_percentage)

    @property
    @pulumi.getter(name="cpuUtilizationPercentage")
    def cpu_utilization_percentage(self) -> Optional[int]:
        """
        The CPU utilization percentage threshold at which you want connector scale out to be triggered.
        """
        return pulumi.get(self, "cpu_utilization_percentage")


@pulumi.output_type
class ConnectorCapacityAutoscalingScaleOutPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cpuUtilizationPercentage":
            suggest = "cpu_utilization_percentage"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorCapacityAutoscalingScaleOutPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorCapacityAutoscalingScaleOutPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorCapacityAutoscalingScaleOutPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu_utilization_percentage: Optional[int] = None):
        """
        :param int cpu_utilization_percentage: The CPU utilization percentage threshold at which you want connector scale out to be triggered.
        """
        if cpu_utilization_percentage is not None:
            pulumi.set(__self__, "cpu_utilization_percentage", cpu_utilization_percentage)

    @property
    @pulumi.getter(name="cpuUtilizationPercentage")
    def cpu_utilization_percentage(self) -> Optional[int]:
        """
        The CPU utilization percentage threshold at which you want connector scale out to be triggered.
        """
        return pulumi.get(self, "cpu_utilization_percentage")


@pulumi.output_type
class ConnectorCapacityProvisionedCapacity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "workerCount":
            suggest = "worker_count"
        elif key == "mcuCount":
            suggest = "mcu_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorCapacityProvisionedCapacity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorCapacityProvisionedCapacity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorCapacityProvisionedCapacity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 worker_count: int,
                 mcu_count: Optional[int] = None):
        """
        :param int worker_count: The number of workers that are allocated to the connector.
        :param int mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. Valid values: `1`, `2`, `4`, `8`. The default value is `1`.
        """
        pulumi.set(__self__, "worker_count", worker_count)
        if mcu_count is not None:
            pulumi.set(__self__, "mcu_count", mcu_count)

    @property
    @pulumi.getter(name="workerCount")
    def worker_count(self) -> int:
        """
        The number of workers that are allocated to the connector.
        """
        return pulumi.get(self, "worker_count")

    @property
    @pulumi.getter(name="mcuCount")
    def mcu_count(self) -> Optional[int]:
        """
        The number of microcontroller units (MCUs) allocated to each connector worker. Valid values: `1`, `2`, `4`, `8`. The default value is `1`.
        """
        return pulumi.get(self, "mcu_count")


@pulumi.output_type
class ConnectorKafkaCluster(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "apacheKafkaCluster":
            suggest = "apache_kafka_cluster"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorKafkaCluster. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorKafkaCluster.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorKafkaCluster.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 apache_kafka_cluster: 'outputs.ConnectorKafkaClusterApacheKafkaCluster'):
        """
        :param 'ConnectorKafkaClusterApacheKafkaClusterArgs' apache_kafka_cluster: The Apache Kafka cluster to which the connector is connected.
        """
        pulumi.set(__self__, "apache_kafka_cluster", apache_kafka_cluster)

    @property
    @pulumi.getter(name="apacheKafkaCluster")
    def apache_kafka_cluster(self) -> 'outputs.ConnectorKafkaClusterApacheKafkaCluster':
        """
        The Apache Kafka cluster to which the connector is connected.
        """
        return pulumi.get(self, "apache_kafka_cluster")


@pulumi.output_type
class ConnectorKafkaClusterApacheKafkaCluster(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bootstrapServers":
            suggest = "bootstrap_servers"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorKafkaClusterApacheKafkaCluster. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorKafkaClusterApacheKafkaCluster.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorKafkaClusterApacheKafkaCluster.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bootstrap_servers: str,
                 vpc: 'outputs.ConnectorKafkaClusterApacheKafkaClusterVpc'):
        """
        :param str bootstrap_servers: The bootstrap servers of the cluster.
        :param 'ConnectorKafkaClusterApacheKafkaClusterVpcArgs' vpc: Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.
        """
        pulumi.set(__self__, "bootstrap_servers", bootstrap_servers)
        pulumi.set(__self__, "vpc", vpc)

    @property
    @pulumi.getter(name="bootstrapServers")
    def bootstrap_servers(self) -> str:
        """
        The bootstrap servers of the cluster.
        """
        return pulumi.get(self, "bootstrap_servers")

    @property
    @pulumi.getter
    def vpc(self) -> 'outputs.ConnectorKafkaClusterApacheKafkaClusterVpc':
        """
        Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.
        """
        return pulumi.get(self, "vpc")


@pulumi.output_type
class ConnectorKafkaClusterApacheKafkaClusterVpc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroups":
            suggest = "security_groups"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorKafkaClusterApacheKafkaClusterVpc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorKafkaClusterApacheKafkaClusterVpc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorKafkaClusterApacheKafkaClusterVpc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 security_groups: Sequence[str],
                 subnets: Sequence[str]):
        """
        :param Sequence[str] security_groups: The security groups for the connector.
        :param Sequence[str] subnets: The subnets for the connector.
        """
        pulumi.set(__self__, "security_groups", security_groups)
        pulumi.set(__self__, "subnets", subnets)

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> Sequence[str]:
        """
        The security groups for the connector.
        """
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter
    def subnets(self) -> Sequence[str]:
        """
        The subnets for the connector.
        """
        return pulumi.get(self, "subnets")


@pulumi.output_type
class ConnectorKafkaClusterClientAuthentication(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "authenticationType":
            suggest = "authentication_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorKafkaClusterClientAuthentication. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorKafkaClusterClientAuthentication.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorKafkaClusterClientAuthentication.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authentication_type: Optional[str] = None):
        """
        :param str authentication_type: The type of client authentication used to connect to the Apache Kafka cluster. Valid values: `IAM`, `NONE`. A value of `NONE` means that no client authentication is used. The default value is `NONE`.
        """
        if authentication_type is not None:
            pulumi.set(__self__, "authentication_type", authentication_type)

    @property
    @pulumi.getter(name="authenticationType")
    def authentication_type(self) -> Optional[str]:
        """
        The type of client authentication used to connect to the Apache Kafka cluster. Valid values: `IAM`, `NONE`. A value of `NONE` means that no client authentication is used. The default value is `NONE`.
        """
        return pulumi.get(self, "authentication_type")


@pulumi.output_type
class ConnectorKafkaClusterEncryptionInTransit(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encryptionType":
            suggest = "encryption_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorKafkaClusterEncryptionInTransit. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorKafkaClusterEncryptionInTransit.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorKafkaClusterEncryptionInTransit.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 encryption_type: Optional[str] = None):
        """
        :param str encryption_type: The type of encryption in transit to the Apache Kafka cluster. Valid values: `PLAINTEXT`, `TLS`. The default values is `PLAINTEXT`.
        """
        if encryption_type is not None:
            pulumi.set(__self__, "encryption_type", encryption_type)

    @property
    @pulumi.getter(name="encryptionType")
    def encryption_type(self) -> Optional[str]:
        """
        The type of encryption in transit to the Apache Kafka cluster. Valid values: `PLAINTEXT`, `TLS`. The default values is `PLAINTEXT`.
        """
        return pulumi.get(self, "encryption_type")


@pulumi.output_type
class ConnectorLogDelivery(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "workerLogDelivery":
            suggest = "worker_log_delivery"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorLogDelivery. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorLogDelivery.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorLogDelivery.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 worker_log_delivery: 'outputs.ConnectorLogDeliveryWorkerLogDelivery'):
        """
        :param 'ConnectorLogDeliveryWorkerLogDeliveryArgs' worker_log_delivery: The workers can send worker logs to different destination types. This configuration specifies the details of these destinations. See below.
        """
        pulumi.set(__self__, "worker_log_delivery", worker_log_delivery)

    @property
    @pulumi.getter(name="workerLogDelivery")
    def worker_log_delivery(self) -> 'outputs.ConnectorLogDeliveryWorkerLogDelivery':
        """
        The workers can send worker logs to different destination types. This configuration specifies the details of these destinations. See below.
        """
        return pulumi.get(self, "worker_log_delivery")


@pulumi.output_type
class ConnectorLogDeliveryWorkerLogDelivery(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudwatchLogs":
            suggest = "cloudwatch_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorLogDeliveryWorkerLogDelivery. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorLogDeliveryWorkerLogDelivery.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorLogDeliveryWorkerLogDelivery.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloudwatch_logs: Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs'] = None,
                 firehose: Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryFirehose'] = None,
                 s3: Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryS3'] = None):
        """
        :param 'ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsArgs' cloudwatch_logs: Details about delivering logs to Amazon CloudWatch Logs. See below.
        :param 'ConnectorLogDeliveryWorkerLogDeliveryFirehoseArgs' firehose: Details about delivering logs to Amazon Kinesis Data Firehose. See below.
        :param 'ConnectorLogDeliveryWorkerLogDeliveryS3Args' s3: Details about delivering logs to Amazon S3. See below.
        """
        if cloudwatch_logs is not None:
            pulumi.set(__self__, "cloudwatch_logs", cloudwatch_logs)
        if firehose is not None:
            pulumi.set(__self__, "firehose", firehose)
        if s3 is not None:
            pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter(name="cloudwatchLogs")
    def cloudwatch_logs(self) -> Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs']:
        """
        Details about delivering logs to Amazon CloudWatch Logs. See below.
        """
        return pulumi.get(self, "cloudwatch_logs")

    @property
    @pulumi.getter
    def firehose(self) -> Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryFirehose']:
        """
        Details about delivering logs to Amazon Kinesis Data Firehose. See below.
        """
        return pulumi.get(self, "firehose")

    @property
    @pulumi.getter
    def s3(self) -> Optional['outputs.ConnectorLogDeliveryWorkerLogDeliveryS3']:
        """
        Details about delivering logs to Amazon S3. See below.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 log_group: Optional[str] = None):
        """
        :param bool enabled: Specifies whether connector logs get sent to the specified Amazon S3 destination.
        :param str log_group: The name of the CloudWatch log group that is the destination for log delivery.
        """
        pulumi.set(__self__, "enabled", enabled)
        if log_group is not None:
            pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Specifies whether connector logs get sent to the specified Amazon S3 destination.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> Optional[str]:
        """
        The name of the CloudWatch log group that is the destination for log delivery.
        """
        return pulumi.get(self, "log_group")


@pulumi.output_type
class ConnectorLogDeliveryWorkerLogDeliveryFirehose(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deliveryStream":
            suggest = "delivery_stream"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorLogDeliveryWorkerLogDeliveryFirehose. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorLogDeliveryWorkerLogDeliveryFirehose.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorLogDeliveryWorkerLogDeliveryFirehose.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 delivery_stream: Optional[str] = None):
        """
        :param bool enabled: Specifies whether connector logs get sent to the specified Amazon S3 destination.
        :param str delivery_stream: The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.
        """
        pulumi.set(__self__, "enabled", enabled)
        if delivery_stream is not None:
            pulumi.set(__self__, "delivery_stream", delivery_stream)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Specifies whether connector logs get sent to the specified Amazon S3 destination.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="deliveryStream")
    def delivery_stream(self) -> Optional[str]:
        """
        The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.
        """
        return pulumi.get(self, "delivery_stream")


@pulumi.output_type
class ConnectorLogDeliveryWorkerLogDeliveryS3(dict):
    def __init__(__self__, *,
                 enabled: bool,
                 bucket: Optional[str] = None,
                 prefix: Optional[str] = None):
        """
        :param bool enabled: Specifies whether connector logs get sent to the specified Amazon S3 destination.
        :param str bucket: The name of the S3 bucket that is the destination for log delivery.
        :param str prefix: The S3 prefix that is the destination for log delivery.
        """
        pulumi.set(__self__, "enabled", enabled)
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Specifies whether connector logs get sent to the specified Amazon S3 destination.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def bucket(self) -> Optional[str]:
        """
        The name of the S3 bucket that is the destination for log delivery.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        """
        The S3 prefix that is the destination for log delivery.
        """
        return pulumi.get(self, "prefix")


@pulumi.output_type
class ConnectorPlugin(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customPlugin":
            suggest = "custom_plugin"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectorPlugin. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectorPlugin.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectorPlugin.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 custom_plugin: 'outputs.ConnectorPluginCustomPlugin'):
        """
        :param 'ConnectorPluginCustomPluginArgs' custom_plugin: Details about a custom plugin. See below.
        """
        pulumi.set(__self__, "custom_plugin", custom_plugin)

    @property
    @pulumi.getter(name="customPlugin")
    def custom_plugin(self) -> 'outputs.ConnectorPluginCustomPlugin':
        """
        Details about a custom plugin. See below.
        """
        return pulumi.get(self, "custom_plugin")


@pulumi.output_type
class ConnectorPluginCustomPlugin(dict):
    def __init__(__self__, *,
                 arn: str,
                 revision: int):
        """
        :param str arn: The Amazon Resource Name (ARN) of the worker configuration.
        :param int revision: The revision of the worker configuration.
        """
        pulumi.set(__self__, "arn", arn)
        pulumi.set(__self__, "revision", revision)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the worker configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def revision(self) -> int:
        """
        The revision of the worker configuration.
        """
        return pulumi.get(self, "revision")


@pulumi.output_type
class ConnectorWorkerConfiguration(dict):
    def __init__(__self__, *,
                 arn: str,
                 revision: int):
        """
        :param str arn: The Amazon Resource Name (ARN) of the worker configuration.
        :param int revision: The revision of the worker configuration.
        """
        pulumi.set(__self__, "arn", arn)
        pulumi.set(__self__, "revision", revision)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the worker configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def revision(self) -> int:
        """
        The revision of the worker configuration.
        """
        return pulumi.get(self, "revision")


@pulumi.output_type
class CustomPluginLocation(dict):
    def __init__(__self__, *,
                 s3: 'outputs.CustomPluginLocationS3'):
        """
        :param 'CustomPluginLocationS3Args' s3: Information of the plugin file stored in Amazon S3. See below.
        """
        pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter
    def s3(self) -> 'outputs.CustomPluginLocationS3':
        """
        Information of the plugin file stored in Amazon S3. See below.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class CustomPluginLocationS3(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketArn":
            suggest = "bucket_arn"
        elif key == "fileKey":
            suggest = "file_key"
        elif key == "objectVersion":
            suggest = "object_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomPluginLocationS3. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomPluginLocationS3.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomPluginLocationS3.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_arn: str,
                 file_key: str,
                 object_version: Optional[str] = None):
        """
        :param str bucket_arn: The Amazon Resource Name (ARN) of an S3 bucket.
        :param str file_key: The file key for an object in an S3 bucket.
        :param str object_version: The version of an object in an S3 bucket.
        """
        pulumi.set(__self__, "bucket_arn", bucket_arn)
        pulumi.set(__self__, "file_key", file_key)
        if object_version is not None:
            pulumi.set(__self__, "object_version", object_version)

    @property
    @pulumi.getter(name="bucketArn")
    def bucket_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of an S3 bucket.
        """
        return pulumi.get(self, "bucket_arn")

    @property
    @pulumi.getter(name="fileKey")
    def file_key(self) -> str:
        """
        The file key for an object in an S3 bucket.
        """
        return pulumi.get(self, "file_key")

    @property
    @pulumi.getter(name="objectVersion")
    def object_version(self) -> Optional[str]:
        """
        The version of an object in an S3 bucket.
        """
        return pulumi.get(self, "object_version")


