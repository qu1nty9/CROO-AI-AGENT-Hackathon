# ProofMesh: A Paid Verification Agent for Trustworthy CROO Workflows

Repository: https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

## TL;DR

ProofMesh is a paid verification and provenance agent for CROO/CAP-style agent commerce. A requester agent can hire ProofMesh before delivering a generated report, dataset summary, or claim bundle. ProofMesh checks each claim against supplied sources, flags unsupported or contradicted statements, returns confidence and limitation metadata, and attaches lifecycle receipt information to the delivered audit.

The core thesis is simple: in an agent marketplace, verification should itself be a callable paid service.

Recommended tracks:

- Data & Verification Agents
- Research & Intelligence Agents

## Problem

Most agent demos focus on generation: summaries, research, code, analytics, or recommendations. Once agents sell those outputs, a second problem appears: buyers need to know what was checked, which sources were used, and whether the output overclaims.

If every agent implements its own quality checks, verification becomes duplicated and inconsistent. ProofMesh treats verification as a reusable dependency. A requester agent can buy an audit from ProofMesh before passing its own output to a customer.

## What ProofMesh Does

ProofMesh provides a `source_coverage_audit` service. The requester sends:

- an artifact type
- claims or raw artifact text
- sources
- optional claim-to-source links

ProofMesh returns:

- artifact-level `is_verified`
- overall confidence
- claim-level audit statuses
- source coverage counts
- contradiction flags
- limitations
- CAP/CROO receipt metadata

The current MVP is intentionally transparent. It does not claim broad semantic truth verification. It performs deterministic source-coverage and local contradiction checks so every result is reproducible from code and saved artifacts.

## Architecture

ProofMesh separates the verification core from the agent-commerce boundary.

```text
Requester Agent
  -> VerificationRequest: claims + sources
  -> CROO/CAP service boundary
  -> ProofMesh Provider
  -> Schema validation
  -> Audit core
  -> VerificationResponse: audit + limitations + receipt metadata
```

The repository also includes a mock CAP network and a live/staging CROO provider runner:

- `src/proofmesh/auditor.py`: deterministic audit core
- `src/proofmesh/schema.py`: request normalization and validation
- `src/proofmesh/cap_mock.py`: local CAP-style negotiation/payment/delivery lifecycle
- `src/proofmesh/provider.py`: mock ProofMesh provider wrapper
- `src/proofmesh/croo_provider.py`: Python provider runner using the official `croo-sdk`
- `src/proofmesh/live_adapter.py`: live/staging readiness and dry-run boundary

The fuller architecture diagrams are in `writeup/architecture.md`.

## Request And Response Contract

The request schema is explicit so another agent can call ProofMesh without prompt interpretation.

```json
{
  "task_id": "demo-research-001",
  "artifact_type": "research_report",
  "claims": [
    {
      "id": "c1",
      "text": "CAP lets agents discover, hire, and pay other agents on-chain.",
      "source_ids": ["s1"]
    }
  ],
  "sources": [
    {
      "id": "s1",
      "title": "Local CROO Hackathon Brief",
      "url": "docs/CROO AI AGENT Hackathon.docx",
      "text": "CAP is a permissionless A2A standard that lets any Agent discover, hire, and pay any other Agent on-chain."
    }
  ],
  "audit_mode": "source_coverage"
}
```

The response is machine-readable and conservative. One contradicted or unsupported claim prevents the artifact from being marked fully verified.

```json
{
  "schema_version": "proofmesh.verification.v1",
  "task_id": "demo-research-001",
  "artifact_type": "research_report",
  "audit_mode": "source_coverage",
  "is_verified": false,
  "overall_confidence": 0.333,
  "source_coverage": {
    "claims_total": 3,
    "claims_supported": 2,
    "claims_partial": 0,
    "claims_contradicted": 1,
    "claims_unsupported": 0,
    "sources_total": 3
  },
  "claim_audits": [],
  "limitations": [],
  "cap_receipt": {
    "mode": "local",
    "settlement_status": "not_settled"
  }
}
```

## Evidence Summary

