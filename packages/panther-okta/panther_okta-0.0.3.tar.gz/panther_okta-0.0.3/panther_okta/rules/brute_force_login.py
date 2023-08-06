import typing

from panther_core import PantherEvent
from panther_utils import match_filters
from panther_config import detection

from panther_okta import sample_logs
from panther_okta._shared import (
    rule_tags,
    SYSTEM_LOG_TYPE,
    SHARED_SUMMARY_ATTRS,
    create_alert_context,
    pick_filters,
)

__all__ = ["brute_force_logins"]


def brute_force_logins(
    pre_filters: typing.List[detection.AnyFilter] = None,
    overrides: detection.RuleOptions = detection.RuleOptions(),
) -> detection.Rule:
    """A user has failed to login more than 5 times in 15 minutes"""

    def _title(event: PantherEvent) -> str:
        return (
            f"Suspected brute force Okta logins to account "
            f"{event.get('actor', {}).get('alternateId', '<UNKNOWN_ACCOUNT>')}, due to "
            f"[{event.get('outcome', {}).get('reason', '<UNKNOWN_REASON>')}]"
        )

    return detection.Rule(
        name=(overrides.name or "--DEPRECATED-- Okta Brute Force Logins"),
        rule_id=(overrides.rule_id or "Okta.BruteForceLogins"),
        log_types=(overrides.log_types or [SYSTEM_LOG_TYPE]),
        tags=(overrides.tags or rule_tags()),
        severity=(overrides.severity or detection.SeverityMedium),
        description=(
            overrides.description
            or "A user has failed to login more than 5 times in 15 minutes"
        ),
        reference=(
            overrides.reference
            or "https://developer.okta.com/docs/reference/api/system-log/#user-events"
        ),
        runbook=(
            overrides.runbook
            or "Reach out to the user if needed to validate the activity, and then block the IP"
        ),
        filters=pick_filters(
            overrides=overrides,
            pre_filters=pre_filters,
            defaults=[
                match_filters.deep_equal("eventType", "user.session.start"),
                match_filters.deep_equal("outcome.result", "FAILURE"),
            ],
        ),
        alert_title=(overrides.alert_title or _title),
        alert_context=(overrides.alert_context or create_alert_context),
        summary_attrs=(overrides.summary_attrs or SHARED_SUMMARY_ATTRS),
        unit_tests=(
            overrides.unit_tests
            or [
                detection.JSONUnitTest(
                    name="Failed Login Alert",
                    expect_match=True,
                    data=sample_logs.failed_login,
                ),
            ]
        ),
    )
