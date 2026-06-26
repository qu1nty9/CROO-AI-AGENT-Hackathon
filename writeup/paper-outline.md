# Paper Outline: Verification-as-a-Service for Agent Economies

Status: working outline.

## Tentative Title

Verification-as-a-Service for Agent Economies: Settlement-Linked Provenance in Composable A2A Workflows

## Abstract Draft

Autonomous agents increasingly produce research, data transformations, and operational decisions for downstream consumers. In paid agent marketplaces, output quality and provenance become market goods: agents must not only generate outputs, but also verify, cite, and audit them. We present ProofMesh, a composable verification agent that can be called by other agents through an agent commerce protocol. ProofMesh returns structured evidence reports linked to the job lifecycle and settlement metadata. We describe the architecture, schema, implementation, and evaluation plan for verification-as-a-service in agent economies.

## Research Questions

1. Can a verification agent improve trust signals in A2A workflows without being tightly coupled to the requester agent?
2. What evidence schema is sufficient for reusable verification across research and data tasks?
3. What are the latency and cost tradeoffs of adding a paid verification dependency?
4. How should settlement metadata be connected to provenance and audit outputs?

## Contributions

- A reusable architecture for a paid verification agent in a CAP-style marketplace.
- A structured evidence report schema for claim-level provenance.
- A reproducible mock CAP lifecycle for local evaluation.
- A plan for live integration and marketplace deployment.
- Initial case studies for research-output verification and optional domain-specific auditing.

## Related Work Areas

- agent marketplaces
- tool-using and multi-agent systems
- provenance and evidence tracking
- fact-checking and claim verification
- software supply-chain style attestations
- paid API and service composition

## Method

Build ProofMesh as a provider agent. A requester agent sends generated artifacts for verification. ProofMesh parses claims, checks provided sources, flags unsupported or contradictory claims, estimates confidence, and delivers a structured response through the CAP lifecycle.

## Evaluation Plan

Datasets and scenarios:

- synthetic research reports with known unsupported claims
- small curated source bundles
- optional domain-specific scenario from the MedShield reference

Metrics:

- unsupported-claim detection
- source coverage
- contradiction flag precision
- latency
- audit cost
- requester workflow overhead
- human agreement on confidence labels

Baselines:

- no verification
- monolithic agent self-check
- external verifier called outside CAP
- ProofMesh as CAP-composed verifier

## Limitations

- mock lifecycle is not equivalent to production settlement
- source retrieval quality may dominate verification quality
- confidence scores require calibration
- high-stakes domains require separate validation

## Publication Path

Short path:

- Kaggle writeup plus technical blog.

Medium path:

- arXiv preprint after MVP, mock evaluation, and one live or well-documented staging integration.

Stronger path:

- workshop submission on agents, trustworthy AI systems, or decentralized AI infrastructure after adding a benchmark and human evaluation.