| Claim | Evidence | Status |
| --- | --- | --- |
| ProofMesh audits source-backed claims | `src/proofmesh/auditor.py`, `artifacts/demo-audit.json` | implemented |
| ProofMesh blocks overclaims | `artifacts/demo-audit.md`, `experiments/2026-06-26-proofmesh-local-audit.md` | implemented |
| ProofMesh handles supported, unsupported, and contradicted cases | `examples/cases/`, `artifacts/phase1/` | implemented |
| ProofMesh runs through an A2A requester/provider lifecycle | `src/proofmesh/cap_mock.py`, `artifacts/phase2/mock-cap-demo-log.json` | implemented as mock CAP |
| ProofMesh reports batch mock CAP results and cost | `artifacts/phase2/mock-cap-batch-summary.json` | implemented as mock CAP |
| ProofMesh has a deterministic mini benchmark | `examples/run_benchmark.py`, `artifacts/benchmark/proofmesh-mini-benchmark.json` | implemented |
| ProofMesh is CROO SDK/staging-ready | `artifacts/phase3/live-readiness-report.json`, `src/proofmesh/croo_provider.py` | implemented |
| ProofMesh completed live CROO settlement | none | not claimed |

## Phase 1: Local Verifier

The first milestone was a dependency-free verifier that can run locally and produce deterministic JSON/Markdown outputs.

Command:

```bash
PYTHONPATH=src .venv/bin/python -m proofmesh.cli audit examples/research_claim.json --format markdown
```

The demo intentionally includes an overclaim that live CROO settlement already happened. ProofMesh marks the artifact as not fully verified, which is the desired behavior.

Saved outputs:

- `artifacts/demo-audit.json`
- `artifacts/demo-audit.md`
- `artifacts/phase1/supported-artifact.json`
- `artifacts/phase1/unsupported-claim.json`
- `artifacts/phase1/contradicted-claim.json`

Canonical Phase 1 cases:

| Case | Expected result | Artifact |
| --- | --- | --- |
| Supported artifact | `is_verified: true` | `artifacts/phase1/supported-artifact.json` |
| Unsupported claim | `is_verified: false` | `artifacts/phase1/unsupported-claim.json` |
| Contradicted claim | `is_verified: false` | `artifacts/phase1/contradicted-claim.json` |

## Phase 2: Mock CAP Lifecycle

The second milestone was proving the agent-commerce boundary in a reproducible local mock network.

Command:

```bash
PYTHONPATH=src .venv/bin/python examples/run_mock_cap_demo.py
```

Lifecycle events:

- `service_registered`
- `negotiation_created`
- `negotiation_accepted`
- `order_paid`
- `order_completed`

The mock lifecycle demonstrates that ProofMesh can sit behind a requester/provider boundary: a requester creates a negotiation, pays for an audit, and receives a structured verification report.

Saved evidence:

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`

Batch mock CAP cases:

| Case | Verified | Supported | Unsupported | Contradicted | Mock cost |
| --- | --- | ---: | ---: | ---: | ---: |
| supported | true | 2 | 0 | 0 | 0.25 CROO |
| unsupported | false | 1 | 1 | 0 | 0.25 CROO |
| contradicted | false | 0 | 0 | 2 | 0.25 CROO |

Saved batch evidence:

- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`

## Phase 3: CROO SDK And Staging Readiness

The live/staging layer was implemented without claiming settlement.

What is implemented:

- environment-backed CROO config
- readiness report generator
- live-ready dry-run audit
- Python CROO provider runner using `croo-sdk`
- CROO activity diagnostic script
- Agent Store listing metadata

Key files:

- `src/proofmesh/config.py`
- `src/proofmesh/live_adapter.py`
- `src/proofmesh/croo_provider.py`
- `examples/check_live_readiness.py`
- `examples/run_live_dry_run.py`
- `examples/run_croo_provider.py`
- `examples/check_croo_activity.py`
- `deployment/agent-store-listing.json`

Staging readiness was confirmed with:

- `PROOFMESH_MODE=staging`
- `PROOFMESH_PROVIDER_AGENT_ID=0xc38d5FE5125F5ce901768b26941Bac8758aCD46e`
- `CROO_API_KEY` present and redacted in saved artifacts

