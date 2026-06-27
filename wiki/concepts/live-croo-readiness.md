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

Ready: true for the maintained staging artifact generated with `CROO_API_KEY`.

Passing checks:

- `croo_sdk_key`
- `croo_sdk_package`
- `croo_api_url`
- `croo_ws_url`
- `service_metadata`

Blocking checks:

- no live/staging order receipt has been attached yet

Resolved checks:

- current SDK package: `croo-sdk`
- current Python import module: `croo`
- official key env var from CROO instruction: `CROO_API_KEY`
- compatibility key env var accepted by ProofMesh: `CROO_SDK_KEY`

## Submission Discipline

All Phase 3 artifacts must be labeled `live_ready_dry_run` until a real CROO order or official staging transaction exists.

## Next Live Steps

1. Register or confirm `proofmesh-source-coverage-audit`.
2. Keep `Require Fund Transfer` disabled for the current fixed-price audit service.
3. Run one staging/live negotiation and delivery.
4. Attach receipt, screenshot, or transaction/order ID to `artifacts/phase3/`.
