# ProofMesh: A Paid Verification Agent for Trustworthy CAP Workflows

Status: Kaggle writeup draft.

Repository: https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

## TL;DR

ProofMesh is a paid, callable verification and provenance agent for CROO CAP workflows. A requester agent can hire ProofMesh before delivering a report, dataset summary, or generated artifact to its own customer. ProofMesh audits the artifact claim by claim, checks source coverage, flags contradictions, returns confidence scores and limitations, and attaches CAP lifecycle metadata to the deliverable.

The core idea is simple: in an agent marketplace, verification should itself be a composable paid service.

Tracks:

- Data & Verification Agents
- Research & Intelligence Agents

## What We Built

ProofMesh is designed as a provider agent that can be called by other agents. Its first service is `source_coverage_audit`: a structured audit of claims against supplied sources.

Current implemented components:

- dependency-free local verification core
- command-line audit interface
- versioned request/response schema: `proofmesh.verification.v1`
- mock CAP requester/provider lifecycle
- example request JSON
- markdown and JSON output modes
- unit tests for supported, unsupported, contradicted, and generated claims
- saved demo outputs in `artifacts/demo-audit.json` and `artifacts/demo-audit.md`
- three canonical Phase 1 demo cases with saved outputs
- saved mock CAP lifecycle evidence in `artifacts/phase2/`
- batch mock CAP summary across supported, unsupported, and contradicted cases
- architecture draft in `writeup/architecture.md`
- live/staging readiness adapter and dry-run artifacts
- one-command evidence regeneration via `examples/run_all_evidence.py`
- submission evidence map and demo runbook
- experiment log showing that ProofMesh blocks an overclaim about live settlement
- LLM Wiki style project knowledge base for reproducibility and writeup continuity

Planned submission components:

- Agent Store listing and DoraHacks BUIDL metadata
- live/staging CROO transaction if credentials and current SDK documentation are available

## Why This Matters

Most agent demos focus on generation: research summaries, code, analytics, reports, decisions. But paid agent commerce creates a second problem: buyers and downstream agents need a reason to trust what they receive.

If every agent implements its own verification logic, verification quality is inconsistent and duplicated. If verification becomes a callable CAP service, any agent can buy the same quality-control dependency before delivering its own output.

ProofMesh turns verification into a marketplace primitive:

- reusable by many requester agents
- priced per audit
- structured enough for downstream automation
- auditable through evidence and settlement metadata
- honest about uncertainty and limitations

## Why CAP Is Essential

Without CAP, ProofMesh is just a local checker or API. With CAP, ProofMesh becomes an economic dependency in an A2A workflow.

The desired lifecycle:

1. A requester agent generates an output for a buyer.
2. Before delivery, it sends a verification job to ProofMesh.
3. ProofMesh accepts the job through CAP.
4. The requester pays for the service.
5. ProofMesh performs the audit.
6. ProofMesh delivers a structured evidence report.
7. The requester includes the audit result in its final deliverable.

This is the hackathon thesis in miniature: agents can discover, hire, pay, and compose other agents as real services.

Current evidence: the repository includes a local mock CAP lifecycle with service registration, negotiation, acceptance, payment event, audit delivery, ledger entries, and saved logs.

Phase 3 status: ProofMesh is live-ready but not live-submitted. The repository includes environment config, service listing metadata, readiness checks, and a dry-run audit with `cap_receipt.mode = live_ready_dry_run`.

## Architecture

```text
Requester Agent
  |
  | VerificationRequest
  v
CROO CAP lifecycle
  |  negotiation -> payment -> delivery
  v
ProofMesh Provider Agent
  |
  | claim extraction / source coverage / contradiction checks
  v
VerificationResponse
  |
  | evidence package + confidence + limitations + CAP receipt
  v
Requester final deliverable
```

ProofMesh separates three concerns:

- `audit core`: deterministic verification logic and scoring
- `agent wrapper`: CAP negotiation, order handling, and delivery
- `evidence output`: structured response for humans and downstream agents

## Request Schema

The request is intentionally explicit. The requester can send claims directly or send artifact text that ProofMesh splits into auditable claims.

