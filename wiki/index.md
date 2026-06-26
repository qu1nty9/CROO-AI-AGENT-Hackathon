# ProofMesh Wiki Index

Last updated: 2026-06-26

## Overview

This wiki maintains the working knowledge base for the CROO AI Agent Hackathon project. It is intended to compound context across planning, implementation, experiments, Kaggle writeup work, and possible publication.

## Source Notes

- [CROO Hackathon Brief](sources/croo-hackathon-brief.md) - extracted challenge requirements and submission constraints from the local `.docx` brief.
- [LLM Wiki Pattern](sources/karpathy-llm-wiki.md) - operating model adapted from the linked gist.
- [Reference Notebooks](sources/reference-notebooks.md) - review of the two notebooks currently in `reference/`.
- [CROO Public Agent Store](sources/croo-agent-store-public.md) - public Agent Store surface and remaining SDK gaps.

## Concept Pages

- [CAP Agent Commerce](concepts/cap-agent-commerce.md) - the local understanding of CROO/CAP from the brief.
- [Project Strategy](concepts/project-strategy.md) - recommended project direction and tradeoffs.
- [ProofMesh Schema](concepts/proofmesh-schema.md) - request/response schema and Phase 1 verification rule.
- [Mock CAP Lifecycle](concepts/mock-cap-lifecycle.md) - local requester/provider/payment/delivery evidence.
- [Live CROO Readiness](concepts/live-croo-readiness.md) - live/staging adapter status and blockers.

## Plans

- [Hackathon Execution Plan](plans/hackathon-execution-plan.md) - full build, submission, writeup, and publication plan.

## Public Drafts

- [Kaggle Writeup Draft](../writeup/kaggle-writeup.md)
- [Paper Outline](../writeup/paper-outline.md)
- [Submission Checklist](../submission/checklist.md)
- [Evidence Map](../submission/evidence-map.md)
- [Demo Runbook](../submission/demo-runbook.md)

## Current Decision

The recommended primary project is `ProofMesh`: a paid verification/provenance agent that other agents can call through CAP. This is more broadly applicable and easier to validate than a high-stakes clinical-only agent, while still allowing a clinical audit as an optional vertical demo.
