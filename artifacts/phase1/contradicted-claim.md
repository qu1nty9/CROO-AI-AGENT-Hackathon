# ProofMesh Audit: case-contradicted-001

- Schema version: `proofmesh.verification.v1`
- Artifact type: `research_report`
- Audit mode: `source_coverage`
- Verified: `False`
- Overall confidence: `0.0`

## Source Coverage

- claims_total: 2
- claims_supported: 0
- claims_partial: 0
- claims_contradicted: 2
- claims_unsupported: 0
- sources_total: 2

## Claim Audits

### c1: contradicted

ProofMesh has already completed a live CROO settlement.

- Confidence: `0.1`
- Supporting sources:
  - `s1` Current Local Status (0.333)
- Contradiction sources: `s1`
- Note: Potential negation mismatch detected in overlapping source text.

### c2: contradicted

Local verification is enough to prove live CAP behavior.

- Confidence: `0.1`
- Supporting sources:
  - `s2` Submission Discipline (0.429)
- Contradiction sources: `s2`
- Note: Potential negation mismatch detected in overlapping source text.

## Limitations

- This MVP performs transparent lexical and source-coverage checks.
- It is not a guarantee of factual truth.
- Semantic verification, web retrieval, and human calibration are future work.

## CAP Receipt

```json
{
  "mode": "local",
  "settlement_status": "not_settled",
  "note": "No live CAP settlement attached to this local audit."
}
```
