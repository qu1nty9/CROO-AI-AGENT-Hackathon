import unittest

from proofmesh.config import load_config
from proofmesh.croo_provider import build_live_cap_receipt, parse_requirements


class CROOProviderTest(unittest.TestCase):
    def test_parse_requirements_accepts_json_payload(self):
        requirements = parse_requirements(
            '{"task_id":"t1","artifact_type":"claim_set","claims":["ProofMesh audits claims."],"sources":[]}'
        )

        self.assertEqual(requirements["task_id"], "t1")
        self.assertEqual(requirements["artifact_type"], "claim_set")
        self.assertEqual(requirements["claims"], ["ProofMesh audits claims."])

    def test_parse_requirements_wraps_plain_text(self):
        requirements = parse_requirements("Audit this generated report.")

        self.assertEqual(requirements["task_id"], "croo-text-requirements")
        self.assertEqual(requirements["artifact_type"], "text")
        self.assertEqual(requirements["artifact_text"], "Audit this generated report.")

    def test_build_live_cap_receipt_uses_staging_mode(self):
        config = load_config(
            {
                "PROOFMESH_MODE": "staging",
                "PROOFMESH_PROVIDER_AGENT_ID": "agent-1",
                "CROO_API_KEY": "test-key",
            }
        )
        order = {
            "status": "paid",
            "service_id": "proofmesh-source-coverage-audit",
            "provider_agent_id": "agent-1",
            "requester_agent_id": "agent-2",
            "negotiation_id": "neg-1",
            "order_id": "order-1",
            "pay_tx_hash": "0xpay",
        }

        receipt = build_live_cap_receipt(config=config, order=order)

        self.assertEqual(receipt["mode"], "croo_staging")
        self.assertEqual(receipt["settlement_status"], "paid")
        self.assertEqual(receipt["order_id"], "order-1")
        self.assertEqual(receipt["pay_tx_hash"], "0xpay")


if __name__ == "__main__":
    unittest.main()
