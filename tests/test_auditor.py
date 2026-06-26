import json
from pathlib import Path
import unittest

from proofmesh import SCHEMA_VERSION, RequestValidationError, audit_request


ROOT = Path(__file__).resolve().parents[1]


class AuditRequestTest(unittest.TestCase):
    def test_supported_claim_has_confidence(self):
        report = audit_request(
            {
                "task_id": "unit-1",
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
                        "title": "Brief",
                        "text": "CAP lets any agent discover hire and pay any other agent on-chain.",
                    }
                ],
            }
        )

        self.assertTrue(report["is_verified"])
        self.assertEqual(report["schema_version"], SCHEMA_VERSION)
        self.assertEqual(report["audit_mode"], "source_coverage")
        self.assertEqual(report["claim_audits"][0]["status"], "supported")
        self.assertGreaterEqual(report["overall_confidence"], 0.7)

    def test_unsupported_claim_is_not_verified(self):
        report = audit_request(
            {
                "task_id": "unit-2",
                "artifact_type": "claim_set",
                "claims": [
                    {
                        "id": "c1",
                        "text": "ProofMesh has completed live settlement on mainnet",
                        "source_ids": ["s1"],
                    }
                ],
                "sources": [
                    {
                        "id": "s1",
                        "title": "Status",
                        "text": "The current MVP runs locally and has no live settlement receipt.",
                    }
                ],
            }
        )

        self.assertFalse(report["is_verified"])
        self.assertIn(report["claim_audits"][0]["status"], {"partial", "contradicted", "unsupported"})

    def test_artifact_text_can_generate_claims(self):
        report = audit_request(
            {
                "task_id": "unit-3",
                "artifact_type": "research_report",
                "artifact_text": "Agents can hire verification services before delivery. Short.",
                "sources": [
                    {
                        "id": "s1",
                        "text": "Agents can hire verification services before delivery.",
                    }
                ],
            }
        )

        self.assertEqual(report["source_coverage"]["claims_total"], 1)

    def test_partial_claim_prevents_verified_status(self):
        report = audit_request(
            {
                "task_id": "unit-4",
                "artifact_type": "claim_set",
                "claims": [
                    {
                        "id": "c1",
                        "text": "CAP lets agents discover hire and pay other agents on-chain",
                        "source_ids": ["s1"],
                    },
                    {
                        "id": "c2",
                        "text": "ProofMesh completed live settlement on CROO mainnet",
                        "source_ids": ["s2"],
                    },
                ],
                "sources": [
                    {
                        "id": "s1",
                        "text": "CAP lets any agent discover hire and pay any other agent on-chain.",
                    },
                    {
                        "id": "s2",
                        "text": "ProofMesh has no live settlement receipt yet.",
                    },
                ],
            }
        )

        self.assertFalse(report["is_verified"])

    def test_missing_claims_and_artifact_text_is_invalid(self):
        with self.assertRaises(RequestValidationError):
            audit_request({"task_id": "unit-invalid", "artifact_type": "claim_set"})

    def test_canonical_supported_case(self):
        report = audit_request(_load_case("supported_artifact.json"))

        self.assertTrue(report["is_verified"])
        self.assertEqual(report["source_coverage"]["claims_supported"], 2)
        self.assertEqual(report["source_coverage"]["claims_contradicted"], 0)

    def test_canonical_unsupported_case(self):
        report = audit_request(_load_case("unsupported_claim.json"))

        self.assertFalse(report["is_verified"])
        statuses = {item["claim_id"]: item["status"] for item in report["claim_audits"]}
        self.assertEqual(statuses["c1"], "supported")
        self.assertEqual(statuses["c2"], "unsupported")

    def test_canonical_contradicted_case(self):
        report = audit_request(_load_case("contradicted_claim.json"))

        self.assertFalse(report["is_verified"])
        self.assertEqual(report["source_coverage"]["claims_contradicted"], 2)
        self.assertTrue(all(item["contradiction_sources"] for item in report["claim_audits"]))


def _load_case(filename):
    path = ROOT / "examples" / "cases" / filename
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
