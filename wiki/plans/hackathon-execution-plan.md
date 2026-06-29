# Hackathon Execution Plan

Date: 2026-06-26

## Objective

Build, document, and submit a strong CROO AI Agent Hackathon project that can also become a Kaggle writeup and a research-style article.

Working project: `ProofMesh`, a CAP-callable verification and provenance agent.

## Success Criteria

Hackathon success means:

- callable agent with request/response schema
- CAP lifecycle demonstrated in mock mode and, if possible, live mode
- open-source repo with license
- clear README and setup
- reproducible tests
- demo video under 5 minutes
- Agent Store listing
- DoraHacks BUIDL submission
- Kaggle writeup with architecture, evidence, limitations, and business model

Research success means:

- problem statement beyond the hackathon
- reproducible evaluation
- clear baselines
- honest limitations
- reusable schema or framework contribution
- enough evidence for an arXiv preprint or technical blog

## Phase 0: Repository And Knowledge Base

Status: started.

Tasks:

- create `AGENTS.md`
- create `wiki/` index, log, sources, concepts, and plan pages
- create `writeup/` drafts
- create `submission/` checklist
- add top-level `README.md`

## Phase 1: MVP Agent

Goal: one executable local ProofMesh agent.

Status: completed for local Kaggle writeup evidence.

Tasks:

- create Python package layout under `src/proofmesh/`
- define Pydantic schemas:
  - `VerificationRequest`
  - `ClaimAudit`
  - `EvidenceSource`
  - `VerificationResponse`
  - `CAPReceipt`
- implement deterministic audit core:
  - claim extraction from structured input
  - source presence checks
  - contradiction markers
  - confidence scoring placeholder with transparent formula
  - limitations field
- implement CLI:
  - `proofmesh audit examples/research_claim.json`
  - output JSON and markdown
- add unit tests for schema validation and scoring

Completed additions:

- runtime schema validation
- schema version `proofmesh.verification.v1`
- canonical supported, unsupported, and contradicted demo cases
- saved outputs under `artifacts/phase1/`
- 8 unit tests passing

## Phase 2: Mock CAP Lifecycle

Goal: prove A2A commerce flow locally.

Status: completed for mock evidence.

Tasks:

- adapt the mock server pattern from `reference/msagent1.ipynb`
- implement provider agent service
- implement requester script
- run scenario:
  - requester submits audit job
  - provider accepts
  - payment event fires
  - ProofMesh audits
  - structured deliverable is submitted
  - ledger entry is recorded
- save demo logs under `experiments/`

Completed additions:

- `src/proofmesh/cap_mock.py`
- `src/proofmesh/provider.py`
- `examples/run_mock_cap_demo.py`
- `examples/run_mock_cap_batch.py`
- `tests/test_cap_mock.py`
- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`
- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`
- experiment record for mock lifecycle

## Phase 3: Live CROO Integration

Goal: replace mock-only pieces with real CAP where possible.

Status: live-ready scaffold complete; live/staging transaction pending credentials and SDK confirmation.

Tasks:

- verify current CROO SDK methods against the installed `croo-sdk` package
- obtain SDK key and Agent Store credentials
- register service metadata
- map local schemas to SDK request/response fields
- run one live transaction or documented staging transaction
- record screenshots/logs/transaction IDs if allowed

Open dependency: current CROO SDK docs and credentials.

Completed additions:

- `src/proofmesh/config.py`
- `src/proofmesh/live_adapter.py`
- `deployment/agent-store-listing.json`
- `deployment/env.example`
- `deployment/live-integration-notes.md`
- `examples/check_live_readiness.py`
- `examples/run_live_dry_run.py`
- `tests/test_live_adapter.py`
- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-dry-run-audit.json`

Current blockers:

- wallet funding did not appear on the usable purchase balance during the purchase attempt
- no live/staging receipt yet

## Phase 4: Demo And Submission

Goal: make judging effortless.

Status: local submission package mostly complete; public repo, Agent Store listing, DoraHacks submission, and demo video still pending.

Artifacts:

- `README.md` with quickstart
- `LICENSE`
- `examples/`
- `tests/`
- `demo/` script
- 5-minute demo video
- Agent Store listing copy
- DoraHacks BUIDL copy
- Kaggle writeup

Completed additions:

- `LICENSE`
- submission-ready `README.md`
- `submission/evidence-map.md`
- `submission/demo-runbook.md`
- `examples/run_all_evidence.py`

Remaining external/publishing tasks:

- Agent Store live listing
- DoraHacks BUIDL
- recorded demo video
- published Kaggle writeup

Completed publishing task:

- public GitHub repository URL: https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

Demo structure:

1. show the problem: agents produce claims that need verification
2. show requester hiring ProofMesh
3. show CAP lifecycle and settlement
4. show audit output
5. show why it is composable and monetizable

## Phase 5: Kaggle Writeup

Goal: produce a public writeup that feels like a polished engineering case study.

Recommended sections:

- TL;DR
- Problem
- Why CAP matters
- Architecture
- Request/response schema
- Demo lifecycle
- Validation
- Business model
- Limitations
- Future work
- Reproducibility

## Phase 6: Paper Or arXiv Track

Goal: convert the project into a research-style artifact.

Possible title:

`Verification-as-a-Service for Agent Economies: Settlement-Linked Provenance in Composable A2A Workflows`

Needed evidence:

- benchmark of tasks with and without verification dependency
- latency and cost analysis
- source coverage and contradiction detection metrics
- confidence calibration or human review agreement
- ablation: monolithic agent vs CAP-composed verifier

## Risk Register

High risks:

- live CROO SDK/API is unavailable or undocumented
- demo overclaims on-chain settlement while only using mock mode
- verification scores look arbitrary
- project is too broad

Mitigations:

- clearly label mock vs live
- keep MVP narrow: source-backed claim audit
- make scoring transparent and conservative
- record reproducible logs
- prioritize one excellent demo over many weak features
