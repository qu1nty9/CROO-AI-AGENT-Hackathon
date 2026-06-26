# ProofMesh Audit: case-unsupported-001

- Schema version: `proofmesh.verification.v1`
- Artifact type: `research_report`
- Audit mode: `source_coverage`
- Verified: `False`
- Overall confidence: `0.5`

## Source Coverage

- claims_total: 2
- claims_supported: 1
- claims_partial: 0
- claims_contradicted: 0
- claims_unsupported: 1
- sources_total: 2

## Claim Audits

### c1: supported

ProofMesh checks whether claims have source coverage, lexical support, and contradiction markers.

- Confidence: `0.91`
- Supporting sources:
  - `s1` ProofMesh MVP Limitations (0.9)
- Note: Claim has source coverage under the MVP scoring rule.

### c2: unsupported

ProofMesh guarantees factual truth for every possible claim.

- Confidence: `0.1`
- Supporting sources:
  - `s2` Unrelated Source (0.143)
- Note: No source reached the minimum lexical support threshold.

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
