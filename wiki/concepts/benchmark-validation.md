# Concept: Benchmark Validation

Status: mini benchmark implemented for judge-facing reproducibility.

## Purpose

The benchmark gives ProofMesh a small, deterministic regression suite beyond hand-picked examples. It is designed to show that the transparent MVP consistently separates three supported statuses:

- `supported`
- `unsupported`
- `contradicted`

## Current Artifact

- Script: `examples/run_benchmark.py`
- JSON output: `artifacts/benchmark/proofmesh-mini-benchmark.json`
- Markdown output: `artifacts/benchmark/proofmesh-mini-benchmark.md`
- Unit guard: `tests/test_benchmark.py`

## Current Result

- Cases: 30
- Supported: 10
- Unsupported: 10
- Contradicted: 10
- Accuracy on this synthetic regression set: 1.0

## Interpretation

This benchmark is useful for reproducibility and regression testing. It should not be described as evidence of broad factual truth verification. The cases are intentionally simple and synthetic, so they support the engineering claim that the MVP behaves consistently under known inputs.

## Next Research Step

For an arXiv-style paper, this should grow into a larger benchmark with human-authored labels, adversarial paraphrases, source ambiguity, and comparisons against requester self-checking.
