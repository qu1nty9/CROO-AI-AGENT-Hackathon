#!/usr/bin/env python3
"""Generate ProofMesh live/staging CROO readiness artifacts."""

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


DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "phase3" / "live-readiness-report.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "phase3" / "live-readiness-report.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check ProofMesh live CROO readiness")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args(argv)

    report = LiveCROOAdapter(load_config()).check_readiness()
    data = report.to_dict()

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(data) + "\n", encoding="utf-8")

    print(f"Readiness report: {args.output_json}")
    print(f"Markdown report: {args.output_md}")
    return 0


def render_markdown(report: dict) -> str:
    lines = [
        "# ProofMesh CROO Live Readiness",
        "",
        f"- Ready: `{report['ready']}`",
        f"- Mode: `{report['config']['mode']}`",
        f"- API URL: `{report['config']['croo_api_url']}`",
        f"- WS URL: `{report['config']['croo_ws_url']}`",
        f"- Service ID: `{report['config']['service_id']}`",
        "",
        "## Checks",
        "",
        "| Check | OK | Detail |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        lines.append(f"| {check['name']} | {check['ok']} | {check['detail']} |")

    lines.extend(["", "## Next Steps", ""])
    for step in report["next_steps"]:
        lines.append(f"- {step}")

    lines.extend(
        [
            "",
            "## Service Listing",
            "",
            f"- Agent: `{report['service_listing']['agent_name']}`",
            f"- Service: `{report['service_listing']['service_id']}`",
            f"- Price: `{report['service_listing']['price']['amount']} {report['service_listing']['price']['token']}`",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
