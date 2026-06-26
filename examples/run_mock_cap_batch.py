#!/usr/bin/env python3
"""Run all canonical ProofMesh cases through the mock CAP lifecycle."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from time import perf_counter
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofmesh.mock_lifecycle import run_mock_cap_lifecycle, summarize_lifecycle  # noqa: E402


DEFAULT_CASES = [
    ("supported", ROOT / "examples" / "cases" / "supported_artifact.json"),
    ("unsupported", ROOT / "examples" / "cases" / "unsupported_claim.json"),
    ("contradicted", ROOT / "examples" / "cases" / "contradicted_claim.json"),
]
DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "phase2" / "mock-cap-batch-summary.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "phase2" / "mock-cap-batch-summary.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all canonical cases through mock CAP")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args(argv)

    summary = run_batch(DEFAULT_CASES)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(summary) + "\n", encoding="utf-8")

    print(f"Mock CAP batch complete: {args.output_json}")
    print(f"Markdown summary: {args.output_md}")
    return 0


def run_batch(cases: list[tuple[str, Path]]) -> dict[str, Any]:
    case_results = []
    for case_name, path in cases:
        requirements = json.loads(path.read_text(encoding="utf-8"))
        started = perf_counter()
        demo = run_mock_cap_lifecycle(requirements)
        elapsed_ms = round((perf_counter() - started) * 1000, 3)
        compact = summarize_lifecycle(demo)
        compact.update(
            {
                "case_name": case_name,
                "request_path": str(path.relative_to(ROOT)),
                "elapsed_ms": elapsed_ms,
                "negotiation_id": demo["lifecycle_summary"]["negotiation_id"],
                "order_id": demo["lifecycle_summary"]["order_id"],
                "delivery_id": demo["lifecycle_summary"]["delivery_id"],
                "payment_tx_id": demo["lifecycle_summary"]["payment_tx_id"],
            }
        )
        case_results.append(compact)

    elapsed_values = [item["elapsed_ms"] for item in case_results]
    total_cost = sum(item["paid_amount_croo"] for item in case_results)
    return {
        "demo_name": "proofmesh_mock_cap_batch",
        "case_count": len(case_results),
        "total_mock_cost_croo": round(total_cost, 6),
        "avg_elapsed_ms": round(statistics.mean(elapsed_values), 3) if elapsed_values else 0.0,
        "max_elapsed_ms": max(elapsed_values) if elapsed_values else 0.0,
        "cases": case_results,
        "limitation": "Mock CAP batch evidence only; not live CROO settlement.",
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# ProofMesh Mock CAP Batch Summary",
        "",
        f"- Cases: `{summary['case_count']}`",
        f"- Total mock cost: `{summary['total_mock_cost_croo']} CROO`",
        f"- Average elapsed: `{summary['avg_elapsed_ms']} ms`",
        f"- Max elapsed: `{summary['max_elapsed_ms']} ms`",
        "",
        "## Cases",
        "",
        "| Case | Verified | Supported | Unsupported | Contradicted | Cost | Elapsed |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for item in summary["cases"]:
        lines.append(
            "| "
            f"{item['case_name']} | "
            f"{item['is_verified']} | "
            f"{item['claims_supported']} | "
            f"{item['claims_unsupported']} | "
            f"{item['claims_contradicted']} | "
            f"{item['paid_amount_croo']} CROO | "
            f"{item['elapsed_ms']} ms |"
        )

    lines.extend(
        [
            "",
            "## Lifecycle Events",
            "",
        ]
    )
    for item in summary["cases"]:
        lines.append(f"- `{item['case_name']}`: {', '.join(item['event_types'])}")

    lines.extend(
        [
            "",
            "## Limitation",
            "",
            summary["limitation"],
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

