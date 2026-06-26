# CROO AI Agent Hackathon Workspace

This workspace follows a lightweight LLM Wiki pattern for a Kaggle/CROO hackathon project.

## Working Principle

There are three layers:

1. `docs/` and `reference/` are raw sources. Treat them as immutable input material.
2. `wiki/` is the maintained knowledge layer. Update it when new sources, decisions, experiments, or writeups are added.
3. `src/`, `tests/`, `writeup/`, and `submission/` are deliverable layers for the agent, reproducibility, and public submission assets.

When a new source is analyzed, add or update:

- `wiki/index.md`
- `wiki/log.md`
- one relevant source note under `wiki/sources/`
- any concept, decision, or plan page that the source changes

## Project Direction

Working title: `ProofMesh`.

Core idea: a paid, callable verification and provenance agent for the CROO Agent Protocol. Other agents can hire it to audit a claim, report, dataset, or generated output. The agent returns a structured evidence report with source provenance, contradiction checks, confidence scoring, cost/latency metadata, and CAP settlement records.

Primary tracks:

- Data & Verification Agents
- Research & Intelligence Agents

Optional secondary demo:

- A domain vertical such as clinical triage audit from `reference/msagent1.ipynb`, only if claims are carefully scoped and evidence-backed.

## Evidence Rules

- Do not invent CROO SDK behavior. Separate mock CAP simulation from live CAP integration.
- Do not fabricate external sources. If sources are unavailable, mark claims as assumptions or placeholders.
- Keep judging-facing claims verifiable from code, logs, demo, or public links.
- For any medical or safety-related demo, avoid clinical deployment claims unless supported by validated references and clear limitations.

## Writeup Rules

Public-facing materials should be in English by default:

- `README.md`
- `writeup/kaggle-writeup.md`
- `submission/checklist.md`
- demo script and paper outline

Internal planning may be bilingual, but keep filenames ASCII and stable.

## Experiment Rules

Each meaningful experiment should record:

- date
- goal
- input scenario
- agent configuration
- CAP mode: mock or live
- output artifact path
- success/failure result
- judging relevance

Prefer reproducible scripts over notebook-only work once the first MVP is selected.

