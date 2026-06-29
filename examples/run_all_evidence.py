#!/usr/bin/env python3
"""Regenerate ProofMesh local evidence artifacts for judges."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


COMMANDS = [
    [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/research_claim.json",
        "--format",
        "json",
        "--output",
        "artifacts/demo-audit.json",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/research_claim.json",
        "--format",
        "markdown",
        "--output",
        "artifacts/demo-audit.md",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/supported_artifact.json",
        "--format",
        "json",
        "--output",
        "artifacts/phase1/supported-artifact.json",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/supported_artifact.json",
        "--format",
        "markdown",
        "--output",
        "artifacts/phase1/supported-artifact.md",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/unsupported_claim.json",
        "--format",
        "json",
        "--output",
        "artifacts/phase1/unsupported-claim.json",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/unsupported_claim.json",
        "--format",
        "markdown",
        "--output",
        "artifacts/phase1/unsupported-claim.md",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/contradicted_claim.json",
        "--format",
        "json",
        "--output",
        "artifacts/phase1/contradicted-claim.json",
    ],
    [
        sys.executable,
        "-m",
        "proofmesh.cli",
        "audit",
        "examples/cases/contradicted_claim.json",
        "--format",
        "markdown",
        "--output",
        "artifacts/phase1/contradicted-claim.md",
    ],
    [
        sys.executable,
        "examples/run_mock_cap_demo.py",
    ],
    [
        sys.executable,
        "examples/run_mock_cap_batch.py",
    ],
    [
        sys.executable,
        "examples/run_benchmark.py",
    ],
    [
        sys.executable,
        "examples/check_live_readiness.py",
    ],
    [
        sys.executable,
        "examples/run_live_dry_run.py",
    ],
]


def main() -> int:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    for command in COMMANDS:
        print("+ " + " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, env=env, check=True)
    print("\nEvidence regeneration complete.")
    print("Live/staging settlement remains a dry run unless a real CROO order receipt is attached.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
