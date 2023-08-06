from . import rules, sample_logs
from ._shared import *


def use_all_with_defaults() -> None:
    rules.admin_disabled_mfa()
    rules.admin_role_assigned()
    rules.api_key_created()
    rules.brute_force_logins()
    rules.account_support_access()
    rules.support_reset()
    # rules.geo_improbable_access()
