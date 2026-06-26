# ProofMesh Phase 1 Demo Cases

These cases are the canonical local acceptance scenarios for the Kaggle writeup.

## Cases

- `supported_artifact.json`: all claims have source coverage; expected `is_verified: true`.
- `unsupported_claim.json`: one claim is supported and one claim lacks source support; expected `is_verified: false`.
- `contradicted_claim.json`: claims overstate live CAP behavior; expected `is_verified: false`.

## Generate Outputs

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/supported_artifact.json --format json --output artifacts/phase1/supported-artifact.json
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/unsupported_claim.json --format json --output artifacts/phase1/unsupported-claim.json
PYTHONPATH=src python3 -m proofmesh.cli audit examples/cases/contradicted_claim.json --format json --output artifacts/phase1/contradicted-claim.json
```

Markdown outputs use the same commands with `--format markdown`.

