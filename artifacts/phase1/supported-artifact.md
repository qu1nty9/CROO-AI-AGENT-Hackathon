# ProofMesh Audit: case-supported-001

- Schema version: `proofmesh.verification.v1`
- Artifact type: `research_report`
- Audit mode: `source_coverage`
- Verified: `True`
- Overall confidence: `1.0`

## Source Coverage

- claims_total: 2
- claims_supported: 2
- claims_partial: 0
- claims_contradicted: 0
- claims_unsupported: 0
- sources_total: 2

## Claim Audits

### c1: supported

ProofMesh audits generated agent outputs before final delivery.

- Confidence: `0.85`
- Supporting sources:
  - `s1` ProofMesh Project README (0.75)
- Note: Claim has source coverage under the MVP scoring rule.

### c2: supported

CAP lets agents discover, hire, and pay other agents on-chain.

- Confidence: `0.861`
- Supporting sources:
  - `s2` Local CROO Hackathon Brief (0.778)
- Note: Claim has source coverage under the MVP scoring rule.

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
