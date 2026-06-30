# CROO Hackathon Submission Checklist

Status: pre-demo submission package ready. Remaining items are external publishing
or recording steps.

## Required By Brief

- [ ] Agent live-listed on CROO Agent Store
  - Metadata is prepared in `deployment/agent-store-listing.json`.
  - Live listing/order receipt is still pending because the wallet funding did
    not appear on the usable purchase balance.
- [x] CAP integration implemented
  - Mock CAP lifecycle is implemented and reproducible.
  - CROO SDK/staging provider scaffold is implemented.
- [x] Agent is callable by other agents in mock CAP
- [x] Settlement flow clearly documented as mock CAP
- [x] Public GitHub repository
  - https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon
- [x] Permissive license: MIT or Apache 2.0
- [x] README with setup instructions
- [x] SDK methods used documented
- [x] Integration notes documented
- [ ] Demo video under 5 minutes
  - Script and runbook are ready in `submission/demo-script.md` and
    `submission/demo-runbook.md`.
- [ ] DoraHacks BUIDL submitted
  - Copy is ready in `submission/dorahacks-copy.md`.

## Recommended Extra Evidence

- [x] Local integration test logs
- [x] Example request JSON
- [x] Example response JSON
- [x] Architecture diagram
- [x] Pricing model
- [x] Known limitations
- [ ] Screenshots or transaction proof from live/staging CAP
  - Purchase attempt is documented, but no order receipt exists yet.
- [x] Kaggle writeup ready locally
  - `writeup/kaggle-writeup.md`
- [ ] Kaggle writeup published
  - Final local draft is ready for publication/paste.
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
- Mini benchmark JSON: `artifacts/benchmark/proofmesh-mini-benchmark.json`
- Mini benchmark Markdown: `artifacts/benchmark/proofmesh-mini-benchmark.md`
- Live readiness report: `artifacts/phase3/live-readiness-report.json`
- Live dry-run audit: `artifacts/phase3/live-dry-run-audit.json`
- CROO purchase attempt: `artifacts/phase3/croo-purchase-attempt.json`
- Kaggle writeup: `writeup/kaggle-writeup.md`
- Tests: `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests`
- All evidence: `PYTHONPATH=src .venv/bin/python examples/run_all_evidence.py`

## Current Live Blockers

- wallet funding did not appear on the usable purchase balance
- no live/staging order receipt yet

## Ready Before Demo Recording

- Repository is public and pushed: https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon
- Final Kaggle writeup is ready locally: `writeup/kaggle-writeup.md`
- Evidence map is ready: `submission/evidence-map.md`
- DoraHacks submission copy is ready: `submission/dorahacks-copy.md`
- Demo script and runbook are ready:
  - `submission/demo-script.md`
  - `submission/demo-runbook.md`
- Agent Store listing metadata is ready: `deployment/agent-store-listing.json`

## Manual/External Remaining

- Record and upload the demo video.
- Paste the final writeup into Kaggle/DoraHacks as required.
- Submit the DoraHacks BUIDL.
- Retry CROO purchase/listing once wallet funding appears on the usable balance.
