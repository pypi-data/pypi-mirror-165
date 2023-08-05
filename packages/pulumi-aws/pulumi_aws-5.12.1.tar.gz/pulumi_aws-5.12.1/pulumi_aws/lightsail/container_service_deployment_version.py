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

__all__ = ['ContainerServiceDeploymentVersionArgs', 'ContainerServiceDeploymentVersion']

@pulumi.input_type
class ContainerServiceDeploymentVersionArgs:
    def __init__(__self__, *,
                 containers: pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]],
                 service_name: pulumi.Input[str],
                 public_endpoint: Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']] = None):
        """
        The set of arguments for constructing a ContainerServiceDeploymentVersion resource.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]] containers: A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        :param pulumi.Input[str] service_name: The name for the container service.
        :param pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs'] public_endpoint: A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        """
        pulumi.set(__self__, "containers", containers)
        pulumi.set(__self__, "service_name", service_name)
        if public_endpoint is not None:
            pulumi.set(__self__, "public_endpoint", public_endpoint)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]]:
        """
        A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        """
        return pulumi.get(self, "containers")

    @containers.setter
    def containers(self, value: pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]]):
        pulumi.set(self, "containers", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        The name for the container service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="publicEndpoint")
    def public_endpoint(self) -> Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']]:
        """
        A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        """
        return pulumi.get(self, "public_endpoint")

    @public_endpoint.setter
    def public_endpoint(self, value: Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']]):
        pulumi.set(self, "public_endpoint", value)


@pulumi.input_type
class _ContainerServiceDeploymentVersionState:
    def __init__(__self__, *,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 public_endpoint: Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ContainerServiceDeploymentVersion resources.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]] containers: A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        :param pulumi.Input[str] created_at: The timestamp when the deployment was created.
        :param pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs'] public_endpoint: A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        :param pulumi.Input[str] service_name: The name for the container service.
        :param pulumi.Input[str] state: The current state of the container service.
        :param pulumi.Input[int] version: The version number of the deployment.
        """
        if containers is not None:
            pulumi.set(__self__, "containers", containers)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if public_endpoint is not None:
            pulumi.set(__self__, "public_endpoint", public_endpoint)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def containers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]]]:
        """
        A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        """
        return pulumi.get(self, "containers")

    @containers.setter
    def containers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceDeploymentVersionContainerArgs']]]]):
        pulumi.set(self, "containers", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the deployment was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="publicEndpoint")
    def public_endpoint(self) -> Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']]:
        """
        A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        """
        return pulumi.get(self, "public_endpoint")

    @public_endpoint.setter
    def public_endpoint(self, value: Optional[pulumi.Input['ContainerServiceDeploymentVersionPublicEndpointArgs']]):
        pulumi.set(self, "public_endpoint", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the container service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the container service.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        The version number of the deployment.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


class ContainerServiceDeploymentVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionContainerArgs']]]]] = None,
                 public_endpoint: Optional[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionPublicEndpointArgs']]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.lightsail.ContainerServiceDeploymentVersion("example",
            containers=[aws.lightsail.ContainerServiceDeploymentVersionContainerArgs(
                container_name="hello-world",
                image="amazon/amazon-lightsail:hello-world",
                commands=[],
                environment={
                    "MY_ENVIRONMENT_VARIABLE": "my_value",
                },
                ports={
                    "80": "HTTP",
                },
            )],
            public_endpoint=aws.lightsail.ContainerServiceDeploymentVersionPublicEndpointArgs(
                container_name="hello-world",
                container_port=80,
                health_check=aws.lightsail.ContainerServiceDeploymentVersionPublicEndpointHealthCheckArgs(
                    healthy_threshold=2,
                    unhealthy_threshold=2,
                    timeout_seconds=2,
                    interval_seconds=5,
                    path="/",
                    success_codes="200-499",
                ),
            ),
            service_name=aws_lightsail_container_service["example"]["name"])
        ```

        ## Import

        Lightsail Container Service Deployment Version can be imported using the `service_name` and `version` separated by a slash (`/`), e.g.,

        ```sh
         $ pulumi import aws:lightsail/containerServiceDeploymentVersion:ContainerServiceDeploymentVersion example container-service-1/1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionContainerArgs']]]] containers: A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        :param pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionPublicEndpointArgs']] public_endpoint: A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        :param pulumi.Input[str] service_name: The name for the container service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerServiceDeploymentVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.lightsail.ContainerServiceDeploymentVersion("example",
            containers=[aws.lightsail.ContainerServiceDeploymentVersionContainerArgs(
                container_name="hello-world",
                image="amazon/amazon-lightsail:hello-world",
                commands=[],
                environment={
                    "MY_ENVIRONMENT_VARIABLE": "my_value",
                },
                ports={
                    "80": "HTTP",
                },
            )],
            public_endpoint=aws.lightsail.ContainerServiceDeploymentVersionPublicEndpointArgs(
                container_name="hello-world",
                container_port=80,
                health_check=aws.lightsail.ContainerServiceDeploymentVersionPublicEndpointHealthCheckArgs(
                    healthy_threshold=2,
                    unhealthy_threshold=2,
                    timeout_seconds=2,
                    interval_seconds=5,
                    path="/",
                    success_codes="200-499",
                ),
            ),
            service_name=aws_lightsail_container_service["example"]["name"])
        ```

        ## Import

        Lightsail Container Service Deployment Version can be imported using the `service_name` and `version` separated by a slash (`/`), e.g.,

        ```sh
         $ pulumi import aws:lightsail/containerServiceDeploymentVersion:ContainerServiceDeploymentVersion example container-service-1/1
        ```

        :param str resource_name: The name of the resource.
        :param ContainerServiceDeploymentVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerServiceDeploymentVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionContainerArgs']]]]] = None,
                 public_endpoint: Optional[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionPublicEndpointArgs']]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerServiceDeploymentVersionArgs.__new__(ContainerServiceDeploymentVersionArgs)

            if containers is None and not opts.urn:
                raise TypeError("Missing required property 'containers'")
            __props__.__dict__["containers"] = containers
            __props__.__dict__["public_endpoint"] = public_endpoint
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["created_at"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["version"] = None
        super(ContainerServiceDeploymentVersion, __self__).__init__(
            'aws:lightsail/containerServiceDeploymentVersion:ContainerServiceDeploymentVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionContainerArgs']]]]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            public_endpoint: Optional[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionPublicEndpointArgs']]] = None,
            service_name: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'ContainerServiceDeploymentVersion':
        """
        Get an existing ContainerServiceDeploymentVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionContainerArgs']]]] containers: A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        :param pulumi.Input[str] created_at: The timestamp when the deployment was created.
        :param pulumi.Input[pulumi.InputType['ContainerServiceDeploymentVersionPublicEndpointArgs']] public_endpoint: A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        :param pulumi.Input[str] service_name: The name for the container service.
        :param pulumi.Input[str] state: The current state of the container service.
        :param pulumi.Input[int] version: The version number of the deployment.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContainerServiceDeploymentVersionState.__new__(_ContainerServiceDeploymentVersionState)

        __props__.__dict__["containers"] = containers
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["public_endpoint"] = public_endpoint
        __props__.__dict__["service_name"] = service_name
        __props__.__dict__["state"] = state
        __props__.__dict__["version"] = version
        return ContainerServiceDeploymentVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Sequence['outputs.ContainerServiceDeploymentVersionContainer']]:
        """
        A set of configuration blocks that describe the settings of the containers that will be launched on the container service. Maximum of 53. Detailed below.
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The timestamp when the deployment was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="publicEndpoint")
    def public_endpoint(self) -> pulumi.Output[Optional['outputs.ContainerServiceDeploymentVersionPublicEndpoint']]:
        """
        A configuration block that describes the settings of the public endpoint for the container service. Detailed below.
        """
        return pulumi.get(self, "public_endpoint")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Output[str]:
        """
        The name for the container service.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the container service.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        The version number of the deployment.
        """
        return pulumi.get(self, "version")

