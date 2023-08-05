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
    'GetCertificateResult',
    'AwaitableGetCertificateResult',
    'get_certificate',
    'get_certificate_output',
]

@pulumi.output_type
class GetCertificateResult:
    """
    A collection of values returned by getCertificate.
    """
    def __init__(__self__, arn=None, certificate=None, certificate_authority_arn=None, certificate_chain=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if certificate and not isinstance(certificate, str):
            raise TypeError("Expected argument 'certificate' to be a str")
        pulumi.set(__self__, "certificate", certificate)
        if certificate_authority_arn and not isinstance(certificate_authority_arn, str):
            raise TypeError("Expected argument 'certificate_authority_arn' to be a str")
        pulumi.set(__self__, "certificate_authority_arn", certificate_authority_arn)
        if certificate_chain and not isinstance(certificate_chain, str):
            raise TypeError("Expected argument 'certificate_chain' to be a str")
        pulumi.set(__self__, "certificate_chain", certificate_chain)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def certificate(self) -> str:
        """
        The PEM-encoded certificate value.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> str:
        return pulumi.get(self, "certificate_authority_arn")

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> str:
        """
        The PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA.
        """
        return pulumi.get(self, "certificate_chain")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            arn=self.arn,
            certificate=self.certificate,
            certificate_authority_arn=self.certificate_authority_arn,
            certificate_chain=self.certificate_chain,
            id=self.id)


def get_certificate(arn: Optional[str] = None,
                    certificate_authority_arn: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificateResult:
    """
    Get information on a Certificate issued by a AWS Certificate Manager Private Certificate Authority.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.acmpca.get_certificate(arn="arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012/certificate/1234b4a0d73e2056789bdbe77d5b1a23",
        certificate_authority_arn="arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012")
    ```


    :param str arn: Amazon Resource Name (ARN) of the certificate issued by the private certificate authority.
    :param str certificate_authority_arn: Amazon Resource Name (ARN) of the certificate authority.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['certificateAuthorityArn'] = certificate_authority_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:acmpca/getCertificate:getCertificate', __args__, opts=opts, typ=GetCertificateResult).value

    return AwaitableGetCertificateResult(
        arn=__ret__.arn,
        certificate=__ret__.certificate,
        certificate_authority_arn=__ret__.certificate_authority_arn,
        certificate_chain=__ret__.certificate_chain,
        id=__ret__.id)


@_utilities.lift_output_func(get_certificate)
def get_certificate_output(arn: Optional[pulumi.Input[str]] = None,
                           certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCertificateResult]:
    """
    Get information on a Certificate issued by a AWS Certificate Manager Private Certificate Authority.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.acmpca.get_certificate(arn="arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012/certificate/1234b4a0d73e2056789bdbe77d5b1a23",
        certificate_authority_arn="arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012")
    ```


    :param str arn: Amazon Resource Name (ARN) of the certificate issued by the private certificate authority.
    :param str certificate_authority_arn: Amazon Resource Name (ARN) of the certificate authority.
    """
    ...
