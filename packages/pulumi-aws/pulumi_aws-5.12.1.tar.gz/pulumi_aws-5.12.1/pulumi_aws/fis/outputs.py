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
    'ExperimentTemplateAction',
    'ExperimentTemplateActionParameter',
    'ExperimentTemplateActionTarget',
    'ExperimentTemplateStopCondition',
    'ExperimentTemplateTarget',
    'ExperimentTemplateTargetFilter',
    'ExperimentTemplateTargetResourceTag',
]

@pulumi.output_type
class ExperimentTemplateAction(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionId":
            suggest = "action_id"
        elif key == "startAfters":
            suggest = "start_afters"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateAction. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateAction.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateAction.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action_id: str,
                 name: str,
                 description: Optional[str] = None,
                 parameters: Optional[Sequence['outputs.ExperimentTemplateActionParameter']] = None,
                 start_afters: Optional[Sequence[str]] = None,
                 target: Optional['outputs.ExperimentTemplateActionTarget'] = None):
        """
        :param str action_id: ID of the action. To find out what actions are supported see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        :param str name: Friendly name given to the target.
        :param str description: Description of the action.
        :param Sequence['ExperimentTemplateActionParameterArgs'] parameters: Parameter(s) for the action, if applicable. See below.
        :param Sequence[str] start_afters: Set of action names that must complete before this action can be executed.
        :param 'ExperimentTemplateActionTargetArgs' target: Action's target, if applicable. See below.
        """
        pulumi.set(__self__, "action_id", action_id)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if start_afters is not None:
            pulumi.set(__self__, "start_afters", start_afters)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="actionId")
    def action_id(self) -> str:
        """
        ID of the action. To find out what actions are supported see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        """
        return pulumi.get(self, "action_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Friendly name given to the target.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the action.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Sequence['outputs.ExperimentTemplateActionParameter']]:
        """
        Parameter(s) for the action, if applicable. See below.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="startAfters")
    def start_afters(self) -> Optional[Sequence[str]]:
        """
        Set of action names that must complete before this action can be executed.
        """
        return pulumi.get(self, "start_afters")

    @property
    @pulumi.getter
    def target(self) -> Optional['outputs.ExperimentTemplateActionTarget']:
        """
        Action's target, if applicable. See below.
        """
        return pulumi.get(self, "target")


@pulumi.output_type
class ExperimentTemplateActionParameter(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        :param str key: Tag key.
        :param str value: Tag value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Tag value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ExperimentTemplateActionTarget(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        :param str key: Tag key.
        :param str value: Tag value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Tag value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ExperimentTemplateStopCondition(dict):
    def __init__(__self__, *,
                 source: str,
                 value: Optional[str] = None):
        """
        :param str source: Source of the condition. One of `none`, `aws:cloudwatch:alarm`.
        :param str value: Tag value.
        """
        pulumi.set(__self__, "source", source)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        Source of the condition. One of `none`, `aws:cloudwatch:alarm`.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Tag value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ExperimentTemplateTarget(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceType":
            suggest = "resource_type"
        elif key == "selectionMode":
            suggest = "selection_mode"
        elif key == "resourceArns":
            suggest = "resource_arns"
        elif key == "resourceTags":
            suggest = "resource_tags"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateTarget. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateTarget.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateTarget.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 resource_type: str,
                 selection_mode: str,
                 filters: Optional[Sequence['outputs.ExperimentTemplateTargetFilter']] = None,
                 resource_arns: Optional[Sequence[str]] = None,
                 resource_tags: Optional[Sequence['outputs.ExperimentTemplateTargetResourceTag']] = None):
        """
        :param str name: Friendly name given to the target.
        :param str resource_type: AWS resource type. The resource type must be supported for the specified action. To find out what resource types are supported, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#resource-types).
        :param str selection_mode: Scopes the identified resources. Valid values are `ALL` (all identified resources), `COUNT(n)` (randomly select `n` of the identified resources), `PERCENT(n)` (randomly select `n` percent of the identified resources).
        :param Sequence['ExperimentTemplateTargetFilterArgs'] filters: Filter(s) for the target. Filters can be used to select resources based on specific attributes returned by the respective describe action of the resource type. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters). See below.
        :param Sequence[str] resource_arns: Set of ARNs of the resources to target with an action. Conflicts with `resource_tag`.
        :param Sequence['ExperimentTemplateTargetResourceTagArgs'] resource_tags: Tag(s) the resources need to have to be considered a valid target for an action. Conflicts with `resource_arns`. See below.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_type", resource_type)
        pulumi.set(__self__, "selection_mode", selection_mode)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if resource_arns is not None:
            pulumi.set(__self__, "resource_arns", resource_arns)
        if resource_tags is not None:
            pulumi.set(__self__, "resource_tags", resource_tags)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Friendly name given to the target.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> str:
        """
        AWS resource type. The resource type must be supported for the specified action. To find out what resource types are supported, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#resource-types).
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="selectionMode")
    def selection_mode(self) -> str:
        """
        Scopes the identified resources. Valid values are `ALL` (all identified resources), `COUNT(n)` (randomly select `n` of the identified resources), `PERCENT(n)` (randomly select `n` percent of the identified resources).
        """
        return pulumi.get(self, "selection_mode")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.ExperimentTemplateTargetFilter']]:
        """
        Filter(s) for the target. Filters can be used to select resources based on specific attributes returned by the respective describe action of the resource type. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters). See below.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="resourceArns")
    def resource_arns(self) -> Optional[Sequence[str]]:
        """
        Set of ARNs of the resources to target with an action. Conflicts with `resource_tag`.
        """
        return pulumi.get(self, "resource_arns")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[Sequence['outputs.ExperimentTemplateTargetResourceTag']]:
        """
        Tag(s) the resources need to have to be considered a valid target for an action. Conflicts with `resource_arns`. See below.
        """
        return pulumi.get(self, "resource_tags")


@pulumi.output_type
class ExperimentTemplateTargetFilter(dict):
    def __init__(__self__, *,
                 path: str,
                 values: Sequence[str]):
        """
        :param str path: Attribute path for the filter.
        :param Sequence[str] values: Set of attribute values for the filter.
        """
        pulumi.set(__self__, "path", path)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def path(self) -> str:
        """
        Attribute path for the filter.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Set of attribute values for the filter.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class ExperimentTemplateTargetResourceTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        :param str key: Tag key.
        :param str value: Tag value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Tag value.
        """
        return pulumi.get(self, "value")


