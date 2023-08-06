from typing import Dict, List, Any, Optional
from panther_config import PantherEvent, detection
from panther_utils import standard_tags

__all__ = [
    "rule_tags",
    "SYSTEM_LOG_TYPE",
    "SUPPORT_ACCESS_EVENTS",
    "SUPPORT_RESET_EVENTS",
    "SHARED_TAGS",
    "SHARED_SUMMARY_ATTRS",
    "create_alert_context",
]

SYSTEM_LOG_TYPE = "Okta.SystemLog"


SUPPORT_ACCESS_EVENTS = [
    "user.session.impersonation.grant",
    "user.session.impersonation.initiate",
]

SUPPORT_RESET_EVENTS = [
    "user.account.reset_password",
    "user.mfa.factor.update",
    "system.mfa.factor.deactivate",
    "user.mfa.attempt_bypass",
]


SHARED_TAGS = [
    "Okta",
    standard_tags.IDENTITY_AND_ACCESS_MGMT,
]


SHARED_SUMMARY_ATTRS = [
    "eventType",
    "severity",
    "displayMessage",
    "p_any_ip_addresses",
]


def rule_tags(*extra_tags: str) -> List[str]:
    return [*SHARED_TAGS, *extra_tags]


def create_alert_context(event: PantherEvent) -> Dict[str, Any]:
    """Returns common context for Okta alerts"""

    return {
        "ips": event.get("p_any_ip_addresses", []),
        "actor": event.get("actor", ""),
        "target": event.get("target", ""),
        "client": event.get("client", ""),
    }


def pick_filters(
    pre_filters: Optional[List[detection.AnyFilter]],
    overrides: detection.RuleOptions,
    defaults: List[detection.AnyFilter],
) -> List[detection.AnyFilter]:
    if pre_filters is None:
        pre_filters = []

    if overrides.filters is None:
        return pre_filters + defaults
    else:
        if isinstance(overrides.filters, detection.AnyFilter):
            return pre_filters + [overrides.filters]

        if isinstance(overrides.filters, list):
            return pre_filters + overrides.filters

    raise RuntimeError("unable to pick filters")
