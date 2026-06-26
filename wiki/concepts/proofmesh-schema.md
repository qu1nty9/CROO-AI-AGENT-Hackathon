# Concept: ProofMesh Verification Schema

Current schema version: `proofmesh.verification.v1`

## Request

Required intent:

- identify the task
- describe the artifact being audited
- provide claims directly or provide artifact text
- provide sources used for source coverage checks
- declare the audit mode

Canonical request fields:

- `schema_version`: currently `proofmesh.verification.v1`
- `task_id`: caller-provided task identifier
- `artifact_type`: for example `research_report`, `dataset_summary`, or `claim_set`
- `artifact_text`: optional raw artifact text
- `claims`: optional list of claim objects
- `sources`: list of source objects
- `audit_mode`: currently `source_coverage`
- `max_latency_seconds`: optional requester preference
- `max_price_croo`: optional requester preference
- `cap_receipt`: optional CAP metadata supplied by wrapper code

At least one of `claims` or `artifact_text` must be non-empty.

## Claim Object

- `id`: stable claim id
- `text`: claim text
- `source_ids`: source ids to check first

## Source Object

- `id`: stable source id
- `title`: optional source title
- `url`: optional URL or local path
- `text`: source excerpt/content

## Response

Canonical response fields:

- `schema_version`
- `task_id`
- `artifact_type`
- `audit_mode`
- `is_verified`
- `overall_confidence`
- `source_coverage`
- `claim_audits`
- `limitations`
- `cap_receipt`
- `generated_at`

## Verification Rule

For Phase 1, `is_verified` is intentionally conservative:

- true only when at least one claim exists
- every claim must be `supported`
- no claim may be `contradicted`

This makes ProofMesh useful as an overclaim blocker in a judging demo.

## Current Audit Mode

`source_coverage` checks:

- lexical overlap between claim and source text
- requested source ids
- local negation mismatch as a contradiction marker

It does not claim semantic truth verification.

