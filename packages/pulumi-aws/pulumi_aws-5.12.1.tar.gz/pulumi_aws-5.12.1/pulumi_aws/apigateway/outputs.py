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
    'AccountThrottleSetting',
    'DocumentationPartLocation',
    'DomainNameEndpointConfiguration',
    'DomainNameMutualTlsAuthentication',
    'IntegrationTlsConfig',
    'MethodSettingsSettings',
    'RestApiEndpointConfiguration',
    'StageAccessLogSettings',
    'StageCanarySettings',
    'UsagePlanApiStage',
    'UsagePlanApiStageThrottle',
    'UsagePlanQuotaSettings',
    'UsagePlanThrottleSettings',
    'GetDomainNameEndpointConfigurationResult',
    'GetRestApiEndpointConfigurationResult',
]

@pulumi.output_type
class AccountThrottleSetting(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "burstLimit":
            suggest = "burst_limit"
        elif key == "rateLimit":
            suggest = "rate_limit"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccountThrottleSetting. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccountThrottleSetting.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccountThrottleSetting.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 burst_limit: Optional[int] = None,
                 rate_limit: Optional[float] = None):
        """
        :param int burst_limit: The absolute maximum number of times API Gateway allows the API to be called per second (RPS).
        :param float rate_limit: The number of times API Gateway allows the API to be called per second on average (RPS).
        """
        if burst_limit is not None:
            pulumi.set(__self__, "burst_limit", burst_limit)
        if rate_limit is not None:
            pulumi.set(__self__, "rate_limit", rate_limit)

    @property
    @pulumi.getter(name="burstLimit")
    def burst_limit(self) -> Optional[int]:
        """
        The absolute maximum number of times API Gateway allows the API to be called per second (RPS).
        """
        return pulumi.get(self, "burst_limit")

    @property
    @pulumi.getter(name="rateLimit")
    def rate_limit(self) -> Optional[float]:
        """
        The number of times API Gateway allows the API to be called per second on average (RPS).
        """
        return pulumi.get(self, "rate_limit")


@pulumi.output_type
class DocumentationPartLocation(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "statusCode":
            suggest = "status_code"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DocumentationPartLocation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DocumentationPartLocation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DocumentationPartLocation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 method: Optional[str] = None,
                 name: Optional[str] = None,
                 path: Optional[str] = None,
                 status_code: Optional[str] = None):
        """
        :param str type: The type of API entity to which the documentation content appliesE.g., `API`, `METHOD` or `REQUEST_BODY`
        :param str method: The HTTP verb of a method. The default value is `*` for any method.
        :param str name: The name of the targeted API entity.
        :param str path: The URL path of the target. The default value is `/` for the root resource.
        :param str status_code: The HTTP status code of a response. The default value is `*` for any status code.
        """
        pulumi.set(__self__, "type", type)
        if method is not None:
            pulumi.set(__self__, "method", method)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if status_code is not None:
            pulumi.set(__self__, "status_code", status_code)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of API entity to which the documentation content appliesE.g., `API`, `METHOD` or `REQUEST_BODY`
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def method(self) -> Optional[str]:
        """
        The HTTP verb of a method. The default value is `*` for any method.
        """
        return pulumi.get(self, "method")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the targeted API entity.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        The URL path of the target. The default value is `/` for the root resource.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="statusCode")
    def status_code(self) -> Optional[str]:
        """
        The HTTP status code of a response. The default value is `*` for any status code.
        """
        return pulumi.get(self, "status_code")


