import json
from pathlib import Path
import unittest

from proofmesh.cap_mock import MockCAPNetwork
from proofmesh.mock_lifecycle import run_mock_cap_lifecycle, summarize_lifecycle
from proofmesh.provider import PROOFMESH_SERVICE_ID, ProofMeshProvider


ROOT = Path(__file__).resolve().parents[1]


class MockCAPLifecycleTest(unittest.TestCase):
    def test_requester_provider_lifecycle_delivers_audit(self):
        requirements = _load_case("contradicted_claim.json")
        network = MockCAPNetwork()
        provider = ProofMeshProvider(network)

        negotiation = network.create_negotiation(
            service_id=PROOFMESH_SERVICE_ID,
            requester_agent_id="cap://test-requester.local",
            requirements=requirements,
        )
        order = provider.handle_negotiation_created(negotiation.negotiation_id)
        payment = network.pay_order(order.order_id)
        delivery = provider.handle_order_paid(order.order_id)
        completed_order = network.get_order(order.order_id)
        audit = delivery.deliverable_schema

        self.assertEqual(completed_order.status, "completed")
        self.assertEqual(payment.event_type, "order_paid")
        self.assertEqual(delivery.status, "submitted")
        self.assertFalse(audit["is_verified"])
        self.assertEqual(audit["cap_receipt"]["mode"], "mock_cap")
        self.assertEqual(audit["cap_receipt"]["order_id"], order.order_id)
        self.assertGreaterEqual(len(network.ledger), 2)
        self.assertEqual(
            [event["event_type"] for event in network.events],
            [
                "service_registered",
                "negotiation_created",
                "negotiation_accepted",
                "order_paid",
                "order_completed",
            ],
        )

    def test_order_must_be_paid_before_delivery(self):
        requirements = _load_case("supported_artifact.json")
        network = MockCAPNetwork()
        provider = ProofMeshProvider(network)
        negotiation = network.create_negotiation(
            service_id=PROOFMESH_SERVICE_ID,
            requester_agent_id="cap://test-requester.local",
            requirements=requirements,
        )
        order = provider.handle_negotiation_created(negotiation.negotiation_id)

        with self.assertRaises(ValueError):
            provider.handle_order_paid(order.order_id)

    def test_canonical_cases_run_through_mock_lifecycle(self):
        expectations = {
            "supported_artifact.json": {
                "is_verified": True,
                "supported": 2,
                "unsupported": 0,
                "contradicted": 0,
            },
            "unsupported_claim.json": {
                "is_verified": False,
                "supported": 1,
                "unsupported": 1,
                "contradicted": 0,
            },
            "contradicted_claim.json": {
                "is_verified": False,
                "supported": 0,
                "unsupported": 0,
                "contradicted": 2,
            },
        }

        for filename, expected in expectations.items():
            with self.subTest(filename=filename):
                demo = run_mock_cap_lifecycle(_load_case(filename))
                summary = summarize_lifecycle(demo)
                self.assertEqual(summary["order_status"], "completed")
                self.assertEqual(summary["is_verified"], expected["is_verified"])
                self.assertEqual(summary["claims_supported"], expected["supported"])
                self.assertEqual(summary["claims_unsupported"], expected["unsupported"])
                self.assertEqual(summary["claims_contradicted"], expected["contradicted"])
                self.assertEqual(summary["paid_amount_croo"], 0.25)
                self.assertEqual(summary["receipt_mode"], "mock_cap")

    def test_invalid_request_is_delivered_as_failed_audit(self):
        network = MockCAPNetwork()
        provider = ProofMeshProvider(network)
        negotiation = network.create_negotiation(
            service_id=PROOFMESH_SERVICE_ID,
            requester_agent_id="cap://test-requester.local",
            requirements={"task_id": "invalid-empty-request"},
        )
        order = provider.handle_negotiation_created(negotiation.negotiation_id)
        network.pay_order(order.order_id)
        delivery = provider.handle_order_paid(order.order_id)
        audit = delivery.deliverable_schema

        self.assertFalse(audit["is_verified"])
        self.assertEqual(audit["overall_confidence"], 0.0)
        self.assertIn("schema validation", audit["limitations"][0])
        self.assertEqual(network.get_order(order.order_id).status, "completed")


def _load_case(filename):
    path = ROOT / "examples" / "cases" / filename
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
