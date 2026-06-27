# ProofMesh CROO Live Readiness

- Ready: `False`
- Mode: `local`
- API URL: `https://api.croo.network`
- WS URL: `wss://api.croo.network/ws`
- Service ID: `proofmesh-source-coverage-audit`

## Checks

| Check | OK | Detail |
| --- | --- | --- |
| croo_sdk_key | False | CROO_API_KEY/CROO_SDK_KEY is missing |
| croo_sdk_package | True | Python module 'croo' is importable |
| croo_api_url | True | https://api.croo.network |
| croo_ws_url | True | wss://api.croo.network/ws |
| service_metadata | True | service_id=proofmesh-source-coverage-audit; provider_agent_id=cap://proofmesh-provider.local |

## Next Steps

- Set CROO_API_KEY from the CROO Agent dashboard; CROO_SDK_KEY is accepted as a legacy alias.

## Service Listing

- Agent: `ProofMesh`
- Service: `proofmesh-source-coverage-audit`
- Price: `0.25 CROO`
