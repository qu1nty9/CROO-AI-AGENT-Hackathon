# ProofMesh Judging Rubric

This page tracks what a judge should be able to verify quickly.

## 1. Does It Satisfy The Required Submission Criteria?

- [ ] Agent Store listing exists
  - Metadata is prepared; live listing/order receipt is pending.
- [x] CAP integration exists
- [x] Agent is callable
- [x] Settlement is shown or clearly documented
  - Mock CAP settlement is shown.
  - Live CROO settlement is explicitly not claimed.
- [x] GitHub repo is public
- [x] Permissive license exists
- [x] README explains setup
- [x] SDK methods are documented
- [ ] Demo video is under 5 minutes
  - Script/runbook are ready; video still needs to be recorded.
- [ ] DoraHacks BUIDL is complete
  - Copy is ready; final submission still needs to be filed.

## 2. Is The Agent Actually Composable?

Strong evidence:

- requester script calls ProofMesh as a separate provider
- request/response schemas are stable
- output is machine-readable JSON
- requester can use ProofMesh output in its own final deliverable

Weak evidence:

- only a standalone notebook
- no provider/requester boundary
- no structured output

## 3. Is CAP Central Or Decorative?

Strong evidence:

- demo shows negotiation, payment, delivery, and receipt
- CAP lifecycle changes the product story
- business model depends on paid A2A calls

Weak evidence:

- CAP mentioned only in README
- local function call with no A2A flow

## 4. Is The Product Useful?

Strong evidence:

- clear buyer: other agents that sell outputs
- clear failure mode: unsupported or contradicted claims
- clear value: evidence before delivery

Weak evidence:

- generic chatbot
- no concrete buyer
- no measurable output quality

## 5. Is The Work Reproducible?

Strong evidence:

- one-command tests
- example input/output
- saved experiment logs
- clear mock vs live distinction

Weak evidence:

- screenshots only
- private API keys required for all behavior
- unverified claims about settlement

## 6. What Could Make This Stand Out?

- live/staging CAP receipt
- clean 5-minute demo
- benchmark table with supported/unsupported/contradicted cases
- concise architecture diagram
- polished README
- honest limitations