@pulumi.output_type
class DomainNameEndpointConfiguration(dict):
    def __init__(__self__, *,
                 types: str):
        """
        :param str types: List of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE` or `REGIONAL`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        pulumi.set(__self__, "types", types)

    @property
    @pulumi.getter
    def types(self) -> str:
        """
        List of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE` or `REGIONAL`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        return pulumi.get(self, "types")


@pulumi.output_type
class DomainNameMutualTlsAuthentication(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "truststoreUri":
            suggest = "truststore_uri"
        elif key == "truststoreVersion":
            suggest = "truststore_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainNameMutualTlsAuthentication. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainNameMutualTlsAuthentication.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainNameMutualTlsAuthentication.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 truststore_uri: str,
                 truststore_version: Optional[str] = None):
        """
        :param str truststore_uri: Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, `s3://bucket-name/key-name`. The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version.
        :param str truststore_version: Version of the S3 object that contains the truststore. To specify a version, you must have versioning enabled for the S3 bucket.
        """
        pulumi.set(__self__, "truststore_uri", truststore_uri)
        if truststore_version is not None:
            pulumi.set(__self__, "truststore_version", truststore_version)

    @property
    @pulumi.getter(name="truststoreUri")
    def truststore_uri(self) -> str:
        """
        Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, `s3://bucket-name/key-name`. The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version.
        """
        return pulumi.get(self, "truststore_uri")

    @property
    @pulumi.getter(name="truststoreVersion")
    def truststore_version(self) -> Optional[str]:
        """
        Version of the S3 object that contains the truststore. To specify a version, you must have versioning enabled for the S3 bucket.
        """
        return pulumi.get(self, "truststore_version")


@pulumi.output_type
class IntegrationTlsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "insecureSkipVerification":
            suggest = "insecure_skip_verification"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationTlsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationTlsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationTlsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 insecure_skip_verification: Optional[bool] = None):
        """
        :param bool insecure_skip_verification: Specifies whether or not API Gateway skips verification that the certificate for an integration endpoint is issued by a [supported certificate authority](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-supported-certificate-authorities-for-http-endpoints.html). This isn’t recommended, but it enables you to use certificates that are signed by private certificate authorities, or certificates that are self-signed. If enabled, API Gateway still performs basic certificate validation, which includes checking the certificate's expiration date, hostname, and presence of a root certificate authority. Supported only for `HTTP` and `HTTP_PROXY` integrations.
        """
        if insecure_skip_verification is not None:
            pulumi.set(__self__, "insecure_skip_verification", insecure_skip_verification)

    @property
    @pulumi.getter(name="insecureSkipVerification")
    def insecure_skip_verification(self) -> Optional[bool]:
        """
        Specifies whether or not API Gateway skips verification that the certificate for an integration endpoint is issued by a [supported certificate authority](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-supported-certificate-authorities-for-http-endpoints.html). This isn’t recommended, but it enables you to use certificates that are signed by private certificate authorities, or certificates that are self-signed. If enabled, API Gateway still performs basic certificate validation, which includes checking the certificate's expiration date, hostname, and presence of a root certificate authority. Supported only for `HTTP` and `HTTP_PROXY` integrations.
        """
        return pulumi.get(self, "insecure_skip_verification")


@pulumi.output_type
class MethodSettingsSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cacheDataEncrypted":
            suggest = "cache_data_encrypted"
        elif key == "cacheTtlInSeconds":
            suggest = "cache_ttl_in_seconds"
        elif key == "cachingEnabled":
            suggest = "caching_enabled"
        elif key == "dataTraceEnabled":
            suggest = "data_trace_enabled"
        elif key == "loggingLevel":
            suggest = "logging_level"
        elif key == "metricsEnabled":
            suggest = "metrics_enabled"
        elif key == "requireAuthorizationForCacheControl":
            suggest = "require_authorization_for_cache_control"
        elif key == "throttlingBurstLimit":
            suggest = "throttling_burst_limit"
        elif key == "throttlingRateLimit":
            suggest = "throttling_rate_limit"
        elif key == "unauthorizedCacheControlHeaderStrategy":
            suggest = "unauthorized_cache_control_header_strategy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MethodSettingsSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MethodSettingsSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MethodSettingsSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cache_data_encrypted: Optional[bool] = None,
                 cache_ttl_in_seconds: Optional[int] = None,
                 caching_enabled: Optional[bool] = None,
                 data_trace_enabled: Optional[bool] = None,
                 logging_level: Optional[str] = None,
                 metrics_enabled: Optional[bool] = None,
                 require_authorization_for_cache_control: Optional[bool] = None,
                 throttling_burst_limit: Optional[int] = None,
                 throttling_rate_limit: Optional[float] = None,
                 unauthorized_cache_control_header_strategy: Optional[str] = None):
        """
        :param bool cache_data_encrypted: Specifies whether the cached responses are encrypted.
        :param int cache_ttl_in_seconds: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
        :param bool caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
        :param bool data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.
        :param str logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. The available levels are `OFF`, `ERROR`, and `INFO`.
        :param bool metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method.
        :param bool require_authorization_for_cache_control: Specifies whether authorization is required for a cache invalidation request.
        :param int throttling_burst_limit: Specifies the throttling burst limit. Default: `-1` (throttling disabled).
        :param float throttling_rate_limit: Specifies the throttling rate limit. Default: `-1` (throttling disabled).
        :param str unauthorized_cache_control_header_strategy: Specifies how to handle unauthorized requests for cache invalidation. The available values are `FAIL_WITH_403`, `SUCCEED_WITH_RESPONSE_HEADER`, `SUCCEED_WITHOUT_RESPONSE_HEADER`.
        """
        if cache_data_encrypted is not None:
            pulumi.set(__self__, "cache_data_encrypted", cache_data_encrypted)
        if cache_ttl_in_seconds is not None:
            pulumi.set(__self__, "cache_ttl_in_seconds", cache_ttl_in_seconds)
        if caching_enabled is not None:
            pulumi.set(__self__, "caching_enabled", caching_enabled)
        if data_trace_enabled is not None:
            pulumi.set(__self__, "data_trace_enabled", data_trace_enabled)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if metrics_enabled is not None:
            pulumi.set(__self__, "metrics_enabled", metrics_enabled)
        if require_authorization_for_cache_control is not None:
            pulumi.set(__self__, "require_authorization_for_cache_control", require_authorization_for_cache_control)
        if throttling_burst_limit is not None:
            pulumi.set(__self__, "throttling_burst_limit", throttling_burst_limit)
        if throttling_rate_limit is not None:
            pulumi.set(__self__, "throttling_rate_limit", throttling_rate_limit)
        if unauthorized_cache_control_header_strategy is not None:
            pulumi.set(__self__, "unauthorized_cache_control_header_strategy", unauthorized_cache_control_header_strategy)

    @property
    @pulumi.getter(name="cacheDataEncrypted")
    def cache_data_encrypted(self) -> Optional[bool]:
        """
        Specifies whether the cached responses are encrypted.
        """
        return pulumi.get(self, "cache_data_encrypted")

    @property
    @pulumi.getter(name="cacheTtlInSeconds")
    def cache_ttl_in_seconds(self) -> Optional[int]:
        """
        Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
        """
        return pulumi.get(self, "cache_ttl_in_seconds")

    @property
    @pulumi.getter(name="cachingEnabled")
    def caching_enabled(self) -> Optional[bool]:
        """
        Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
        """
        return pulumi.get(self, "caching_enabled")

    @property
    @pulumi.getter(name="dataTraceEnabled")
    def data_trace_enabled(self) -> Optional[bool]:
        """
        Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "data_trace_enabled")

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[str]:
        """
        Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. The available levels are `OFF`, `ERROR`, and `INFO`.
        """
        return pulumi.get(self, "logging_level")

    @property
    @pulumi.getter(name="metricsEnabled")
    def metrics_enabled(self) -> Optional[bool]:
        """
        Specifies whether Amazon CloudWatch metrics are enabled for this method.
        """
        return pulumi.get(self, "metrics_enabled")

    @property
    @pulumi.getter(name="requireAuthorizationForCacheControl")
    def require_authorization_for_cache_control(self) -> Optional[bool]:
        """
        Specifies whether authorization is required for a cache invalidation request.
        """
        return pulumi.get(self, "require_authorization_for_cache_control")

    @property
    @pulumi.getter(name="throttlingBurstLimit")
    def throttling_burst_limit(self) -> Optional[int]:
        """
        Specifies the throttling burst limit. Default: `-1` (throttling disabled).
        """
        return pulumi.get(self, "throttling_burst_limit")

    @property
    @pulumi.getter(name="throttlingRateLimit")
    def throttling_rate_limit(self) -> Optional[float]:
        """
        Specifies the throttling rate limit. Default: `-1` (throttling disabled).
        """
        return pulumi.get(self, "throttling_rate_limit")

    @property
    @pulumi.getter(name="unauthorizedCacheControlHeaderStrategy")
    def unauthorized_cache_control_header_strategy(self) -> Optional[str]:
        """
        Specifies how to handle unauthorized requests for cache invalidation. The available values are `FAIL_WITH_403`, `SUCCEED_WITH_RESPONSE_HEADER`, `SUCCEED_WITHOUT_RESPONSE_HEADER`.
        """
        return pulumi.get(self, "unauthorized_cache_control_header_strategy")


