# ProofMesh Live-Ready Dry Run

- Task: `case-supported-001`
- Verified: `True`
- Confidence: `1.0`
- Receipt mode: `live_ready_dry_run`
- Readiness ready: `False`

## Coverage

- Claims total: `2`
- Supported: `2`
- Unsupported: `0`
- Contradicted: `0`

## Readiness Checks

| Check | OK | Detail |
| --- | --- | --- |
| croo_sdk_key | False | CROO_SDK_KEY is missing |
| croo_sdk_package | False | Python module 'croo' is not installed or not discoverable |
| croo_api_url | True | https://api.croo.network |
| croo_ws_url | True | wss://api.croo.network/ws |
| service_metadata | True | service_id=proofmesh-source-coverage-audit; provider_agent_id=cap://proofmesh-provider.local |

## Limitation

Dry-run only. No live CROO order or settlement was created.
