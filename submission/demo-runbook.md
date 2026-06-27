# ProofMesh Demo Runbook

Target: 4-5 minute demo video.

## Pre-Demo Setup

From the repository root:

```bash
PYTHONPATH=src .venv/bin/python examples/run_all_evidence.py
```

This regenerates:

- local audit artifacts
- Phase 1 canonical case outputs
- Phase 2 mock CAP lifecycle outputs
- Phase 3 live-readiness dry-run outputs

## Segment 1: Problem

Show `writeup/kaggle-writeup.md`.

Say:

Agents can sell outputs, but downstream buyers need to know what was checked and what evidence supports the claims. ProofMesh turns verification into a paid callable service.

## Segment 2: Local Verifier

Command:

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/research_claim.json --format markdown
```

Show:

- `is_verified: false`
- the overclaim about live settlement is contradicted

## Segment 3: Mock CAP Lifecycle

Command:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_demo.py
```

Show:

- `artifacts/phase2/mock-cap-demo-log.md`
- service registration
- negotiation
- payment event
- delivery
- receipt discipline

## Segment 4: Batch Evidence

Command:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_batch.py
```

Show:

- `artifacts/phase2/mock-cap-batch-summary.md`
- supported case verifies
- unsupported case fails
- contradicted case fails
- total mock cost is `0.75 CROO`

## Segment 5: Live Readiness

Command:

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
```

Show:

- `artifacts/phase3/live-readiness-report.md`
- service metadata ready
- SDK package confirmed as `croo-sdk` / Python module `croo`
- `CROO_API_KEY` required for a local live/staging run
- no live/staging order receipt attached yet

Say clearly:

This is live-ready dry-run evidence, not live settlement.

## Segment 6: Close

Show:

- `deployment/agent-store-listing.json`
- `submission/evidence-map.md`

Close:

ProofMesh demonstrates a reusable paid verification dependency for agent commerce. The local and mock evidence is complete; live CROO settlement is the remaining external integration step.
