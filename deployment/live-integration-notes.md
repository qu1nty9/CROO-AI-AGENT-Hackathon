# ProofMesh Live/Staging CROO Integration Notes

Status: live-ready scaffold implemented; live CROO transaction pending a registered service and staging/live order.

## What Is Implemented

- Environment-backed configuration in `src/proofmesh/config.py`
- Live readiness checks in `src/proofmesh/live_adapter.py`
- Service listing metadata in `deployment/agent-store-listing.json`
- Readiness report generator in `examples/check_live_readiness.py`
- Live-ready audit dry run in `examples/run_live_dry_run.py`
- Repository metadata set to `https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon`
- CROO Python SDK package confirmed as `croo-sdk`, importing module `croo`
- `CROO_API_KEY` supported as the official key variable; `CROO_SDK_KEY` remains a compatibility alias

## Current Public Signal

CROO setup instructions currently use `pip install croo-sdk`, `export CROO_API_KEY=...`, and a provider startup command. The installed package exposes `croo.AgentClient`, `croo.Config`, negotiation/order types, and WebSocket events.

## Required For True Live Integration

- CROO dashboard access
- `CROO_API_KEY`
- confirmed service registration method
- confirmed order negotiation and delivery method names
- staging or live Agent Store listing
- at least one transaction/order receipt or official staging receipt
- `Require Fund Transfer` should stay disabled for ProofMesh unless the service is redesigned to manage principal funds. ProofMesh sells a fixed-price verification report, not a swap/bridge/lend flow.

## Local Commands

Install the live SDK:

```bash
.venv/bin/pip install croo-sdk
```

Set the CROO dashboard key:

```bash
export CROO_API_KEY="croo_sk_..."
```

Check readiness:

```bash
PYTHONPATH=src .venv/bin/python examples/check_live_readiness.py
```

Run live-ready dry-run audit:

```bash
PYTHONPATH=src .venv/bin/python examples/run_live_dry_run.py
```

Run the CROO provider:

```bash
export PROOFMESH_MODE=staging
export PROOFMESH_PROVIDER_AGENT_ID="0xc38d5FE5125F5ce901768b26941Bac8758aCD46e"
PYTHONPATH=src .venv/bin/python examples/run_croo_provider.py
```

If `npx ts-node examples/provider.ts` fails because npm cannot download `ts-node`, use the Python provider above. It uses the installed `croo-sdk` package directly.

## Important Submission Rule

Until a real CROO order or official staging transaction exists, all Phase 3 artifacts must be labeled as `live_ready_dry_run`, not live settlement.