@pulumi.output_type
class RestApiEndpointConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vpcEndpointIds":
            suggest = "vpc_endpoint_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RestApiEndpointConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RestApiEndpointConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RestApiEndpointConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 types: str,
                 vpc_endpoint_ids: Optional[Sequence[str]] = None):
        """
        :param str types: A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE`, `REGIONAL` or `PRIVATE`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. If set to `PRIVATE` recommend to set `put_rest_api_mode` = `merge` to not cause the endpoints and associated Route53 records to be deleted. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        :param Sequence[str] vpc_endpoint_ids: Set of VPC Endpoint identifiers. It is only supported for `PRIVATE` endpoint type. If importing an OpenAPI specification via the `body` argument, this corresponds to the [`x-amazon-apigateway-endpoint-configuration` extension `vpcEndpointIds` property](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions-endpoint-configuration.html). If the argument value is provided and is different than the OpenAPI value, **the argument value will override the OpenAPI value**.
        """
        pulumi.set(__self__, "types", types)
        if vpc_endpoint_ids is not None:
            pulumi.set(__self__, "vpc_endpoint_ids", vpc_endpoint_ids)

    @property
    @pulumi.getter
    def types(self) -> str:
        """
        A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE`, `REGIONAL` or `PRIVATE`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. If set to `PRIVATE` recommend to set `put_rest_api_mode` = `merge` to not cause the endpoints and associated Route53 records to be deleted. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        return pulumi.get(self, "types")

    @property
    @pulumi.getter(name="vpcEndpointIds")
    def vpc_endpoint_ids(self) -> Optional[Sequence[str]]:
        """
        Set of VPC Endpoint identifiers. It is only supported for `PRIVATE` endpoint type. If importing an OpenAPI specification via the `body` argument, this corresponds to the [`x-amazon-apigateway-endpoint-configuration` extension `vpcEndpointIds` property](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions-endpoint-configuration.html). If the argument value is provided and is different than the OpenAPI value, **the argument value will override the OpenAPI value**.
        """
        return pulumi.get(self, "vpc_endpoint_ids")


@pulumi.output_type
class StageAccessLogSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationArn":
            suggest = "destination_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StageAccessLogSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StageAccessLogSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StageAccessLogSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_arn: str,
                 format: str):
        """
        :param str destination_arn: The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with `amazon-apigateway-`. Automatically removes trailing `:*` if present.
        :param str format: The formatting and values recorded in the logs.
               For more information on configuring the log format rules visit the AWS [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html)
        """
        pulumi.set(__self__, "destination_arn", destination_arn)
        pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with `amazon-apigateway-`. Automatically removes trailing `:*` if present.
        """
        return pulumi.get(self, "destination_arn")

    @property
    @pulumi.getter
    def format(self) -> str:
        """
        The formatting and values recorded in the logs.
        For more information on configuring the log format rules visit the AWS [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html)
        """
        return pulumi.get(self, "format")


