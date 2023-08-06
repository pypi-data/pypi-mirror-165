import typing
import unittest
from panther_config import PantherEvent
import panther_okta as okta


class TestModule(unittest.TestCase):
    def test_root_module_api(self) -> None:
        self.assertIsInstance(okta.use_all_with_defaults, typing.Callable)

    def test_create_alert_context(self) -> None:
        self.assertIsInstance(okta.create_alert_context, typing.Callable)

        mock_data = {
            "p_any_ip_addresses": ["0.0.0.0"],
            "actor": "actor-value",
            "target": "target-value",
            "client": "client-value",
        }

        evt = PantherEvent(mock_data, data_model=None)
        ctx = okta.create_alert_context(evt)

        self.assertEqual(
            ctx,
            {
                "ips": mock_data["p_any_ip_addresses"],
                "actor": mock_data["actor"],
                "target": mock_data["target"],
                "client": mock_data["client"],
            },
        )
