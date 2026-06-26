"""Command line interface for ProofMesh."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .auditor import audit_request
from .schema import RequestValidationError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="proofmesh")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="audit a verification request JSON file")
    audit_parser.add_argument("request_path", type=Path)
    audit_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    audit_parser.add_argument("--output", type=Path)

    args = parser.parse_args(argv)

    if args.command == "audit":
        payload = _read_json(args.request_path)
        try:
            report = audit_request(payload)
        except RequestValidationError as exc:
            raise SystemExit(f"invalid ProofMesh request: {exc}") from None
        rendered = _render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)
        if args.output:
            args.output.write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"request file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from None

    if not isinstance(data, dict):
        raise SystemExit("request JSON must be an object")
    return data


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# ProofMesh Audit: {report['task_id']}",
        "",
        f"- Schema version: `{report['schema_version']}`",
        f"- Artifact type: `{report['artifact_type']}`",
        f"- Audit mode: `{report['audit_mode']}`",
        f"- Verified: `{report['is_verified']}`",
        f"- Overall confidence: `{report['overall_confidence']}`",
        "",
        "## Source Coverage",
        "",
    ]

    for key, value in report["source_coverage"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Claim Audits", ""])
    for item in report["claim_audits"]:
        lines.extend(
            [
                f"### {item['claim_id']}: {item['status']}",
                "",
                item["claim"],
                "",
                f"- Confidence: `{item['confidence']}`",
            ]
        )
        if item["supporting_sources"]:
            lines.append("- Supporting sources:")
            for source in item["supporting_sources"]:
                title = source["title"] or source["source_id"]
                lines.append(f"  - `{source['source_id']}` {title} ({source['support_score']})")
        if item["contradiction_sources"]:
            lines.append(f"- Contradiction sources: `{', '.join(item['contradiction_sources'])}`")
        for note in item["notes"]:
            lines.append(f"- Note: {note}")
        lines.append("")

    lines.extend(["## Limitations", ""])
    for limitation in report["limitations"]:
        lines.append(f"- {limitation}")

    lines.extend(["", "## CAP Receipt", "", "```json", json.dumps(report["cap_receipt"], indent=2), "```"])
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
