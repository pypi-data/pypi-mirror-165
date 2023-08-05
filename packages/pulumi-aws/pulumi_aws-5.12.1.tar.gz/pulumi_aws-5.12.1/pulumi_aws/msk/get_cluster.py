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
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    """
    A collection of values returned by getCluster.
    """
    def __init__(__self__, arn=None, bootstrap_brokers=None, bootstrap_brokers_public_sasl_iam=None, bootstrap_brokers_public_sasl_scram=None, bootstrap_brokers_public_tls=None, bootstrap_brokers_sasl_iam=None, bootstrap_brokers_sasl_scram=None, bootstrap_brokers_tls=None, cluster_name=None, id=None, kafka_version=None, number_of_broker_nodes=None, tags=None, zookeeper_connect_string=None, zookeeper_connect_string_tls=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if bootstrap_brokers and not isinstance(bootstrap_brokers, str):
            raise TypeError("Expected argument 'bootstrap_brokers' to be a str")
        pulumi.set(__self__, "bootstrap_brokers", bootstrap_brokers)
        if bootstrap_brokers_public_sasl_iam and not isinstance(bootstrap_brokers_public_sasl_iam, str):
            raise TypeError("Expected argument 'bootstrap_brokers_public_sasl_iam' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_public_sasl_iam", bootstrap_brokers_public_sasl_iam)
        if bootstrap_brokers_public_sasl_scram and not isinstance(bootstrap_brokers_public_sasl_scram, str):
            raise TypeError("Expected argument 'bootstrap_brokers_public_sasl_scram' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_public_sasl_scram", bootstrap_brokers_public_sasl_scram)
        if bootstrap_brokers_public_tls and not isinstance(bootstrap_brokers_public_tls, str):
            raise TypeError("Expected argument 'bootstrap_brokers_public_tls' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_public_tls", bootstrap_brokers_public_tls)
        if bootstrap_brokers_sasl_iam and not isinstance(bootstrap_brokers_sasl_iam, str):
            raise TypeError("Expected argument 'bootstrap_brokers_sasl_iam' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_sasl_iam", bootstrap_brokers_sasl_iam)
        if bootstrap_brokers_sasl_scram and not isinstance(bootstrap_brokers_sasl_scram, str):
            raise TypeError("Expected argument 'bootstrap_brokers_sasl_scram' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_sasl_scram", bootstrap_brokers_sasl_scram)
        if bootstrap_brokers_tls and not isinstance(bootstrap_brokers_tls, str):
            raise TypeError("Expected argument 'bootstrap_brokers_tls' to be a str")
        pulumi.set(__self__, "bootstrap_brokers_tls", bootstrap_brokers_tls)
        if cluster_name and not isinstance(cluster_name, str):
            raise TypeError("Expected argument 'cluster_name' to be a str")
        pulumi.set(__self__, "cluster_name", cluster_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kafka_version and not isinstance(kafka_version, str):
            raise TypeError("Expected argument 'kafka_version' to be a str")
        pulumi.set(__self__, "kafka_version", kafka_version)
        if number_of_broker_nodes and not isinstance(number_of_broker_nodes, int):
            raise TypeError("Expected argument 'number_of_broker_nodes' to be a int")
        pulumi.set(__self__, "number_of_broker_nodes", number_of_broker_nodes)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if zookeeper_connect_string and not isinstance(zookeeper_connect_string, str):
            raise TypeError("Expected argument 'zookeeper_connect_string' to be a str")
        pulumi.set(__self__, "zookeeper_connect_string", zookeeper_connect_string)
        if zookeeper_connect_string_tls and not isinstance(zookeeper_connect_string_tls, str):
            raise TypeError("Expected argument 'zookeeper_connect_string_tls' to be a str")
        pulumi.set(__self__, "zookeeper_connect_string_tls", zookeeper_connect_string_tls)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the MSK cluster.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="bootstrapBrokers")
    def bootstrap_brokers(self) -> str:
        """
        Comma separated list of one or more hostname:port pairs of kafka brokers suitable to bootstrap connectivity to the kafka cluster. Contains a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `PLAINTEXT` or `TLS_PLAINTEXT`. The resource sorts values alphabetically. AWS may not always return all endpoints so this value is not guaranteed to be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers")

    @property
    @pulumi.getter(name="bootstrapBrokersPublicSaslIam")
    def bootstrap_brokers_public_sasl_iam(self) -> str:
        """
        One or more DNS names (or IP addresses) and SASL IAM port pairs. For example, `b-1-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9198,b-2-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9198,b-3-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9198`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS` and `client_authentication.0.sasl.0.iam` is set to `true` and `broker_node_group_info.0.connectivity_info.0.public_access.0.type` is set to `SERVICE_PROVIDED_EIPS` and the cluster fulfill all other requirements for public access. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_public_sasl_iam")

    @property
    @pulumi.getter(name="bootstrapBrokersPublicSaslScram")
    def bootstrap_brokers_public_sasl_scram(self) -> str:
        """
        One or more DNS names (or IP addresses) and SASL SCRAM port pairs. For example, `b-1-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9196,b-2-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9196,b-3-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9196`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS` and `client_authentication.0.sasl.0.scram` is set to `true` and `broker_node_group_info.0.connectivity_info.0.public_access.0.type` is set to `SERVICE_PROVIDED_EIPS` and the cluster fulfill all other requirements for public access. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_public_sasl_scram")

    @property
    @pulumi.getter(name="bootstrapBrokersPublicTls")
    def bootstrap_brokers_public_tls(self) -> str:
        """
        One or more DNS names (or IP addresses) and TLS port pairs. For example, `b-1-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9194,b-2-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9194,b-3-public.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9194`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS` and `broker_node_group_info.0.connectivity_info.0.public_access.0.type` is set to `SERVICE_PROVIDED_EIPS` and the cluster fulfill all other requirements for public access. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_public_tls")

    @property
    @pulumi.getter(name="bootstrapBrokersSaslIam")
    def bootstrap_brokers_sasl_iam(self) -> str:
        """
        One or more DNS names (or IP addresses) and SASL IAM port pairs. For example, `b-1.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9098,b-2.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9098,b-3.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9098`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS` and `client_authentication.0.sasl.0.iam` is set to `true`. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_sasl_iam")

    @property
    @pulumi.getter(name="bootstrapBrokersSaslScram")
    def bootstrap_brokers_sasl_scram(self) -> str:
        """
        One or more DNS names (or IP addresses) and SASL SCRAM port pairs. For example, `b-1.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9096,b-2.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9096,b-3.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9096`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS` and `client_authentication.0.sasl.0.scram` is set to `true`. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_sasl_scram")

    @property
    @pulumi.getter(name="bootstrapBrokersTls")
    def bootstrap_brokers_tls(self) -> str:
        """
        One or more DNS names (or IP addresses) and TLS port pairs. For example, `b-1.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9094,b-2.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9094,b-3.exampleClusterName.abcde.c2.kafka.us-east-1.amazonaws.com:9094`. This attribute will have a value if `encryption_info.0.encryption_in_transit.0.client_broker` is set to `TLS_PLAINTEXT` or `TLS`. The resource sorts the list alphabetically. AWS may not always return all endpoints so the values may not be stable across applies.
        """
        return pulumi.get(self, "bootstrap_brokers_tls")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> str:
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kafkaVersion")
    def kafka_version(self) -> str:
        """
        Apache Kafka version.
        """
        return pulumi.get(self, "kafka_version")

    @property
    @pulumi.getter(name="numberOfBrokerNodes")
    def number_of_broker_nodes(self) -> int:
        """
        Number of broker nodes in the cluster.
        """
        return pulumi.get(self, "number_of_broker_nodes")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of key-value pairs assigned to the cluster.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="zookeeperConnectString")
    def zookeeper_connect_string(self) -> str:
        """
        A comma separated list of one or more hostname:port pairs to use to connect to the Apache Zookeeper cluster. The returned values are sorted alphbetically. The AWS API may not return all endpoints, so this value is not guaranteed to be stable across applies.
        """
        return pulumi.get(self, "zookeeper_connect_string")

    @property
    @pulumi.getter(name="zookeeperConnectStringTls")
    def zookeeper_connect_string_tls(self) -> str:
        """
        A comma separated list of one or more hostname:port pairs to use to connect to the Apache Zookeeper cluster via TLS. The returned values are sorted alphabetically. The AWS API may not return all endpoints, so this value is not guaranteed to be stable across applies.
        """
        return pulumi.get(self, "zookeeper_connect_string_tls")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            arn=self.arn,
            bootstrap_brokers=self.bootstrap_brokers,
            bootstrap_brokers_public_sasl_iam=self.bootstrap_brokers_public_sasl_iam,
            bootstrap_brokers_public_sasl_scram=self.bootstrap_brokers_public_sasl_scram,
            bootstrap_brokers_public_tls=self.bootstrap_brokers_public_tls,
            bootstrap_brokers_sasl_iam=self.bootstrap_brokers_sasl_iam,
            bootstrap_brokers_sasl_scram=self.bootstrap_brokers_sasl_scram,
            bootstrap_brokers_tls=self.bootstrap_brokers_tls,
            cluster_name=self.cluster_name,
            id=self.id,
            kafka_version=self.kafka_version,
            number_of_broker_nodes=self.number_of_broker_nodes,
            tags=self.tags,
            zookeeper_connect_string=self.zookeeper_connect_string,
            zookeeper_connect_string_tls=self.zookeeper_connect_string_tls)


