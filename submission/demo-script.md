# ProofMesh Demo Script

Target length: 4-5 minutes.

## 0:00-0:30 Problem

Agents are starting to sell outputs: research, reports, dataset summaries, code, and decisions. The weak point is trust. A buyer needs to know which claims were checked, what sources support them, and whether the delivering agent overclaimed.

ProofMesh solves this by making verification a paid callable service for other agents.

## 0:30-1:00 Product

ProofMesh is a CROO CAP provider agent. A requester agent can hire it before delivering its own report to a buyer. ProofMesh audits the artifact claim by claim and returns a structured evidence package.

Tracks:

- Data & Verification Agents
- Research & Intelligence Agents

## 1:00-1:45 Local Verifier

Show:

```bash
PYTHONPATH=src python3 -m proofmesh.cli audit examples/research_claim.json --format markdown
```

Explain the example:

- claim 1 is supported by the CROO brief
- claim 2 is supported by the submission requirements
- claim 3 overclaims that live settlement already happened

ProofMesh marks the full artifact as not verified because one claim is contradicted.

## 1:45-2:45 CAP Lifecycle

Show the mock lifecycle:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_demo.py
```

1. requester submits `VerificationRequest`
2. provider receives negotiation
3. provider accepts
4. payment event occurs
5. ProofMesh audits the artifact
6. provider delivers `VerificationResponse`
7. requester receives evidence package and receipt

Important line:

This demo labels mock and live behavior separately. The verifier is designed to prevent overclaiming, so the project itself should not overclaim settlement.

Show saved evidence:

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`
- `artifacts/phase2/mock-cap-batch-summary.md`

Optional batch proof:

```bash
PYTHONPATH=src python3 examples/run_mock_cap_batch.py
```

## 2:45-3:30 Output

Show the response fields:

- `is_verified`
- `overall_confidence`
- `source_coverage`
- `claim_audits`
- `contradiction_sources`
- `limitations`
- `cap_receipt`

Explain that downstream agents can consume this JSON automatically.

## 3:30-4:15 Why It Can Earn

Verification is a natural paid dependency:

- basic audit per claim bundle
- deeper contradiction scan
- premium domain-specific plugins
- signed evidence bundles

Requester agents improve their own deliverables by hiring ProofMesh before delivery.

## 4:15-5:00 Close

Show live readiness:

```bash
PYTHONPATH=src python3 examples/check_live_readiness.py
```

Say clearly:

- local verifier is implemented
- mock CAP lifecycle is implemented
- live-ready scaffold is implemented
- live CROO order is pending SDK key and current SDK/API confirmation

ProofMesh demonstrates the CROO thesis: agents do not only generate outputs; they can hire each other for reusable paid capabilities. Verification is one of the most reusable capabilities in an agent marketplace.
