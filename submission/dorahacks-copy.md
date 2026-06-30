# DoraHacks Submission Copy

## Project Name

ProofMesh

## One-Liner

A paid verification and provenance agent that other CROO CAP agents can hire before delivering generated outputs.

## Short Description

ProofMesh is a CAP-callable verification agent for the agent economy. Requester agents send generated reports, dataset summaries, or claim bundles to ProofMesh. ProofMesh audits claims against supplied sources, flags unsupported or contradicted statements, returns confidence scores and limitations, and delivers a structured evidence package through the CAP lifecycle.

## Problem

As agents begin selling outputs to humans and other agents, buyers need trust signals: which claims were checked, which sources support them, and whether the output overclaims. Verification should not be duplicated inside every agent. It should be a reusable paid service.

## Solution

ProofMesh turns verification into a composable agent service. A requester agent can hire ProofMesh as a dependency before delivering its own paid output. ProofMesh returns machine-readable audit results that can be included in the requester agent's final deliverable.

## Tracks

- Data & Verification Agents
- Research & Intelligence Agents

## Key Features

- claim-level source coverage audit
- contradiction flagging
- conservative artifact-level verification status
- structured JSON and markdown output
- mock CAP provider/requester lifecycle
- batch mock CAP evidence for supported, unsupported, and contradicted cases
- deterministic mini benchmark
- live/staging readiness checker and dry-run audit
- Python CROO provider runner using `croo-sdk`
- documented CROO purchase attempt blocked by wallet funding
- reproducible local tests and experiment logs

## Business Model

ProofMesh charges per audit. Pricing can scale by number of claims, number of sources, depth of contradiction checking, latency requirements, domain-specific verifier plugins, and signed evidence bundles.

## Current Status

Implemented:

- local verifier core
- CLI
- example request
- unit tests
- experiment log
- mock CAP lifecycle demo
- batch mock CAP summary
- mini benchmark: 30/30 deterministic synthetic cases
- live readiness report
- live-ready dry-run audit
- Python CROO provider runner
- purchase attempt artifact documenting the wallet-funding blocker

In progress:

- Agent Store live listing
- live/staging CROO order receipt after wallet funding appears on the usable purchase balance

## Repository

https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

## Demo Video

Pending recording. The script and runbook are ready:

- `submission/demo-script.md`
- `submission/demo-runbook.md`

Target length: under 5 minutes.

## Agent Store Listing

Metadata is prepared in `deployment/agent-store-listing.json`.

Intended service:

- Agent: `ProofMesh`
- Service ID: `proofmesh-source-coverage-audit`
- Service name: `Source Coverage Audit`
- Price: `0.25 CROO` per audit
- Require Fund Transfer: `false`
- Provider agent ID: `0xc38d5FE5125F5ce901768b26941Bac8758aCD46e`

Current status: live listing/order receipt is pending because the CROO wallet
funding used for the purchase did not appear on the usable purchase balance.
ProofMesh does not claim live settlement until a receipt is attached.

## Judging Evidence

- Final writeup: `writeup/kaggle-writeup.md`
- Evidence map: `submission/evidence-map.md`
- Architecture: `writeup/architecture.md`
- Mini benchmark: `artifacts/benchmark/proofmesh-mini-benchmark.md`
- Live readiness notes: `deployment/live-integration-notes.md`
