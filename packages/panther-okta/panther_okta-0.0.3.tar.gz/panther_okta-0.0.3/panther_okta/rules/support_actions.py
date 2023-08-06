import typing

from panther_core import PantherEvent
from panther_utils import match_filters
from panther_config import detection

from .. import sample_logs
from .._shared import (
    rule_tags,
    pick_filters,
    standard_tags,
    SYSTEM_LOG_TYPE,
    create_alert_context,
    SHARED_SUMMARY_ATTRS,
    SUPPORT_RESET_EVENTS,
    SUPPORT_ACCESS_EVENTS,
)

__all__ = [
    "account_support_access",
    "support_reset",
]


def account_support_access(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """Detects when an admin user has granted access to Okta Support for your account"""

    def _title(event: PantherEvent) -> str:
        return f"Okta Support Access Granted by {event.udm('actor_user')}"

    return detection.Rule(
        name=(overrides.name or "Okta Support Access Granted"),
        rule_id=(overrides.rule_id or "Okta.Support.Access"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(
            overrides.tags
            or rule_tags(
                standard_tags.DATA_MODEL, "Initial Access:Trusted Relationship"
            )
        ),
        reports=(overrides.reports or {detection.ReportKeyMITRE: ["TA0001:T1199"]}),
        severity=(overrides.severity or detection.SeverityMedium),
        description=(
            overrides.description
            or "An admin user has granted access to Okta Support to your account"
        ),
        reference=(
            overrides.reference
            or "https://help.okta.com/en/prod/Content/Topics/Settings/settings-support-access.htm"
        ),
        runbook=(
            overrides.runbook or "Contact Admin to ensure this was sanctioned activity"
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_in("eventType", SUPPORT_ACCESS_EVENTS),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="Support Access Granted",
                    expect_match=True,
                    data=sample_logs.user_session_impersonation_grant,
                ),
                detection.JSONUnitTest(
                    name="Login Event",
                    expect_match=False,
                    data=sample_logs.user_session_start,
                ),
            ]
        ),
    )


def support_reset(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """A Password or MFA factor was reset by Okta Support"""

    def _title(event: PantherEvent) -> str:
        return f"Okta Support Reset Password or MFA for user {event.udm('actor_user')}"

    return detection.Rule(
        name=(overrides.name or "Okta Support Reset Credential"),
        rule_id=(overrides.rule_id or "Okta.Support.Reset"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(
            overrides.tags
            or rule_tags(
                standard_tags.DATA_MODEL, "Initial Access:Trusted Relationship"
            )
        ),
        reports=(overrides.reports or {detection.ReportKeyMITRE: ["TA0001:T1199"]}),
        severity=(overrides.severity or detection.SeverityHigh),
        description=(
            overrides.description
            or "A Password or MFA factor was reset by Okta Support"
        ),
        reference=(
            overrides.reference
            or "https://help.okta.com/en/prod/Content/Topics/Directory/get-support.htm#:~:text=Visit%20the%20Okta%20Help%20Center,1%2D800%2D219%2D0964"
        ),
        runbook=(
            overrides.runbook or "Contact Admin to ensure this was sanctioned activity"
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_in("eventType", SUPPORT_RESET_EVENTS),
                match_filters.deep_equal("actor.alternateId", "system@okta.com"),
                match_filters.deep_equal("transaction.id", "unknown"),
                match_filters.deep_equal("userAgent.rawUserAgent", None),
                match_filters.deep_equal("client.geographicalContext.country", None),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="Support Reset Credential",
                    expect_match=True,
                    data=sample_logs.support_password_reset,
                ),
                detection.JSONUnitTest(
                    name="Reset by Company Admin",
                    expect_match=False,
                    data=sample_logs.admin_password_reset,
                ),
            ]
        ),
    )
