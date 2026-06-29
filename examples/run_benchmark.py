#!/usr/bin/env python3
"""Run a deterministic mini benchmark for ProofMesh claim verification."""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofmesh.auditor import audit_request  # noqa: E402


DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "benchmark" / "proofmesh-mini-benchmark.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "benchmark" / "proofmesh-mini-benchmark.md"


TOPICS = [
    ("alpha", "evidence mesh records source coverage for every claim"),
    ("beta", "audit reports include confidence scores and limitations"),
    ("gamma", "provider services return structured verification results"),
    ("delta", "requester agents can compare supported and unsupported claims"),
    ("epsilon", "settlement metadata is separated from factual verification"),
    ("zeta", "claim audits preserve source identifiers for traceability"),
    ("eta", "batch evaluation summarizes supported unsupported and contradicted cases"),
    ("theta", "dry run artifacts avoid claiming live settlement"),
    ("iota", "schema validation requires claims or artifact text"),
    ("kappa", "pricing metadata is recorded per audit request"),
]


def build_cases() -> list[dict[str, Any]]:
    cases = []
    for index, (topic, statement) in enumerate(TOPICS, start=1):
        cases.append(
            {
                "case_id": f"supported-{index:02d}",
                "expected_status": "supported",
                "request": {
                    "task_id": f"bench-supported-{index:02d}",
                    "artifact_type": "claim_set",
                    "claims": [
                        {
                            "id": "c1",
                            "text": f"The {topic} module {statement}.",
                            "source_ids": ["s1"],
                        }
                    ],
                    "sources": [
                        {
                            "id": "s1",
                            "title": f"{topic.title()} source",
                            "text": f"The {topic} module {statement} in the ProofMesh benchmark.",
                        }
                    ],
                },
            }
        )

        cases.append(
            {
                "case_id": f"unsupported-{index:02d}",
                "expected_status": "unsupported",
                "request": {
                    "task_id": f"bench-unsupported-{index:02d}",
                    "artifact_type": "claim_set",
                    "claims": [
                        {
                            "id": "c1",
                            "text": f"The {topic} module performs orbital weather prediction for satellites.",
                            "source_ids": ["s1"],
                        }
                    ],
                    "sources": [
                        {
                            "id": "s1",
                            "title": f"{topic.title()} source",
                            "text": f"The {topic} service documentation discusses source coverage, audit reports, and verification metadata.",
                        }
                    ],
                },
            }
        )

        cases.append(
            {
                "case_id": f"contradicted-{index:02d}",
                "expected_status": "contradicted",
                "request": {
                    "task_id": f"bench-contradicted-{index:02d}",
                    "artifact_type": "claim_set",
                    "claims": [
                        {
                            "id": "c1",
                            "text": f"The {topic} module does not {statement}.",
                            "source_ids": ["s1"],
                        }
                    ],
                    "sources": [
                        {
                            "id": "s1",
                            "title": f"{topic.title()} source",
                            "text": f"The {topic} module {statement} in the ProofMesh benchmark.",
                        }
                    ],
                },
            }
        )
    return cases


def run_benchmark(cases: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    confusion: dict[str, Counter[str]] = {}
    for case in cases:
        report = audit_request(case["request"])
        actual_status = report["claim_audits"][0]["status"] if report["claim_audits"] else "missing"
        expected_status = case["expected_status"]
        confusion.setdefault(expected_status, Counter())[actual_status] += 1
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": expected_status,
                "actual_status": actual_status,
                "correct": expected_status == actual_status,
                "is_verified": report["is_verified"],
                "overall_confidence": report["overall_confidence"],
            }
        )

    correct = sum(1 for row in rows if row["correct"])
    total = len(rows)
    per_label = _per_label_metrics(rows)
    return {
        "benchmark": "proofmesh-mini-benchmark",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases_total": total,
        "cases_correct": correct,
        "accuracy": round(correct / total, 3) if total else 0.0,
        "labels": ["supported", "unsupported", "contradicted"],
        "per_label": per_label,
        "confusion": {label: dict(counts) for label, counts in confusion.items()},
        "rows": rows,
        "limitations": [
            "Synthetic benchmark cases are deterministic and intentionally simple.",
            "Scores measure the current transparent MVP behavior, not broad factual truth verification.",
            "The benchmark is meant for regression checks and judge-facing reproducibility, not academic generalization.",
        ],
    }


def _per_label_metrics(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    labels = sorted({row["expected_status"] for row in rows} | {row["actual_status"] for row in rows})
    metrics = {}
    for label in labels:
        tp = sum(1 for row in rows if row["expected_status"] == label and row["actual_status"] == label)
        fp = sum(1 for row in rows if row["expected_status"] != label and row["actual_status"] == label)
        fn = sum(1 for row in rows if row["expected_status"] == label and row["actual_status"] != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        metrics[label] = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "support": sum(1 for row in rows if row["expected_status"] == label),
        }
    return metrics


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# ProofMesh Mini Benchmark",
        "",
        f"- Generated at: `{result['generated_at']}`",
        f"- Cases: `{result['cases_total']}`",
        f"- Correct: `{result['cases_correct']}`",
        f"- Accuracy: `{result['accuracy']}`",
        "",
        "## Per-Label Metrics",
        "",
        "| Label | Precision | Recall | Support |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, metrics in result["per_label"].items():
        lines.append(
            f"| {label} | {metrics['precision']} | {metrics['recall']} | {metrics['support']} |"
        )

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Expected | Actual | Correct | Confidence |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in result["rows"]:
        lines.append(
            f"| {row['case_id']} | {row['expected_status']} | {row['actual_status']} | "
            f"{row['correct']} | {row['overall_confidence']} |"
        )

    lines.extend(["", "## Limitations", ""])
    for limitation in result["limitations"]:
        lines.append(f"- {limitation}")
    return "\n".join(lines)


def main() -> int:
    result = run_benchmark(build_cases())
    DEFAULT_OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    DEFAULT_OUTPUT_MD.write_text(render_markdown(result) + "\n", encoding="utf-8")
    print(f"Benchmark JSON: {DEFAULT_OUTPUT_JSON}")
    print(f"Benchmark Markdown: {DEFAULT_OUTPUT_MD}")
    print(f"Accuracy: {result['accuracy']} ({result['cases_correct']}/{result['cases_total']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
