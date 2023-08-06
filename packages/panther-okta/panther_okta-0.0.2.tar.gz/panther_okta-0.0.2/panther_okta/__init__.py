from typing import Literal

from . import rules, sample_logs, queries
from ._shared import *


def use_all_with_defaults(
    datalake: Literal["athena", "snowflake"] = "snowflake"
) -> None:
    rules.admin_disabled_mfa()
    rules.admin_role_assigned()
    rules.api_key_created()
    rules.brute_force_logins()
    rules.account_support_access()
    rules.support_reset()
    rules.geo_improbable_access()

    queries.activity_audit(datalake=datalake)
    queries.session_id_audit(datalake=datalake)
    queries.admin_access_granted(datalake=datalake)
    queries.mfa_password_reset_audit(datalake=datalake)
    queries.support_access(datalake=datalake)
