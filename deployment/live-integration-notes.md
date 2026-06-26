# ProofMesh Live/Staging CROO Integration Notes

Status: live-ready scaffold implemented; live CROO transaction pending credentials and current SDK/API confirmation.

## What Is Implemented

- Environment-backed configuration in `src/proofmesh/config.py`
- Live readiness checks in `src/proofmesh/live_adapter.py`
- Service listing metadata in `deployment/agent-store-listing.json`
- Readiness report generator in `examples/check_live_readiness.py`
- Live-ready audit dry run in `examples/run_live_dry_run.py`
- Repository metadata set to `https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon`

## Current Public Signal

The public Agent Store at `https://agent.croo.network/` exposes Store, Connect, and Register Agent surfaces. Public SDK/API documentation was not discoverable from the available page during this pass.

## Required For True Live Integration

- CROO dashboard access
- `CROO_SDK_KEY`
- confirmed current Python SDK package/import name
- confirmed service registration method
- confirmed order negotiation and delivery method names
- staging or live Agent Store listing
- at least one transaction/order receipt or official staging receipt

## Local Commands

Check readiness:

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
```

Run live-ready dry-run audit:

```bash
PYTHONPATH=src python3 examples/run_live_dry_run.py
```

## Important Submission Rule

Until a real CROO order or official staging transaction exists, all Phase 3 artifacts must be labeled as `live_ready_dry_run`, not live settlement.
