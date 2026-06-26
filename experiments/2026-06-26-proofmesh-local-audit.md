# Experiment: ProofMesh Local Audit MVP

Date: 2026-06-26

## Goal

Verify that the first deterministic ProofMesh MVP can audit a structured claim set and avoid overclaiming live CROO settlement.

## Command

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m proofmesh.cli audit examples/research_claim.json --format markdown
```

## Input

`examples/research_claim.json`

The example contains three claims:

- CAP lets agents discover, hire, and pay other agents on-chain.
- The hackathon requires Agent Store listing, CAP integration, open source code, demo plus README, and DoraHacks BUIDL.
- ProofMesh has already completed a live on-chain settlement on CROO mainnet.

## Result

Unit tests:

- 4 tests passed.

Audit output:

- `is_verified`: false
- `overall_confidence`: 0.333
- claims supported: 2
- claims contradicted: 1

## Interpretation

The MVP correctly blocks full verification when a claim overstates project status. This is important for the final hackathon submission because mock CAP lifecycle, local tests, and live settlement must be clearly separated.

## Judging Relevance

This experiment demonstrates the central product claim: ProofMesh can act as a conservative verification dependency for other agents before they deliver or publish outputs.

