# Concept: Live CROO Readiness

Status: live-ready scaffold complete; live transaction pending service registration and staging/live order receipt.

## Implemented

- `src/proofmesh/config.py`
- `src/proofmesh/live_adapter.py`
- `deployment/agent-store-listing.json`
- `deployment/env.example`
- `deployment/live-integration-notes.md`
- `examples/check_live_readiness.py`
- `examples/run_live_dry_run.py`
- `tests/test_live_adapter.py`
- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-readiness-report.md`
- `artifacts/phase3/live-dry-run-audit.json`
- `artifacts/phase3/live-dry-run-audit.md`

## Current Readiness

Ready: false.

Passing checks:

- `croo_api_url`
- `croo_ws_url`
- `service_metadata`

Blocking checks:

- `CROO_API_KEY`/`CROO_SDK_KEY` is missing in the public artifact environment
- no live/staging order receipt has been attached yet

Resolved checks:

- current SDK package: `croo-sdk`
- current Python import module: `croo`
- official key env var from CROO instruction: `CROO_API_KEY`
- compatibility key env var accepted by ProofMesh: `CROO_SDK_KEY`

## Submission Discipline

All Phase 3 artifacts must be labeled `live_ready_dry_run` until a real CROO order or official staging transaction exists.

## Next Live Steps

1. Get CROO dashboard access.
2. Install `croo-sdk` in `.venv`.
3. Set `CROO_API_KEY`.
4. Register `proofmesh-source-coverage-audit`.
5. Keep `Require Fund Transfer` disabled for the current fixed-price audit service.
6. Run one staging/live negotiation and delivery.
7. Attach receipt, screenshot, or transaction/order ID to `artifacts/phase3/`.
