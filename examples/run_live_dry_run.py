#!/usr/bin/env python3
"""Run a live-ready ProofMesh audit without submitting to CROO."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofmesh.config import load_config  # noqa: E402
from proofmesh.live_adapter import LiveCROOAdapter  # noqa: E402


DEFAULT_REQUEST = ROOT / "examples" / "cases" / "supported_artifact.json"
DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "phase3" / "live-dry-run-audit.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "phase3" / "live-dry-run-audit.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run ProofMesh live-ready dry-run audit")
    parser.add_argument("--request", type=Path, default=DEFAULT_REQUEST)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args(argv)

    requirements = json.loads(args.request.read_text(encoding="utf-8"))
    audit = LiveCROOAdapter(load_config()).audit_dry_run(requirements)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(audit) + "\n", encoding="utf-8")

    print(f"Live dry-run audit: {args.output_json}")
    print(f"Markdown audit: {args.output_md}")
    return 0


def render_markdown(audit: dict) -> str:
    readiness = audit["live_readiness"]
    coverage = audit["source_coverage"]
    receipt = audit["cap_receipt"]
    lines = [
        "# ProofMesh Live-Ready Dry Run",
        "",
        f"- Task: `{audit['task_id']}`",
        f"- Verified: `{audit['is_verified']}`",
        f"- Confidence: `{audit['overall_confidence']}`",
        f"- Receipt mode: `{receipt['mode']}`",
        f"- Readiness ready: `{readiness['ready']}`",
        "",
        "## Coverage",
        "",
        f"- Claims total: `{coverage['claims_total']}`",
        f"- Supported: `{coverage['claims_supported']}`",
        f"- Unsupported: `{coverage['claims_unsupported']}`",
        f"- Contradicted: `{coverage['claims_contradicted']}`",
        "",
        "## Readiness Checks",
        "",
        "| Check | OK | Detail |",
        "| --- | --- | --- |",
    ]
    for check in readiness["checks"]:
        lines.append(f"| {check['name']} | {check['ok']} | {check['detail']} |")
    lines.extend(["", "## Limitation", "", "Dry-run only. No live CROO order or settlement was created."])
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

