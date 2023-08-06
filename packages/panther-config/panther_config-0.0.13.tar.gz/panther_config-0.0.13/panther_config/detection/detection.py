# Copyright (C) 2022 Panther Labs Inc
#
# Panther Enterprise is licensed under the terms of a commercial license available from
# Panther Labs Inc ("Panther Commercial License") by contacting contact@runpanther.com.
# All use, distribution, and/or modification of this software, whether commercial or non-commercial,
# falls under the Panther Commercial License to the extent it is permitted.

# coding=utf-8
# *** WARNING: generated file
import typing
import dataclasses

from panther_core import PantherEvent

"""
The detection module provides classes representing Panther detections: Rules, Policies, Scheduled Rules and more
"""

from .. import _utilities

__all__ = [
    "AnyFilter",
    "DynamicStringField",
    "DynamicStringFieldOptions",
    "DynamicDestinations",
    "DynamicDestinationsOptions",
    "AlertGrouping",
    "AlertGroupingOptions",
    "PythonFilter",
    "PythonFilterOptions",
    "_BaseUnitTest",
    "_BaseUnitTestOptions",
    "JSONUnitTest",
    "JSONUnitTestOptions",
    "Rule",
    "RuleOptions",
    "SeverityLow",
    "SeverityInfo",
    "SeverityMedium",
    "SeverityHigh",
    "SeverityCritical",
    "ReportKeyMITRE",
]


SeverityLow = "LOW"
SeverityInfo = "INFO"
SeverityMedium = "MEDIUM"
SeverityHigh = "HIGH"
SeverityCritical = "CRITICAL"
ReportKeyMITRE = "MITRE ATT&CK"


@dataclasses.dataclass
class DynamicStringFieldOptions:
    """Options dataclass for DynamicStringField. All arguments are marked optional.

    - func -- Dynamic handler
    - fallback -- Fallback value in case the dynamic handler fails
    """

    func: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    fallback: typing.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class DynamicStringField(_utilities.ConfigNode):
    """Make a field dynamic based on the detection input

    - func -- Dynamic handler (required)
    - fallback -- Fallback value in case the dynamic handler fails (optional, default: "")
    """

    # required
    func: typing.Callable[[PantherEvent], str]

    # optional
    fallback: str = ""

    # internal private methods
    def _typename(self) -> str:
        return "DynamicStringField"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["func", "fallback"]


@dataclasses.dataclass
class DynamicDestinationsOptions:
    """Options dataclass for DynamicDestinations. All arguments are marked optional.

    - func -- Dynamic handler
    - fallback -- Fallback value in case the dynamic handler fails
    """

    func: typing.Optional[typing.Callable[[PantherEvent], typing.List[str]]] = None

    fallback: typing.Optional[typing.List[str]] = None


@dataclasses.dataclass(frozen=True)
class DynamicDestinations(_utilities.ConfigNode):
    """Make destinations dynamic based on the detection input

    - func -- Dynamic handler (required)
    - fallback -- Fallback value in case the dynamic handler fails (optional, default: None)
    """

    # required
    func: typing.Callable[[PantherEvent], typing.List[str]]

    # optional
    fallback: typing.Optional[typing.List[str]] = None

    # internal private methods
    def _typename(self) -> str:
        return "DynamicDestinations"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["func", "fallback"]


@dataclasses.dataclass
class AlertGroupingOptions:
    """Options dataclass for AlertGrouping. All arguments are marked optional.

    - group_by -- Function to generate a key for grouping matches
    - period_minutes -- How long should matches be grouped into an alert after the first match
    """

    group_by: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    period_minutes: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class AlertGrouping(_utilities.ConfigNode):
    """Configuration for how an alert is grouped

    - group_by -- Function to generate a key for grouping matches (optional, default: None)
    - period_minutes -- How long should matches be grouped into an alert after the first match (optional, default: 15)
    """

    # optional
    group_by: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    period_minutes: int = 15

    # internal private methods
    def _typename(self) -> str:
        return "AlertGrouping"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["group_by", "period_minutes"]


@dataclasses.dataclass
class PythonFilterOptions:
    """Options dataclass for PythonFilter. All arguments are marked optional.

    - func -- Provide a function whose python source will be used as the filter definition
    """

    func: typing.Optional[typing.Callable[[PantherEvent], bool]] = None


@dataclasses.dataclass(frozen=True)
class PythonFilter(_utilities.ConfigNode):
    """Create a filter by referencing a python function

    - func -- Provide a function whose python source will be used as the filter definition (required)
    """

    # required
    func: typing.Callable[[PantherEvent], bool]

    # internal private methods
    def _typename(self) -> str:
        return "PythonFilter"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["func"]


@dataclasses.dataclass
class _BaseUnitTestOptions:
    """Options dataclass for _BaseUnitTest. All arguments are marked optional."""


@dataclasses.dataclass(frozen=True)
class _BaseUnitTest(_utilities.ConfigNode):
    """Base unit test"""

    # internal private methods
    def _typename(self) -> str:
        return "_BaseUnitTest"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return []


