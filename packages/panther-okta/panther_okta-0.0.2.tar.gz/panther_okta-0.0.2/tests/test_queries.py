import typing
import unittest

from panther_config import query
import panther_okta as okta


class TestQueries(unittest.TestCase):
    def test_queries(self) -> None:
        datalakes: typing.List[typing.Literal["snowflake", "athena"]] = [
            "snowflake",
            "athena",
        ]

        for datalake in datalakes:
            self.assertIsInstance(
                okta.queries.activity_audit(datalake=datalake), query.Query
            )
            self.assertIsInstance(
                okta.queries.session_id_audit(datalake=datalake), query.Query
            )
            self.assertIsInstance(
                okta.queries.admin_access_granted(datalake=datalake), query.Query
            )
            self.assertIsInstance(
                okta.queries.mfa_password_reset_audit(datalake=datalake), query.Query
            )
            self.assertIsInstance(
                okta.queries.support_access(datalake=datalake), query.Query
            )
