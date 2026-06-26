# CROO Hackathon Submission Checklist

Status: working checklist.

## Required By Brief

- [ ] Agent listed on CROO Agent Store
- [ ] CAP integration implemented
- [x] Agent is callable by other agents in mock CAP
- [x] Settlement flow clearly documented as mock CAP
- [ ] Public GitHub repository
- [x] Permissive license: MIT or Apache 2.0
- [x] README with setup instructions
- [ ] SDK methods used documented
- [ ] Integration notes documented
- [ ] Demo video under 5 minutes
- [ ] DoraHacks BUIDL submitted

## Recommended Extra Evidence

- [x] Local integration test logs
- [x] Example request JSON
- [x] Example response JSON
- [ ] Architecture diagram
- [x] Pricing model
- [x] Known limitations
- [ ] Screenshots or transaction proof from live/staging CAP
- [ ] Kaggle writeup published
  - Current draft: `writeup/kaggle-writeup.md`
- [x] Evidence map
  - `submission/evidence-map.md`
- [x] Demo runbook
  - `submission/demo-runbook.md`

## Demo Video Script

1. State the problem: agents need paid verification dependencies.
2. Show ProofMesh listed or configured as a service.
3. Submit a verification request from a requester agent.
4. Show negotiation and payment lifecycle.
5. Show ProofMesh audit output.
6. Show completion receipt and explain business model.

## Current Local Evidence

- Request: `examples/research_claim.json`
- JSON output: `artifacts/demo-audit.json`
- Markdown output: `artifacts/demo-audit.md`
- Phase 1 supported case: `artifacts/phase1/supported-artifact.json`
- Phase 1 unsupported case: `artifacts/phase1/unsupported-claim.json`
- Phase 1 contradicted case: `artifacts/phase1/contradicted-claim.json`
- Mock CAP lifecycle JSON: `artifacts/phase2/mock-cap-demo-log.json`
- Mock CAP lifecycle Markdown: `artifacts/phase2/mock-cap-demo-log.md`
- Mock CAP batch JSON: `artifacts/phase2/mock-cap-batch-summary.json`
- Mock CAP batch Markdown: `artifacts/phase2/mock-cap-batch-summary.md`
- Live readiness report: `artifacts/phase3/live-readiness-report.json`
- Live dry-run audit: `artifacts/phase3/live-dry-run-audit.json`
- Tests: `PYTHONPATH=src python3 -m unittest discover -s tests`
- All evidence: `PYTHONPATH=src python3 examples/run_all_evidence.py`

## Current Live Blockers

- `CROO_SDK_KEY` is missing
- current CROO Python SDK package/import name is not confirmed locally
- no live/staging order receipt yet
