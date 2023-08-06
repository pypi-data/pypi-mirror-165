import typing

from panther_core import PantherEvent
from panther_utils import match_filters
from panther_config import detection

from .. import sample_logs
from .._shared import (
    rule_tags,
    pick_filters,
    SYSTEM_LOG_TYPE,
    SHARED_SUMMARY_ATTRS,
    create_alert_context,
)

__all__ = [
    "api_key_created",
    "api_key_revoked",
]


def api_key_created(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """A user created an API Key in Okta"""

    def _title(event: PantherEvent) -> str:
        target = event.get("target", [{}])
        key_name = (
            target[0].get("displayName", "MISSING DISPLAY NAME")
            if target
            else "MISSING TARGET"
        )

        return (
            f"{event.deep_get('actor', 'displayName')} <{event.deep_get('actor', 'alternateId')}>"
            f"created a new API key - <{key_name}>"
        )

    return detection.Rule(
        name=(overrides.name or "Okta API Key Created"),
        rule_id=(overrides.rule_id or "Okta.APIKeyCreated"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(
            overrides.tags
            or rule_tags(
                "Credential Access:Steal Application Access Token",
            )
        ),
        reports=(overrides.reports or {detection.ReportKeyMITRE: ["TA0006:T1528"]}),
        severity=(overrides.severity or detection.SeverityInfo),
        description=(overrides.description or "A user created an API Key in Okta"),
        reference=(
            overrides.reference
            or "https://help.okta.com/en/prod/Content/Topics/Security/API.htm"
        ),
        runbook=(
            overrides.runbook
            or "Reach out to the user if needed to validate the activity."
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_equal("eventType", "system.api_token.create"),
                match_filters.deep_equal("outcome.result", "SUCCESS"),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="API Key Created",
                    expect_match=True,
                    data=sample_logs.system_api_token_create,
                ),
            ]
        ),
    )


def api_key_revoked(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """A user has revoked an API Key in Okta"""

    def _title(event: PantherEvent) -> str:
        target = event.get("target", [{}])
        key_name = (
            target[0].get("displayName", "MISSING DISPLAY NAME")
            if target
            else "MISSING TARGET"
        )

        return (
            f"{event.get('actor', {}).get('displayName')} <{event.get('actor', {}).get('alternateId')}>"
            f"revoked API key - <{key_name}>"
        )

    return detection.Rule(
        name=(overrides.name or "Okta API Key Revoked"),
        rule_id=(overrides.rule_id or "Okta.APIKeyRevoked"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(overrides.tags or rule_tags()),
        severity=(overrides.severity or detection.SeverityInfo),
        description=(overrides.description or "A user has revoked an API Key in Okta"),
        reference=(
            overrides.reference
            or "https://help.okta.com/en/prod/Content/Topics/Security/API.htm"
        ),
        runbook=(overrides.runbook or "Validate this action was authorized."),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_equal("eventType", "system.api_token.revoke"),
                match_filters.deep_equal("outcome.result", "SUCCESS"),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="API Key Revoked",
                    expect_match=True,
                    data=sample_logs.system_api_token_revoke,
                ),
            ]
        ),
    )
