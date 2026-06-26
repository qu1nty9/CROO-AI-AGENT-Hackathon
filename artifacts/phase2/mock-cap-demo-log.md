# ProofMesh Mock CAP Lifecycle Demo

## Summary

- Service: `proofmesh-source-coverage-audit`
- Requester: `cap://research-requester.local`
- Provider: `cap://proofmesh-provider.local`
- Negotiation: `neg_6df57e255f`
- Order: `order_6e8f4424d3`
- Delivery: `del_d990f61559`
- Payment tx: `0xmock1c257f163fce41c5987d5bf0`
- Payment block: `9000001`
- Final order status: `completed`
- Audit verified: `False`
- Audit confidence: `0.0`

## CAP Lifecycle

- `service_registered` at `2026-06-26T20:31:40.306548+00:00`
- `negotiation_created` at `2026-06-26T20:31:40.306672+00:00`
- `negotiation_accepted` at `2026-06-26T20:31:40.306697+00:00`
- `order_paid` at `2026-06-26T20:31:40.306716+00:00`
- `order_completed` at `2026-06-26T20:31:40.306898+00:00`

## Delivered Audit

- Schema version: `proofmesh.verification.v1`
- Task: `case-contradicted-001`
- Artifact type: `research_report`
- Audit mode: `source_coverage`
- Verified: `False`
- Overall confidence: `0.0`
- Claims total: `2`
- Supported: `0`
- Unsupported: `0`
- Contradicted: `2`

## Claim Results

### c1: contradicted

ProofMesh has already completed a live CROO settlement.

- Confidence: `0.1`
- Contradiction sources: `s1`
- Note: Potential negation mismatch detected in overlapping source text.

### c2: contradicted

Local verification is enough to prove live CAP behavior.

- Confidence: `0.1`
- Contradiction sources: `s2`
- Note: Potential negation mismatch detected in overlapping source text.

## Receipt Discipline

This is a mock CAP lifecycle for local reproducibility. It is not a live CROO settlement.
