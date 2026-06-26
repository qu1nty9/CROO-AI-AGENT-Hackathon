# ProofMesh Audit: demo-research-001

- Schema version: `proofmesh.verification.v1`
- Artifact type: `research_report`
- Audit mode: `source_coverage`
- Verified: `False`
- Overall confidence: `0.333`

## Source Coverage

- claims_total: 3
- claims_supported: 2
- claims_partial: 0
- claims_contradicted: 1
- claims_unsupported: 0
- sources_total: 3

## Claim Audits

### c1: supported

CAP lets agents discover, hire, and pay other agents on-chain.

- Confidence: `0.861`
- Supporting sources:
  - `s1` Local CROO Hackathon Brief (0.778)
- Note: Claim has source coverage under the MVP scoring rule.

### c2: supported

The hackathon requires every build to include an Agent Store listing, CAP integration, open source code, a demo plus README, and a DoraHacks BUIDL.

- Confidence: `0.817`
- Supporting sources:
  - `s2` Local Submission Requirements (0.667)
- Note: Claim has source coverage under the MVP scoring rule.

### c3: contradicted

ProofMesh has already completed a live on-chain settlement on CROO mainnet.

- Confidence: `0.1`
- Supporting sources:
  - `s3` Current Local Status (0.25)
- Contradiction sources: `s3`
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
