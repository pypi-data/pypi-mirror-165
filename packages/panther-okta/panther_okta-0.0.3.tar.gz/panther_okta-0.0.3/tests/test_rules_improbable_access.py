import unittest
import panther_okta as okta

from panther_config import testing, detection, PantherEvent
from panther_okta.rules.improbable_access import geo_improbable_access_filter


class TestGIAFilters(testing.PantherPythonFilterTestCase):
    def test_geo_improbable_access_filter_valid(self) -> None:
        f = geo_improbable_access_filter()
        self.assertFilterIsValid(f)


class TestRulesImprobableAccess(unittest.TestCase):
    def test_improbable_access(self):
        name_override = "Override Name"
        rule = okta.rules.geo_improbable_access(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)

    def test_improbable_access_group_by(self):
        name_override = "Override Name"
        rule = okta.rules.geo_improbable_access(
            overrides=detection.RuleOptions(name=name_override)
        )

        test_evt = PantherEvent({"actor": {"alternateId": "alt-id"}}, data_model=None)
        key = rule.alert_grouping.group_by(test_evt)

        self.assertEqual(key, "alt-id")
