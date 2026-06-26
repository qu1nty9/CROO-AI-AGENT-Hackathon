# Experiment: ProofMesh Mock CAP Lifecycle

Date: 2026-06-26

## Goal

Close Phase 2 by proving that ProofMesh can run as a separate provider in a local A2A commerce flow:

requester -> negotiation -> payment event -> audit -> delivery -> receipt/log

## Command

```bash
PYTHONPATH=src python3 examples/run_mock_cap_demo.py
```

## Input

Default request:

- `examples/cases/contradicted_claim.json`

This request contains overclaims about live CROO settlement and local verification proving live CAP behavior.

## Output

Saved artifacts:

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`
- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`

## Result

Lifecycle events:

- `service_registered`
- `negotiation_created`
- `negotiation_accepted`
- `order_paid`
- `order_completed`

Ledger events:

- `order_paid`: `0.25 CROO`
- `order_delivered`: `0.0 CROO`

Delivered audit:

- `is_verified: false`
- `overall_confidence: 0.0`
- `claims_contradicted: 2`
- `cap_receipt.mode: mock_cap`

Tests:

- `PYTHONPATH=src python3 -m unittest discover -s tests`
- 12 tests passed

Batch summary:

| Case | Verified | Supported | Unsupported | Contradicted | Mock cost |
| --- | --- | ---: | ---: | ---: | ---: |
| supported | true | 2 | 0 | 0 | 0.25 CROO |
| unsupported | false | 1 | 1 | 0 | 0.25 CROO |
| contradicted | false | 0 | 0 | 2 | 0.25 CROO |

## Interpretation

Phase 2 is ready for Kaggle writeup evidence. ProofMesh is no longer only a local function or CLI; it has a provider/requester boundary and a reproducible mock commerce lifecycle.

## Limitation

This is mock CAP evidence. It is not live CROO settlement. Live/staging integration remains a later phase.
