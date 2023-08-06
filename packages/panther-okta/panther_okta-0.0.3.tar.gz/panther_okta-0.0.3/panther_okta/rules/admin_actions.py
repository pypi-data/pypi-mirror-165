import typing

from panther_utils import match_filters
from panther_config import detection, PantherEvent

from .. import sample_logs
from .._shared import (
    rule_tags,
    standard_tags,
    SYSTEM_LOG_TYPE,
    create_alert_context,
    SHARED_SUMMARY_ATTRS,
    SUPPORT_ACCESS_EVENTS,
    pick_filters,
)

__all__ = [
    "admin_disabled_mfa",
    "admin_role_assigned",
]


def admin_disabled_mfa(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """An admin user has disabled the MFA requirement for your Okta account"""

    def _title(event: PantherEvent) -> str:
        return f"Okta System-wide MFA Disabled by Admin User {event.udm('actor_user')}"

    return detection.Rule(
        name=(overrides.name or "Okta MFA Globally Disabled"),
        rule_id=(overrides.rule_id or "Okta.Global.MFA.Disabled"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(
            overrides.tags
            or rule_tags(
                standard_tags.DATA_MODEL,
                "Defense Evasion:Modify Authentication Process",
            )
        ),
        reports=(overrides.reports or {detection.ReportKeyMITRE: ["TA0005:T1556"]}),
        severity=(overrides.severity or detection.SeverityHigh),
        description=(
            overrides.description
            or "An admin user has disabled the MFA requirement for your Okta account"
        ),
        reference=(
            overrides.reference
            or "https://developer.okta.com/docs/reference/api/event-types/?q=system.mfa.factor.deactivate"
        ),
        runbook=(
            overrides.runbook or "Contact Admin to ensure this was sanctioned activity"
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_equal("eventType", "system.mfa.factor.deactivate"),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="MFA Disabled",
                    expect_match=True,
                    data=sample_logs.system_mfa_factor_deactivate,
                ),
                detection.JSONUnitTest(
                    name="Login Event",
                    expect_match=False,
                    data=sample_logs.user_session_start,
                ),
            ]
        ),
    )


def admin_role_assigned(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """A user has been granted administrative privileges in Okta"""

    def _title(event: PantherEvent) -> str:
        target = event.get("target", [{}])
        display_name = (
            target[0].get("displayName", "MISSING DISPLAY NAME") if target else ""
        )
        alternate_id = (
            target[0].get("alternateId", "MISSING ALTERNATE ID") if target else ""
        )
        privilege = event.deep_get(
            "debugContext",
            "debugData",
            "privilegeGranted",
            default="<UNKNOWN_PRIVILEGE>",
        )

        return (
            f"{event.deep_get('actor', 'displayName')} "
            f"<{event.deep_get('actor', 'alternateId')}> granted "
            f"[{privilege}] privileges to {display_name} <{alternate_id}>"
        )

    def _severity(event: PantherEvent) -> str:
        if (
            event.deep_get("debugContext", "debugData", "privilegeGranted")
            == "Super administrator"
        ):
            return "HIGH"
        return "INFO"

    return detection.Rule(
        name=(overrides.name or "Okta Admin Role Assigned"),
        rule_id=(overrides.rule_id or "Okta.AdminRoleAssigned"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(
            overrides.tags
            or rule_tags(
                standard_tags.DATA_MODEL,
                "Privilege Escalation:Valid Accounts",
            )
        ),
        reports=(overrides.reports or {detection.ReportKeyMITRE: ["TA0004:T1078"]}),
        severity=(
            overrides.severity
            or detection.DynamicStringField(
                func=_severity,
                fallback=detection.SeverityInfo,
            )
        ),
        description=(
            overrides.description
            or "A user has been granted administrative privileges in Okta"
        ),
        reference=(
            overrides.reference
            or "https://help.okta.com/en/prod/Content/Topics/Security/administrators-admin-comparison.htm"
        ),
        runbook=(
            overrides.runbook
            or "Reach out to the user if needed to validate the activity"
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_equal("eventType", "user.account.privilege.grant"),
                match_filters.deep_equal("outcome.result", "SUCCESS"),
                match_filters.deep_equal_pattern(
                    "debugContext.debugData.privilegeGranted", r"[aA]dministrator"
                ),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="Admin Access Assigned",
                    expect_match=True,
                    data=sample_logs.admin_access_assigned,
                ),
            ]
        ),
    )
