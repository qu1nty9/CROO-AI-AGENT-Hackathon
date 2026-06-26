# Experiment: ProofMesh Live/Staging Readiness

Date: 2026-06-26

## Goal

Close the locally actionable part of Phase 3 by preparing ProofMesh for live/staging CROO integration without falsely claiming a live settlement.

## Commands

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
PYTHONPATH=src python3 examples/run_live_dry_run.py
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Outputs

- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-readiness-report.md`
- `artifacts/phase3/live-dry-run-audit.json`
- `artifacts/phase3/live-dry-run-audit.md`

## Result

Readiness: false.

Passing checks:

- `croo_api_url`
- `croo_ws_url`
- `service_metadata`

Blocking checks:

- `CROO_SDK_KEY` is missing
- Python module `croo` is not installed or not discoverable

Dry-run audit:

- `cap_receipt.mode: live_ready_dry_run`
- no live CROO order was created
- no live settlement was created

Tests:

- 16 tests passed

## Interpretation

The project is ready for live integration from a code and metadata standpoint. The remaining work requires external CROO dashboard/SDK state rather than local code changes.

## Submission Discipline

Do not describe Phase 3 artifacts as live settlement. The correct label is `live-ready dry run` until a real CROO order or official staging transaction is attached.

