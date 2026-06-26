# Experiment: ProofMesh Phase 1 Acceptance

Date: 2026-06-26

## Goal

Close Phase 1 for the Kaggle/DoraHacks submission by proving that the local verifier has:

- stable request/response schema
- runtime validation
- canonical supported, unsupported, and contradicted examples
- saved outputs
- unit test coverage

## Schema

Current schema version: `proofmesh.verification.v1`

Implementation:

- `src/proofmesh/schema.py`
- `src/proofmesh/auditor.py`
- `src/proofmesh/cli.py`

## Commands

```bash
PYTHONPATH=src python3 -m unittest discover -s tests

PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/supported_artifact.json --format json --output artifacts/phase1/supported-artifact.json
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/unsupported_claim.json --format json --output artifacts/phase1/unsupported-claim.json
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/contradicted_claim.json --format json --output artifacts/phase1/contradicted-claim.json
```

## Results

Unit tests:

- 8 tests passed

Canonical cases:

| Case | Output | Result |
| --- | --- | --- |
| supported artifact | `artifacts/phase1/supported-artifact.json` | `is_verified: true` |
| unsupported claim | `artifacts/phase1/unsupported-claim.json` | `is_verified: false` |
| contradicted claim | `artifacts/phase1/contradicted-claim.json` | `is_verified: false` |

## Interpretation

Phase 1 is ready for the Kaggle writeup. ProofMesh can now demonstrate the core local value proposition before CAP is attached: it can approve supported artifacts and block missing-evidence or overclaiming artifacts.

## Next Step

Build the mock CAP lifecycle:

requester -> negotiation -> payment event -> audit -> delivery -> receipt/log