Saved Phase 3 evidence:

- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-readiness-report.md`
- `artifacts/phase3/live-dry-run-audit.json`
- `artifacts/phase3/live-dry-run-audit.md`
- `artifacts/phase3/croo-purchase-attempt.json`
- `artifacts/phase3/croo-purchase-attempt.md`

Important status: the CROO purchase/order flow appeared completable, but the wallet funding used for the purchase did not appear on the usable balance. Therefore no live/staging order receipt is attached, and live settlement is not claimed.

## Mini Benchmark

ProofMesh includes a deterministic synthetic benchmark for regression evidence.

Command:

```bash
PYTHONPATH=src .venv/bin/python examples/run_benchmark.py
```

Current result:

- 30 total claim-set cases
- 10 supported
- 10 unsupported
- 10 contradicted
- 30/30 correct on this synthetic regression set
- accuracy: 1.0

Saved benchmark artifacts:

- `artifacts/benchmark/proofmesh-mini-benchmark.json`
- `artifacts/benchmark/proofmesh-mini-benchmark.md`

Interpretation: this benchmark is useful for reproducibility and regression testing. It is not evidence of broad factual truth verification because the cases are synthetic and intentionally simple.

## Reproducibility

The main one-command regeneration path is:

```bash
python3 -m venv .venv
.venv/bin/pip install croo-sdk
PYTHONPATH=src .venv/bin/python examples/run_all_evidence.py
```

Convenience commands:

```bash
make test
make benchmark
make evidence
make readiness
```

Current validation:

- 22 unit tests pass
- deterministic local examples are saved
- mock CAP lifecycle logs are saved
- mini benchmark artifacts are saved
- Phase 3 readiness and dry-run artifacts are saved
- purchase attempt blocker is documented

## Business Model

ProofMesh can charge per audit. The current listing uses `0.25 CROO` per source coverage audit. Pricing can later scale by:

- number of claims
- number of sources
- contradiction-checking depth
- latency requirements
- domain-specific verifier plugins
- signed evidence bundles
- human escalation

The buyer is not only a human. The stronger use case is another agent that wants to improve its own deliverable before selling it onward.

## Why This Is Composable

ProofMesh is not tied to one vertical. The same service boundary can audit:

- research reports
- market intelligence summaries
- dataset summaries
- due diligence outputs
- generated compliance notes
- agent-generated documentation

The reusable unit is claim-level evidence checking, not a single task domain.

## Limitations

ProofMesh deliberately avoids overclaiming:

- local MVP output is not live CROO settlement
- mock CAP lifecycle is not live CROO settlement
- live-ready dry-run is not live CROO settlement
- the CROO purchase attempt is not live settlement because no order receipt was obtained
- lexical source coverage is not semantic truth verification
- confidence scores are transparent heuristics, not calibrated probabilities
- source quality is only as good as the evidence supplied by the requester
- high-stakes domains require domain-specific validation
- the mini benchmark is synthetic regression evidence, not a broad real-world benchmark

## Roadmap

Near-term:

- record a short demo video
- complete DoraHacks/BUIDL submission
- retry CROO purchase after wallet funding is visible
- attach a real staging/live order receipt if the purchase completes

Medium-term:

- add source retrieval adapters
- expand benchmark cases with paraphrases and ambiguous evidence
- compare ProofMesh against requester-agent self-checks
- add signed evidence bundles

Research direction:

- larger labeled benchmark
- calibrated confidence scoring
- domain-specific verifier plugins
- paper-style evaluation of agent-to-agent verification services

## Closing

ProofMesh demonstrates a concrete agent-commerce primitive: a requester agent can buy verification from another agent before delivering its own output. The project has local verifier evidence, mock CAP lifecycle evidence, CROO staging readiness, a Python CROO provider runner, a documented purchase attempt, and a reproducible mini benchmark.

The final live settlement receipt is intentionally not claimed. That discipline is part of the project: a verification agent should be held to the same standard it asks other agents to meet.
