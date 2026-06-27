# ProofMesh Live-Ready Dry Run

- Task: `case-supported-001`
- Verified: `True`
- Confidence: `1.0`
- Receipt mode: `live_ready_dry_run`
- Readiness ready: `True`

## Coverage

- Claims total: `2`
- Supported: `2`
- Unsupported: `0`
- Contradicted: `0`

## Readiness Checks

| Check | OK | Detail |
| --- | --- | --- |
| croo_sdk_key | True | CROO_API_KEY/CROO_SDK_KEY is set |
| croo_sdk_package | True | Python module 'croo' is importable |
| croo_api_url | True | https://api.croo.network |
| croo_ws_url | True | wss://api.croo.network/ws |
| service_metadata | True | service_id=proofmesh-source-coverage-audit; provider_agent_id=0xc38d5FE5125F5ce901768b26941Bac8758aCD46e |

## Limitation

Dry-run only. No live CROO order or settlement was created.