```json
{
  "task_id": "demo-research-001",
  "artifact_type": "research_report",
  "artifact_text": "CAP lets agents discover, hire, and pay other agents on-chain.",
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

## Response Schema

ProofMesh returns a structured response:

```json
{
  "task_id": "demo-research-001",
  "artifact_type": "research_report",
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

The important behavior is conservative verification: one contradicted or unsupported claim prevents the entire artifact from being marked fully verified.

Phase 1 schema version: `proofmesh.verification.v1`.

## Demo Scenario

The demo scenario is a research-agent handoff across a mock CAP lifecycle.

There are two related demo layers:

- the local CLI demo contains two source-backed claims and one overclaim about live settlement
- the mock CAP lifecycle demo uses a stricter request with two overclaims about live CROO behavior

ProofMesh marks both artifacts as not verified. This is exactly the product behavior we want: ProofMesh should help other agents avoid publishing or selling overstated claims.

The Phase 2 mock CAP demo shows:

- requester: `cap://research-requester.local`
- provider: `cap://proofmesh-provider.local`
- service: `proofmesh-source-coverage-audit`
- price: `0.25 CROO`
- lifecycle: service registration -> negotiation -> acceptance -> payment -> delivery
- delivered audit: `is_verified: false`
- delivered audit summary: `claims_contradicted: 2`

Saved evidence:

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`
- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`
- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/live-dry-run-audit.json`

## Current Reproducible Run

Run the local verifier:

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/research_claim.json --format markdown
```

Regenerate all local evidence:

```bash
PYTHONPATH=src .venv/bin/python examples/run_all_evidence.py
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Current result:

- 16 unit tests pass
- example audit returns `is_verified: false`
- the live-settlement overclaim is flagged as contradicted
- saved outputs:
  - `artifacts/demo-audit.json`
  - `artifacts/demo-audit.md`

Phase 1 canonical cases:

| Case | Expected result | Saved output |
| --- | --- | --- |
| Supported artifact | `is_verified: true` | `artifacts/phase1/supported-artifact.json` |
| Unsupported claim | `is_verified: false` | `artifacts/phase1/unsupported-claim.json` |
| Contradicted claim | `is_verified: false` | `artifacts/phase1/contradicted-claim.json` |

Run the mock CAP lifecycle:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_demo.py
```

Expected lifecycle events:

- `service_registered`
- `negotiation_created`
- `negotiation_accepted`
- `order_paid`
- `order_completed`

Run all canonical cases through mock CAP:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_batch.py
```

Batch summary:

| Case | Verified | Supported | Unsupported | Contradicted | Mock cost |
| --- | --- | ---: | ---: | ---: | ---: |
| supported | true | 2 | 0 | 0 | 0.25 CROO |
| unsupported | false | 1 | 1 | 0 | 0.25 CROO |
| contradicted | false | 0 | 0 | 2 | 0.25 CROO |

Check live/staging readiness:

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
```

Current live readiness:

- API URL configured: `https://api.croo.network`
- WS URL configured: `wss://api.croo.network/ws`
- service metadata ready
- CROO SDK confirmed as `croo-sdk`, importing module `croo`
- staging readiness artifact is `Ready: true` with redacted `CROO_API_KEY`
- blocked by missing live/staging order receipt

## Validation

Current validation:

- deterministic unit tests
- fixed example input
- three canonical demo cases
- mock requester/provider lifecycle test
- saved mock CAP lifecycle log
- batch cost/latency summary across canonical cases
- live-ready config/readiness dry-run
- reproducible local command
- experiment record in `experiments/`
- evidence map in `submission/evidence-map.md`
- demo runbook in `submission/demo-runbook.md`

Next validation before final submission:

- Agent Store listing evidence
- live/staging CROO integration once SDK key and current SDK methods are available

Ideal validation:

- small benchmark of 30-50 synthetic claim sets
- human-readable expected labels
- precision/recall for unsupported and contradicted claims
- comparison with a requester agent self-check

## Business Model

ProofMesh can charge per audit:

- basic source coverage audit: low cost, fast response
- deeper contradiction scan: higher cost, more sources
- domain-specific verifier plugins: premium pricing
- signed evidence bundle or human escalation: enterprise tier

The buyer is not only a human. The more important buyer is another agent that wants to improve its own deliverable before selling it onward.

## Why This Is Composable

ProofMesh is not tied to one vertical. It can audit:

- research reports
- market intelligence summaries
- dataset summaries
- due-diligence outputs
- generated compliance notes
- agent-generated documentation

The same interface works because the service boundary is claim-level verification, not one specific task domain.

## Limitations

Current limitations:

- local MVP is not live CROO settlement
- mock CAP lifecycle is not live CROO settlement
- live-ready dry-run is not live CROO settlement
- lexical source coverage is not semantic truth verification
- confidence scores are transparent heuristics, not calibrated probabilities
- source quality is only as good as the provided evidence
- high-stakes domains require domain-specific validation

Submission rule: the final demo must clearly label mock, staging, and live behavior. Overclaiming settlement would undermine the whole project.

## Roadmap

Short-term:

- convert architecture draft into final visual
- produce demo video
- prepare Agent Store listing copy

Medium-term:

- integrate current CROO SDK
- attach live/staging CAP receipt
- add source retrieval adapters
- add benchmark cases and metrics

Long-term:

- calibrated confidence scoring
- signed evidence bundles
- domain-specific verifier plugins
- publication-quality evaluation

## Reproducibility

The repository includes:

- `src/proofmesh/` for the verifier
- `src/proofmesh/cap_mock.py` for the mock CAP network
- `src/proofmesh/provider.py` for the ProofMesh provider wrapper
- `examples/run_mock_cap_demo.py` for the requester/provider lifecycle demo
- `examples/run_mock_cap_batch.py` for batch mock CAP evidence
- `examples/check_live_readiness.py` for Phase 3 readiness
- `examples/run_live_dry_run.py` for live-ready dry-run audit
- `examples/run_all_evidence.py` for one-command local verification
- `examples/` for input requests
- `artifacts/` for saved demo outputs
- `tests/` for unit tests
- `experiments/` for run records
- `wiki/` for maintained project knowledge
- `submission/` for judging assets

## Closing

ProofMesh is a small but concrete example of agent commerce: a requester agent can buy trust signals from another agent. That is the real product surface. CAP is not just payment plumbing here; it is what makes verification reusable, priced, and composable across the agent economy.