def get_cluster(cluster_name: Optional[str] = None,
                tags: Optional[Mapping[str, str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Get information on an Amazon MSK Cluster.

    > **Note:** This data sources returns information on _provisioned_ clusters.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.msk.get_cluster(cluster_name="example")
    ```


    :param str cluster_name: Name of the cluster.
    :param Mapping[str, str] tags: Map of key-value pairs assigned to the cluster.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:msk/getCluster:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        arn=__ret__.arn,
        bootstrap_brokers=__ret__.bootstrap_brokers,
        bootstrap_brokers_public_sasl_iam=__ret__.bootstrap_brokers_public_sasl_iam,
        bootstrap_brokers_public_sasl_scram=__ret__.bootstrap_brokers_public_sasl_scram,
        bootstrap_brokers_public_tls=__ret__.bootstrap_brokers_public_tls,
        bootstrap_brokers_sasl_iam=__ret__.bootstrap_brokers_sasl_iam,
        bootstrap_brokers_sasl_scram=__ret__.bootstrap_brokers_sasl_scram,
        bootstrap_brokers_tls=__ret__.bootstrap_brokers_tls,
        cluster_name=__ret__.cluster_name,
        id=__ret__.id,
        kafka_version=__ret__.kafka_version,
        number_of_broker_nodes=__ret__.number_of_broker_nodes,
        tags=__ret__.tags,
        zookeeper_connect_string=__ret__.zookeeper_connect_string,
        zookeeper_connect_string_tls=__ret__.zookeeper_connect_string_tls)


@_utilities.lift_output_func(get_cluster)
def get_cluster_output(cluster_name: Optional[pulumi.Input[str]] = None,
                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Get information on an Amazon MSK Cluster.

    > **Note:** This data sources returns information on _provisioned_ clusters.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.msk.get_cluster(cluster_name="example")
    ```


    :param str cluster_name: Name of the cluster.
    :param Mapping[str, str] tags: Map of key-value pairs assigned to the cluster.
    """
    ...