@pulumi.output_type
class StageCanarySettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "percentTraffic":
            suggest = "percent_traffic"
        elif key == "stageVariableOverrides":
            suggest = "stage_variable_overrides"
        elif key == "useStageCache":
            suggest = "use_stage_cache"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StageCanarySettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StageCanarySettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StageCanarySettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 percent_traffic: Optional[float] = None,
                 stage_variable_overrides: Optional[Mapping[str, Any]] = None,
                 use_stage_cache: Optional[bool] = None):
        """
        :param float percent_traffic: The percent `0.0` - `100.0` of traffic to divert to the canary deployment.
        :param Mapping[str, Any] stage_variable_overrides: A map of overridden stage `variables` (including new variables) for the canary deployment.
        :param bool use_stage_cache: Whether the canary deployment uses the stage cache. Defaults to false.
        """
        if percent_traffic is not None:
            pulumi.set(__self__, "percent_traffic", percent_traffic)
        if stage_variable_overrides is not None:
            pulumi.set(__self__, "stage_variable_overrides", stage_variable_overrides)
        if use_stage_cache is not None:
            pulumi.set(__self__, "use_stage_cache", use_stage_cache)

    @property
    @pulumi.getter(name="percentTraffic")
    def percent_traffic(self) -> Optional[float]:
        """
        The percent `0.0` - `100.0` of traffic to divert to the canary deployment.
        """
        return pulumi.get(self, "percent_traffic")

    @property
    @pulumi.getter(name="stageVariableOverrides")
    def stage_variable_overrides(self) -> Optional[Mapping[str, Any]]:
        """
        A map of overridden stage `variables` (including new variables) for the canary deployment.
        """
        return pulumi.get(self, "stage_variable_overrides")

    @property
    @pulumi.getter(name="useStageCache")
    def use_stage_cache(self) -> Optional[bool]:
        """
        Whether the canary deployment uses the stage cache. Defaults to false.
        """
        return pulumi.get(self, "use_stage_cache")


