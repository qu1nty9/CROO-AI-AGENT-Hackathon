# Kaggle Writeup Asset Plan

## Required Screenshots Or Figures

- [ ] Architecture diagram: requester agent -> CAP lifecycle -> ProofMesh -> verification response
- [x] Architecture diagram draft in `writeup/architecture.md`
- [ ] CLI run screenshot showing `is_verified: false`
- [ ] Unit test screenshot or copied terminal output
- [ ] Mock CAP lifecycle log screenshot
- [ ] Example JSON response snippet
- [ ] Agent Store listing screenshot, if available
- [ ] DoraHacks submission screenshot, if useful

## Tables

### Evidence Status Table

| Claim | Evidence | Status |
| --- | --- | --- |
| ProofMesh audits source-backed claims | local CLI + tests + `artifacts/demo-audit.json` | implemented |
| ProofMesh flags overclaims | `artifacts/demo-audit.md` | implemented |
| ProofMesh handles supported/unsupported/contradicted cases | `artifacts/phase1/*.json` | implemented |
| ProofMesh runs through CAP lifecycle | `artifacts/phase2/mock-cap-demo-log.json` | implemented as mock |
| ProofMesh reports batch cost/latency | `artifacts/phase2/mock-cap-batch-summary.json` | implemented as mock |
| ProofMesh is live-ready | `artifacts/phase3/live-readiness-report.json` | scaffold implemented |
| ProofMesh settles on live CROO | live/staging receipt | pending |

### Demo Cases Table

| Case | Expected Result | Purpose |
| --- | --- | --- |
| supported artifact | verified | happy path |
| unsupported claim | not verified | missing evidence |
| contradicted claim | not verified | overclaim prevention |

### Business Model Table

| Tier | Buyer | Output | Pricing Logic |
| --- | --- | --- | --- |
| Basic | research agent | source coverage | per claim bundle |
| Pro | data/report agent | contradiction scan | per claim + source |
| Enterprise | regulated workflow | signed evidence bundle | premium |

## Final Writeup Checklist

- [ ] no unverified live settlement claims
- [ ] clear distinction between local, mock, staging, and live
- [ ] all commands reproducible
- [x] one-command local evidence regeneration
- [ ] demo output matches repository state
- [ ] at least one visual diagram
- [ ] at least one concrete failure case
- [ ] tracks named explicitly
- [ ] limitations section included
- [ ] business model explained in one paragraph