@dataclasses.dataclass
class JSONUnitTestOptions:
    """Options dataclass for JSONUnitTest. All arguments are marked optional.

    - data -- json data
    - expect_match -- should this event trigger the rule?
    - name -- name of the unit test
    """

    data: typing.Optional[str] = None

    expect_match: typing.Optional[bool] = None

    name: typing.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class JSONUnitTest(_BaseUnitTest):
    """Unit test with json content

    - data -- json data (required)
    - expect_match -- should this event trigger the rule? (required)
    - name -- name of the unit test (required)
    """

    # required
    data: str

    # required
    expect_match: bool

    # required
    name: str

    # internal private methods
    def _typename(self) -> str:
        return "JSONUnitTest"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["data", "expect_match", "name"]


@dataclasses.dataclass
class RuleOptions:
    """Options dataclass for Rule. All arguments are marked optional.

    - filters -- Define event filters for the rule
    - log_types -- Log Types to associate with this rule
    - rule_id -- ID for the rule
    - severity -- Severity for the rule
    - alert_context -- Optional JSON to attach to alerts generated by this rule
    - alert_grouping -- Configuration for how an alert is grouped
    - alert_title -- Title to use in the alert
    - description -- Description for the rule
    - destinations -- Alert destinations for the rule
    - enabled -- Short description for the query
    - name -- Display name for the rule
    - reference -- Reference for the rule
    - reports -- Report mappings for the rule
    - runbook -- Runbook for the rule
    - summary_attrs -- Summary Attributes for the rule
    - tags -- Tags for the rule
    - threshold -- Number of matches received before an alert is triggered
    - unit_tests -- Define event filters for the rule
    """

    filters: typing.Optional[
        typing.Union[
            typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
        ]
    ] = None

    log_types: typing.Optional[typing.Union[str, typing.List[str]]] = None

    rule_id: typing.Optional[str] = None

    severity: typing.Optional[typing.Union[str, DynamicStringField]] = None

    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    alert_grouping: typing.Optional[AlertGrouping] = None

    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    description: typing.Optional[typing.Union[str, DynamicStringField]] = None

    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    enabled: typing.Optional[bool] = None

    name: typing.Optional[str] = None

    reference: typing.Optional[typing.Union[str, DynamicStringField]] = None

    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = None

    summary_attrs: typing.Optional[typing.List[str]] = None

    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    threshold: typing.Optional[int] = None

    unit_tests: typing.Optional[
        typing.Union[_BaseUnitTest, typing.List[_BaseUnitTest]]
    ] = None


@dataclasses.dataclass(frozen=True)
class Rule(_utilities.ConfigNode):
    """Define a Rule-type detection to execute against log data in your Panther instance

    - filters -- Define event filters for the rule (required)
    - log_types -- Log Types to associate with this rule (required)
    - rule_id -- ID for the rule (required)
    - severity -- Severity for the rule (required)
    - alert_context -- Optional JSON to attach to alerts generated by this rule (optional, default: None)
    - alert_grouping -- Configuration for how an alert is grouped (optional, default: None)
    - alert_title -- Title to use in the alert (optional, default: None)
    - description -- Description for the rule (optional, default: "")
    - destinations -- Alert destinations for the rule (optional, default: None)
    - enabled -- Short description for the query (optional, default: True)
    - name -- Display name for the rule (optional, default: "")
    - reference -- Reference for the rule (optional, default: "")
    - reports -- Report mappings for the rule (optional, default: None)
    - runbook -- Runbook for the rule (optional, default: "")
    - summary_attrs -- Summary Attributes for the rule (optional, default: None)
    - tags -- Tags for the rule (optional, default: None)
    - threshold -- Number of matches received before an alert is triggered (optional, default: 1)
    - unit_tests -- Define event filters for the rule (optional, default: None)
    """

    # required
    filters: typing.Union[
        typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
    ]

    # required
    log_types: typing.Union[str, typing.List[str]]

    # required
    rule_id: str

    # required
    severity: typing.Union[str, DynamicStringField]

    # optional
    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    # optional
    alert_grouping: typing.Optional[AlertGrouping] = None

    # optional
    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    description: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    # optional
    enabled: bool = True

    # optional
    name: typing.Optional[str] = ""

    # optional
    reference: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    # optional
    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    summary_attrs: typing.Optional[typing.List[str]] = None

    # optional
    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # optional
    threshold: int = 1

    # optional
    unit_tests: typing.Optional[
        typing.Union[_BaseUnitTest, typing.List[_BaseUnitTest]]
    ] = None

    # internal private methods
    def _typename(self) -> str:
        return "Rule"

    def _output_key(self) -> str:
        return "config-node:rule"

    def _fields(self) -> typing.List[str]:
        return [
            "filters",
            "log_types",
            "rule_id",
            "severity",
            "alert_context",
            "alert_grouping",
            "alert_title",
            "description",
            "destinations",
            "enabled",
            "name",
            "reference",
            "reports",
            "runbook",
            "summary_attrs",
            "tags",
            "threshold",
            "unit_tests",
        ]


AnyFilter = typing.Union[PythonFilter]
