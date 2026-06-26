# Concept: Project Strategy

## Recommended Direction

Build `ProofMesh`: a paid verification and provenance agent for CAP.

Input:

- claim, report, dataset summary, generated output, or URL bundle
- optional source list
- desired audit mode
- maximum cost and latency preferences

Output:

- structured evidence report
- claim table
- source provenance
- contradiction flags
- confidence score
- limitations
- CAP job and settlement metadata

## Why This Is A Strong Hackathon Bet

ProofMesh satisfies the core hackathon thesis: agents should be able to hire other agents as paid dependencies. Verification is a natural dependency because many agent workflows need trust, quality control, and source-backed delivery.

It also fits two tracks:

- Data & Verification Agents: output checks, provenance, consistency, auditability
- Research & Intelligence Agents: source-backed synthesis and fact-checking

## Why Not Start With A Pure Medical Agent

The MedShield reference has a strong concrete demo, but clinical triage safety claims are high-stakes. Without validated clinical datasets, medical references, and careful limitations, the project risks looking overclaimed.

A domain-neutral verification agent is safer and more broadly composable. A medical triage audit can still be a demonstration case if framed as a synthetic safety-audit example, not a clinical device.

## Judging Story

The clean story:

1. In an agent economy, output quality and provenance become paid services.
2. ProofMesh is a reusable verification dependency for other agents.
3. CAP turns verification into a callable, priced, settled microservice.
4. The demo proves the lifecycle with reproducible logs.
5. The writeup shows why this creates a business model, not just a chatbot.

## Publication Story

The research angle:

`Composable paid verification agents for trustworthy agent economies`.

Possible contribution:

- architecture for verification-as-a-service in A2A marketplaces
- schema for evidence reports and settlement-linked provenance
- evaluation of latency, cost, confidence calibration, and source coverage
- case studies comparing monolithic agents vs agents with verification dependencies

