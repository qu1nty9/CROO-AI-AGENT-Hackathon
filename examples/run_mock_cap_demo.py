#!/usr/bin/env python3
"""Run the local ProofMesh mock CAP lifecycle demo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofmesh.mock_lifecycle import run_mock_cap_lifecycle  # noqa: E402


DEFAULT_REQUEST = ROOT / "examples" / "cases" / "contradicted_claim.json"
DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "phase2" / "mock-cap-demo-log.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "phase2" / "mock-cap-demo-log.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run ProofMesh mock CAP lifecycle demo")
    parser.add_argument("--request", type=Path, default=DEFAULT_REQUEST)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args(argv)

    requirements = json.loads(args.request.read_text(encoding="utf-8"))
    demo = run_demo(requirements)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(demo, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(demo) + "\n", encoding="utf-8")

    print(f"Mock CAP demo complete: {args.output_json}")
    print(f"Markdown summary: {args.output_md}")
    return 0


def run_demo(requirements: dict[str, Any]) -> dict[str, Any]:
    return run_mock_cap_lifecycle(requirements)


def render_markdown(demo: dict[str, Any]) -> str:
    summary = demo["lifecycle_summary"]
    audit = demo["delivered_audit"]
    coverage = audit["source_coverage"]

    lines = [
        "# ProofMesh Mock CAP Lifecycle Demo",
        "",
        "## Summary",
        "",
        f"- Service: `{demo['service_id']}`",
        f"- Requester: `{demo['requester_agent_id']}`",
        f"- Provider: `{demo['provider_agent_id']}`",
        f"- Negotiation: `{summary['negotiation_id']}`",
        f"- Order: `{summary['order_id']}`",
        f"- Delivery: `{summary['delivery_id']}`",
        f"- Payment tx: `{summary['payment_tx_id']}`",
        f"- Payment block: `{summary['payment_block_number']}`",
        f"- Final order status: `{summary['final_order_status']}`",
        f"- Audit verified: `{summary['audit_is_verified']}`",
        f"- Audit confidence: `{summary['audit_overall_confidence']}`",
        "",
        "## CAP Lifecycle",
        "",
    ]

    for event in demo["network_log"]["events"]:
        lines.append(f"- `{event['event_type']}` at `{event['timestamp']}`")

    lines.extend(
        [
            "",
            "## Delivered Audit",
            "",
            f"- Schema version: `{audit['schema_version']}`",
            f"- Task: `{audit['task_id']}`",
            f"- Artifact type: `{audit['artifact_type']}`",
            f"- Audit mode: `{audit['audit_mode']}`",
            f"- Verified: `{audit['is_verified']}`",
            f"- Overall confidence: `{audit['overall_confidence']}`",
            f"- Claims total: `{coverage['claims_total']}`",
            f"- Supported: `{coverage['claims_supported']}`",
            f"- Unsupported: `{coverage['claims_unsupported']}`",
            f"- Contradicted: `{coverage['claims_contradicted']}`",
            "",
            "## Claim Results",
            "",
        ]
    )

    for item in audit["claim_audits"]:
        lines.extend(
            [
                f"### {item['claim_id']}: {item['status']}",
                "",
                item["claim"],
                "",
                f"- Confidence: `{item['confidence']}`",
            ]
        )
        if item["contradiction_sources"]:
            lines.append(f"- Contradiction sources: `{', '.join(item['contradiction_sources'])}`")
        for note in item["notes"]:
            lines.append(f"- Note: {note}")
        lines.append("")

    lines.extend(
        [
            "## Receipt Discipline",
            "",
            "This is a mock CAP lifecycle for local reproducibility. It is not a live CROO settlement.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
