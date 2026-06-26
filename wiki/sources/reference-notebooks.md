# Source Note: Reference Notebooks

Date ingested: 2026-06-26

## Files Reviewed

- `reference/msagent1.ipynb`
- `reference/croo-ai-agent-1.ipynb`

## `msagent1.ipynb`

This notebook proposes `MedShield`, a composable clinical triage verifier and safety auditor agent. It creates files for:

- requirements
- config
- clinical verifier logic
- CROO websocket agent client
- mock server
- integration test runner

Strengths:

- concrete service with a clear buyer: triage or diagnosis agents
- clear request and response schema
- strong fit for Data & Verification Agents
- end-to-end mock lifecycle: negotiation, payment, delivery
- stronger product narrative than a generic demo

Risks:

- clinical claims need careful evidence and limitations
- demographic bias scoring appears heuristic and would need validation before publication
- live CROO SDK/API behavior must be verified
- health/safety framing may create a higher burden of proof for judges and readers

## `croo-ai-agent-1.ipynb`

This notebook sketches `AgentMesh`, a multi-agent research pipeline with a Fractional Routing Protocol. It decomposes a query, routes work to search, synthesis, fact-check, and report agents, and simulates CAP registration and settlement.

Strengths:

- directly demonstrates A2A composability
- good narrative for Research & Intelligence Agents
- has publication potential if turned into an evaluated architecture
- can be adapted into a provenance and verification product

Risks:

- CAP behavior is simulated rather than integrated
- some URLs and source claims are placeholders in demo mode
- less product-specific than MedShield unless narrowed
- needs rigorous evaluation to avoid looking like a wrapper around LLM calls

## Recommended Synthesis

Use the broader AgentMesh idea as the architecture, but narrow the product to verification/provenance. The recommended project is `ProofMesh`: a CAP-callable verification agent that audits outputs from other agents and returns an evidence package.

MedShield can become one optional demo scenario, not the entire project, unless we decide to accept the higher validation burden of a clinical product.

