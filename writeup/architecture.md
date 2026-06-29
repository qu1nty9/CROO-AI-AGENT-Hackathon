# ProofMesh Architecture Draft

This page provides diagrams and text that can be reused in the Kaggle writeup.

## End-to-End Evidence Topology

```mermaid
flowchart LR
    subgraph "Requester Side"
        R["Requester Agent"]
        Req["Verification Request<br/>claims + sources"]
    end

    subgraph "ProofMesh"
        P["Provider Boundary"]
        A["Audit Core"]
        S["Schema Validation"]
        B["Benchmark / Regression Cases"]
    end

    subgraph "CROO / CAP Layer"
        M["Mock CAP Lifecycle"]
        L["CROO SDK Provider Runner"]
        W["Wallet / Funding Flow"]
    end

    subgraph "Evidence Package"
        O["Verification Report"]
        E1["Phase 1 Artifacts"]
        E2["Phase 2 Mock CAP Logs"]
        E3["Phase 3 Readiness + Purchase Attempt"]
        EB["Mini Benchmark Summary"]
    end

    R --> Req --> P
    P --> S --> A --> O
    A --> B --> EB
    P --> M --> E2
    P --> L --> W --> E3
    O --> E1
```

## Mock CAP Lifecycle

```mermaid
sequenceDiagram
    participant R as Requester Agent
    participant C as Mock CAP Network
    participant P as ProofMesh Provider
    participant A as ProofMesh Audit Core

    R->>C: create_negotiation(VerificationRequest)
    C-->>P: negotiation_created
    P->>C: accept_negotiation
    C-->>R: order_created
    R->>C: pay_order
    C-->>P: order_paid
    P->>A: audit_request(requirements + mock_cap_receipt)
    A-->>P: VerificationResponse
    P->>C: deliver_order(VerificationResponse)
    C-->>R: order_completed + delivery
```

## Live/Staging CROO Boundary

```mermaid
sequenceDiagram
    participant U as Operator / Buyer
    participant C as CROO API + Store
    participant P as ProofMesh Python Provider
    participant A as ProofMesh Audit Core
    participant W as Wallet Funding

    U->>W: fund buyer wallet
    U->>C: attempt service purchase
    P->>C: listen for negotiations via croo-sdk
    C-->>P: pending negotiation / paid order
    P->>A: audit_request(requirements + live receipt)
    A-->>P: structured verification report
    P->>C: deliver_order(report)
    Note over W,C: In the documented attempt, funding did not appear on usable purchase balance, so no order receipt was obtained.
```

## Component Boundaries

```text
examples/run_mock_cap_demo.py
  |
  | requester-side demo command
  v
src/proofmesh/cap_mock.py
  |
  | negotiation, payment event, ledger, delivery log
  v
src/proofmesh/provider.py
  |
  | provider accepts paid order and calls audit core
  v
src/proofmesh/auditor.py
  |
  | claim-level verification
  v
VerificationResponse JSON
```

## Evidence Artifacts

- `artifacts/phase2/mock-cap-demo-log.json`
- `artifacts/phase2/mock-cap-demo-log.md`
- `artifacts/phase2/mock-cap-batch-summary.json`
- `artifacts/phase2/mock-cap-batch-summary.md`
- `artifacts/benchmark/proofmesh-mini-benchmark.json`
- `artifacts/benchmark/proofmesh-mini-benchmark.md`
- `artifacts/phase3/live-readiness-report.json`
- `artifacts/phase3/croo-purchase-attempt.md`
