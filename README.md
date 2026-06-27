# ProofMesh: CAP Verification and Provenance Agent

ProofMesh is a CROO AI Agent Hackathon project.

`ProofMesh` is a paid, callable verification agent for the CROO Agent Protocol. Other agents can hire it to audit generated outputs, research claims, datasets, or reports. It returns a structured evidence package with provenance, contradiction checks, confidence scoring, and settlement metadata.

Repository: https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

## Current Status

- Local verifier: implemented
- Mock CAP requester/provider lifecycle: implemented
- Batch evidence for supported/unsupported/contradicted cases: implemented
- Live/staging CROO readiness scaffold: implemented
- CROO Python SDK: package confirmed as `croo-sdk`, importing module `croo`
- Live CROO settlement: pending registered service and staging/live order receipt
- Agent Store listing: metadata prepared, live listing pending

## Recommended Hackathon Tracks

- Data & Verification Agents
- Research & Intelligence Agents

## Quickstart

Run all local evidence generation and tests:

```bash
python3 -m venv .venv
.venv/bin/pip install croo-sdk
PYTHONPATH=src .venv/bin/python examples/run_all_evidence.py
```

Expected current result:

- 17 tests pass
- local audit artifacts regenerate
- Phase 1/2/3 artifacts regenerate
- committed staging readiness is `True` when generated with `CROO_API_KEY`
- third-party reruns without `CROO_API_KEY` will show the key check as missing
- live settlement remains a dry run until a staging/live order receipt is attached

Run the local deterministic verifier:

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/research_claim.json --format markdown
```

Run tests:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Expected current behavior: the example report is not fully verified, because one claim says a live CROO settlement already happened while the local status source says no live settlement receipt exists yet.

Run the Phase 1 canonical demo cases:

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/supported_artifact.json --format markdown
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/unsupported_claim.json --format markdown
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/contradicted_claim.json --format markdown
```

Saved outputs live under `artifacts/phase1/`.

Run the Phase 2 mock CAP lifecycle demo:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_demo.py
```

Saved lifecycle evidence:

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`

Run all canonical cases through mock CAP:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_batch.py
```

Saved batch evidence:

- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`

Check Phase 3 live/staging readiness:

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
```

For CROO live/staging setup:

```bash
.venv/bin/pip install croo-sdk
export CROO_API_KEY="croo_sk_..."
PYTHONPATH=src .venv/bin/python examples/check_live_readiness.py
```

ProofMesh also accepts `CROO_SDK_KEY` as a legacy alias. Keep `Require Fund Transfer` disabled for the current service listing; ProofMesh returns a fixed-price verification report and does not transfer principal funds.

Run a live-ready dry-run audit:

```bash
PYTHONPATH=src python3 examples/run_live_dry_run.py
```

Saved Phase 3 evidence:

- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-readiness-report.md`
- `artifacts/phase3/live-dry-run-audit.json`
- `artifacts/phase3/live-dry-run-audit.md`

## Key Artifacts

- Kaggle writeup draft: `writeup/kaggle-writeup.md`
- Architecture draft: `writeup/architecture.md`
- Evidence map: `submission/evidence-map.md`
- Demo runbook: `submission/demo-runbook.md`
- DoraHacks copy draft: `submission/dorahacks-copy.md`
- Agent Store listing draft: `deployment/agent-store-listing.json`
- Live integration notes: `deployment/live-integration-notes.md`

## Important Limitation

Mock CAP artifacts and live-ready dry-run artifacts are not live CROO settlement. The repository is explicit about this because ProofMesh is designed to prevent overclaims.

## Source Discipline

The workspace follows an LLM Wiki approach: raw sources stay unchanged, while the `wiki/` folder accumulates maintained summaries, decisions, experiment notes, and writeup material.
