import unittest

from proofmesh.config import load_config
from proofmesh.live_adapter import LiveCROOAdapter


class LiveAdapterTest(unittest.TestCase):
    def test_config_loads_defaults_and_redacts_key(self):
        config = load_config({"CROO_API_KEY": "secret-key"})

        self.assertEqual(config.croo_api_url, "https://api.croo.network")
        self.assertEqual(config.croo_ws_url, "wss://api.croo.network/ws")
        self.assertEqual(config.to_dict()["croo_sdk_key"], "***redacted***")

    def test_config_accepts_legacy_sdk_key_alias(self):
        config = load_config({"CROO_SDK_KEY": "legacy-secret-key"})

        self.assertEqual(config.croo_sdk_key, "legacy-secret-key")

    def test_readiness_reports_missing_credentials(self):
        config = load_config({})
        report = LiveCROOAdapter(config).check_readiness()
        checks = {check.name: check for check in report.checks}

        self.assertFalse(report.ready)
        self.assertFalse(checks["croo_sdk_key"].ok)
        self.assertIn("CROO_API_KEY", checks["croo_sdk_key"].detail)
        self.assertIn("CROO_SDK_KEY", checks["croo_sdk_key"].detail)
        self.assertTrue(checks["croo_api_url"].ok)
        self.assertTrue(checks["croo_ws_url"].ok)

    def test_service_listing_contains_schema_and_price(self):
        config = load_config({"PROOFMESH_PRICE_CROO": "0.5"})
        listing = LiveCROOAdapter(config).build_service_listing()

        self.assertEqual(listing["service_id"], "proofmesh-source-coverage-audit")
        self.assertEqual(listing["price"]["amount"], 0.5)
        self.assertEqual(listing["input_schema"]["schema_version"], "proofmesh.verification.v1")

    def test_live_dry_run_attaches_receipt_and_readiness(self):
        config = load_config({})
        audit = LiveCROOAdapter(config).audit_dry_run(
            {
                "task_id": "dry-run-unit",
                "artifact_type": "claim_set",
                "claims": [
                    {
                        "id": "c1",
                        "text": "CAP lets agents discover hire and pay other agents on-chain",
                        "source_ids": ["s1"],
                    }
                ],
                "sources": [
                    {
                        "id": "s1",
                        "text": "CAP lets any agent discover hire and pay any other agent on-chain.",
                    }
                ],
            }
        )

        self.assertTrue(audit["is_verified"])
        self.assertEqual(audit["cap_receipt"]["mode"], "live_ready_dry_run")
        self.assertFalse(audit["live_readiness"]["ready"])


if __name__ == "__main__":
    unittest.main()