@pulumi.output_type
class UsagePlanApiStage(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "apiId":
            suggest = "api_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UsagePlanApiStage. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UsagePlanApiStage.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UsagePlanApiStage.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 api_id: str,
                 stage: str,
                 throttles: Optional[Sequence['outputs.UsagePlanApiStageThrottle']] = None):
        """
        :param str api_id: API Id of the associated API stage in a usage plan.
        :param str stage: API stage name of the associated API stage in a usage plan.
        :param Sequence['UsagePlanApiStageThrottleArgs'] throttles: The throttling limits of the usage plan.
        """
        pulumi.set(__self__, "api_id", api_id)
        pulumi.set(__self__, "stage", stage)
        if throttles is not None:
            pulumi.set(__self__, "throttles", throttles)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> str:
        """
        API Id of the associated API stage in a usage plan.
        """
        return pulumi.get(self, "api_id")

    @property
    @pulumi.getter
    def stage(self) -> str:
        """
        API stage name of the associated API stage in a usage plan.
        """
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def throttles(self) -> Optional[Sequence['outputs.UsagePlanApiStageThrottle']]:
        """
        The throttling limits of the usage plan.
        """
        return pulumi.get(self, "throttles")


@pulumi.output_type
class UsagePlanApiStageThrottle(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "burstLimit":
            suggest = "burst_limit"
        elif key == "rateLimit":
            suggest = "rate_limit"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UsagePlanApiStageThrottle. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UsagePlanApiStageThrottle.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UsagePlanApiStageThrottle.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 path: str,
                 burst_limit: Optional[int] = None,
                 rate_limit: Optional[float] = None):
        """
        :param str path: The method to apply the throttle settings for. Specfiy the path and method, for example `/test/GET`.
        :param int burst_limit: The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        :param float rate_limit: The API request steady-state rate limit.
        """
        pulumi.set(__self__, "path", path)
        if burst_limit is not None:
            pulumi.set(__self__, "burst_limit", burst_limit)
        if rate_limit is not None:
            pulumi.set(__self__, "rate_limit", rate_limit)

    @property
    @pulumi.getter
    def path(self) -> str:
        """
        The method to apply the throttle settings for. Specfiy the path and method, for example `/test/GET`.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="burstLimit")
    def burst_limit(self) -> Optional[int]:
        """
        The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        """
        return pulumi.get(self, "burst_limit")

    @property
    @pulumi.getter(name="rateLimit")
    def rate_limit(self) -> Optional[float]:
        """
        The API request steady-state rate limit.
        """
        return pulumi.get(self, "rate_limit")


@pulumi.output_type
class UsagePlanQuotaSettings(dict):
    def __init__(__self__, *,
                 limit: int,
                 period: str,
                 offset: Optional[int] = None):
        """
        :param int limit: The maximum number of requests that can be made in a given time period.
        :param str period: The time period in which the limit applies. Valid values are "DAY", "WEEK" or "MONTH".
        :param int offset: The number of requests subtracted from the given limit in the initial time period.
        """
        pulumi.set(__self__, "limit", limit)
        pulumi.set(__self__, "period", period)
        if offset is not None:
            pulumi.set(__self__, "offset", offset)

    @property
    @pulumi.getter
    def limit(self) -> int:
        """
        The maximum number of requests that can be made in a given time period.
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def period(self) -> str:
        """
        The time period in which the limit applies. Valid values are "DAY", "WEEK" or "MONTH".
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter
    def offset(self) -> Optional[int]:
        """
        The number of requests subtracted from the given limit in the initial time period.
        """
        return pulumi.get(self, "offset")


@pulumi.output_type
class UsagePlanThrottleSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "burstLimit":
            suggest = "burst_limit"
        elif key == "rateLimit":
            suggest = "rate_limit"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UsagePlanThrottleSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UsagePlanThrottleSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UsagePlanThrottleSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 burst_limit: Optional[int] = None,
                 rate_limit: Optional[float] = None):
        """
        :param int burst_limit: The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        :param float rate_limit: The API request steady-state rate limit.
        """
        if burst_limit is not None:
            pulumi.set(__self__, "burst_limit", burst_limit)
        if rate_limit is not None:
            pulumi.set(__self__, "rate_limit", rate_limit)

    @property
    @pulumi.getter(name="burstLimit")
    def burst_limit(self) -> Optional[int]:
        """
        The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        """
        return pulumi.get(self, "burst_limit")

    @property
    @pulumi.getter(name="rateLimit")
    def rate_limit(self) -> Optional[float]:
        """
        The API request steady-state rate limit.
        """
        return pulumi.get(self, "rate_limit")


@pulumi.output_type
class GetDomainNameEndpointConfigurationResult(dict):
    def __init__(__self__, *,
                 types: Sequence[str]):
        """
        :param Sequence[str] types: List of endpoint types.
        """
        pulumi.set(__self__, "types", types)

    @property
    @pulumi.getter
    def types(self) -> Sequence[str]:
        """
        List of endpoint types.
        """
        return pulumi.get(self, "types")


@pulumi.output_type
class GetRestApiEndpointConfigurationResult(dict):
    def __init__(__self__, *,
                 types: Sequence[str],
                 vpc_endpoint_ids: Sequence[str]):
        pulumi.set(__self__, "types", types)
        pulumi.set(__self__, "vpc_endpoint_ids", vpc_endpoint_ids)

    @property
    @pulumi.getter
    def types(self) -> Sequence[str]:
        return pulumi.get(self, "types")

    @property
    @pulumi.getter(name="vpcEndpointIds")
    def vpc_endpoint_ids(self) -> Sequence[str]:
        return pulumi.get(self, "vpc_endpoint_ids")


