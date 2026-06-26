# ProofMesh Evidence Map

This page maps judging claims to reproducible artifacts.

## Core Claim

ProofMesh is a paid verification and provenance agent that another agent can call before delivering generated output.

Evidence:

- `src/proofmesh/auditor.py`
- `src/proofmesh/schema.py`
- `examples/cases/`
- `artifacts/phase1/`

## A2A Mock CAP Claim

ProofMesh can run behind a requester/provider boundary with negotiation, payment event, audit delivery, and receipt/log metadata.

Evidence:

- `src/proofmesh/cap_mock.py`
- `src/proofmesh/provider.py`
- `src/proofmesh/mock_lifecycle.py`
- `examples/run_mock_cap_demo.py`
- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`

## Batch Validation Claim

The same mock CAP flow handles supported, unsupported, and contradicted artifacts.

Evidence:

- `examples/run_mock_cap_batch.py`
- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`

## Live Readiness Claim

ProofMesh has service metadata, env config, readiness checks, and a live-ready dry-run adapter, but no live settlement is claimed.

Evidence:

- `src/proofmesh/config.py`
- `src/proofmesh/live_adapter.py`
- `deployment/agent-store-listing.json`
- `deployment/live-integration-notes.md`
- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-dry-run-audit.json`

## Reproducibility Claim

The local verifier, mock CAP lifecycle, batch evidence, and live-ready dry run can be regenerated locally.

Command:

```bash
PYTHONPATH=src python3 examples/run_all_evidence.py
```

Expected current test result:

- 16 tests pass

## Non-Claims

These are explicitly not claimed yet:

- live CROO settlement
- live Agent Store listing
- calibrated truth probability
- clinical or regulated-domain readiness

