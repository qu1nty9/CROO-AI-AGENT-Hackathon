# Concept: ProofMesh Mock CAP Lifecycle

Status: implemented locally.

## Purpose

The mock CAP lifecycle provides reproducible local evidence for the Kaggle writeup before live CROO credentials or current SDK integration are available.

It is not a live CROO settlement. It is a local A2A commerce simulation that proves the product boundary:

requester -> negotiation -> payment event -> audit -> delivery -> receipt/log

## Components

- `src/proofmesh/cap_mock.py`: in-memory CAP-like network
- `src/proofmesh/provider.py`: ProofMesh provider wrapper
- `examples/run_mock_cap_demo.py`: requester/provider demo runner
- `examples/run_mock_cap_batch.py`: batch runner for all canonical cases
- `tests/test_cap_mock.py`: lifecycle tests
- `artifacts/phase2/mock-cap-demo-log.json`: saved JSON evidence
- `artifacts/phase2/mock-cap-demo-log.md`: saved Markdown evidence
- `artifacts/phase2/mock-cap-batch-summary.json`: batch cost/latency summary
- `artifacts/phase2/mock-cap-batch-summary.md`: batch writeup table

## Lifecycle Events

The current demo records these events:

1. `service_registered`
2. `negotiation_created`
3. `negotiation_accepted`
4. `order_paid`
5. `order_completed`

The mock ledger records:

- `order_paid` with amount `0.25 CROO`
- `order_delivered` with amount `0.0 CROO`

## Batch Evidence

The batch demo runs the supported, unsupported, and contradicted canonical cases through the same mock CAP lifecycle.

Current batch summary:

- 3 cases
- total mock cost: `0.75 CROO`
- each case follows the same lifecycle events
- supported case is verified
- unsupported and contradicted cases are not verified

## Judging Use

This artifact shows that CAP is not decorative in the project story. ProofMesh is called across a provider/requester boundary and delivers machine-readable audit output after a payment event.

## Limitation

All IDs, block numbers, and transaction hashes are local mock values. The final submission must label them as mock evidence unless live CROO integration is added later.
