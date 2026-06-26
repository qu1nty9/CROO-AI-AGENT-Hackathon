# Source Note: LLM Wiki Pattern

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Date ingested: 2026-06-26

## Core Pattern

The linked gist describes a workflow where an LLM maintains a persistent markdown wiki instead of repeatedly re-reading raw documents from scratch. Raw sources remain unchanged. The wiki becomes a structured, interlinked, maintained layer containing summaries, concepts, contradictions, decisions, and synthesis pages.

## Useful Adaptation For This Hackathon

For this workspace, the pattern maps cleanly to:

- `docs/` and `reference/` as raw sources
- `wiki/` as the maintained knowledge base
- `wiki/index.md` as the navigation layer
- `wiki/log.md` as an append-only project history
- `writeup/` as public narrative output
- future `src/`, `tests/`, and `experiments/` as reproducible build artifacts

## Operational Rule

Whenever a source, implementation result, or decision changes the project, update the wiki. The goal is to make each future session start from accumulated project knowledge rather than rediscovering context.

## Why It Matters Here

The hackathon has multiple deliverables: working agent, demo, README, marketplace listing, DoraHacks submission, Kaggle writeup, and possibly a research article. A maintained wiki prevents these assets from diverging and provides material for high-quality public writing.

