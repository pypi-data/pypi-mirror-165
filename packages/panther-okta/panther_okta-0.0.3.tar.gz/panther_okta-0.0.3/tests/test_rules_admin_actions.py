import json
import unittest

from panther_config import detection, PantherEvent
import panther_okta as okta


class TestRulesAdminActions(unittest.TestCase):
    def test_admin_disabled_mfa(self):
        name_override = "Override Name"
        rule = okta.rules.admin_disabled_mfa(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)

    def test_admin_role_assigned(self):
        name_override = "Override Name"
        rule = okta.rules.admin_role_assigned(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)

        evt = PantherEvent(json.loads(okta.sample_logs.admin_access_assigned))

        title = rule.alert_title(evt)

        self.assertEqual(
            title,
            "Jack Naglieri <jack@acme.io> granted [Organization administrator, Application administrator (all)] privileges to Alice Green <alice@acme.io>",
        )
