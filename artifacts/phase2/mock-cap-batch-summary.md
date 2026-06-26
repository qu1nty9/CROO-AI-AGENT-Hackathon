# ProofMesh Mock CAP Batch Summary

- Cases: `3`
- Total mock cost: `0.75 CROO`
- Average elapsed: `0.299 ms`
- Max elapsed: `0.457 ms`

## Cases

| Case | Verified | Supported | Unsupported | Contradicted | Cost | Elapsed |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| supported | True | 2 | 0 | 0 | 0.25 CROO | 0.457 ms |
| unsupported | False | 1 | 1 | 0 | 0.25 CROO | 0.191 ms |
| contradicted | False | 0 | 0 | 2 | 0.25 CROO | 0.249 ms |

## Lifecycle Events

- `supported`: service_registered, negotiation_created, negotiation_accepted, order_paid, order_completed
- `unsupported`: service_registered, negotiation_created, negotiation_accepted, order_paid, order_completed
- `contradicted`: service_registered, negotiation_created, negotiation_accepted, order_paid, order_completed

## Limitation

Mock CAP batch evidence only; not live CROO settlement.
