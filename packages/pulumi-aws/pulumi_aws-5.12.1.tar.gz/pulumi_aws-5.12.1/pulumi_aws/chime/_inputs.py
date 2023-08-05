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
    'VoiceConnectorGroupConnectorArgs',
    'VoiceConnectorOrganizationRouteArgs',
    'VoiceConnectorTerminationCredentialsCredentialArgs',
]

@pulumi.input_type
class VoiceConnectorGroupConnectorArgs:
    def __init__(__self__, *,
                 priority: pulumi.Input[int],
                 voice_connector_id: pulumi.Input[str]):
        """
        :param pulumi.Input[int] priority: The priority associated with the Amazon Chime Voice Connector, with 1 being the highest priority. Higher priority Amazon Chime Voice Connectors are attempted first.
        :param pulumi.Input[str] voice_connector_id: The Amazon Chime Voice Connector ID.
        """
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "voice_connector_id", voice_connector_id)

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Input[int]:
        """
        The priority associated with the Amazon Chime Voice Connector, with 1 being the highest priority. Higher priority Amazon Chime Voice Connectors are attempted first.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: pulumi.Input[int]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="voiceConnectorId")
    def voice_connector_id(self) -> pulumi.Input[str]:
        """
        The Amazon Chime Voice Connector ID.
        """
        return pulumi.get(self, "voice_connector_id")

    @voice_connector_id.setter
    def voice_connector_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "voice_connector_id", value)


@pulumi.input_type
class VoiceConnectorOrganizationRouteArgs:
    def __init__(__self__, *,
                 host: pulumi.Input[str],
                 priority: pulumi.Input[int],
                 protocol: pulumi.Input[str],
                 weight: pulumi.Input[int],
                 port: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] host: The FQDN or IP address to contact for origination traffic.
        :param pulumi.Input[int] priority: The priority associated with the host, with 1 being the highest priority. Higher priority hosts are attempted first.
        :param pulumi.Input[str] protocol: The protocol to use for the origination route. Encryption-enabled Amazon Chime Voice Connectors use TCP protocol by default.
        :param pulumi.Input[int] weight: The weight associated with the host. If hosts are equal in priority, calls are redistributed among them based on their relative weight.
        :param pulumi.Input[int] port: The designated origination route port. Defaults to `5060`.
        """
        pulumi.set(__self__, "host", host)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "weight", weight)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def host(self) -> pulumi.Input[str]:
        """
        The FQDN or IP address to contact for origination traffic.
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: pulumi.Input[str]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Input[int]:
        """
        The priority associated with the host, with 1 being the highest priority. Higher priority hosts are attempted first.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: pulumi.Input[int]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        """
        The protocol to use for the origination route. Encryption-enabled Amazon Chime Voice Connectors use TCP protocol by default.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Input[int]:
        """
        The weight associated with the host. If hosts are equal in priority, calls are redistributed among them based on their relative weight.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: pulumi.Input[int]):
        pulumi.set(self, "weight", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The designated origination route port. Defaults to `5060`.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class VoiceConnectorTerminationCredentialsCredentialArgs:
    def __init__(__self__, *,
                 password: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        :param pulumi.Input[str] password: RFC2617 compliant password associated with the SIP credentials.
        :param pulumi.Input[str] username: RFC2617 compliant username associated with the SIP credentials.
        """
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        RFC2617 compliant password associated with the SIP credentials.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        RFC2617 compliant username associated with the SIP credentials.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


