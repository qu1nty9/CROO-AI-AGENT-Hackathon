# DoraHacks Submission Copy Draft

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
- live/staging readiness checker and dry-run audit
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
- live readiness report
- live-ready dry-run audit

In progress:

- Agent Store metadata
- live/staging CROO transaction, depending on credentials and current SDK access

## Repository

https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon

## Demo Video

TBD

## Agent Store Listing

TBD
