#!/usr/bin/env python3
"""Run the live/staging CROO provider for ProofMesh."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofmesh.config import load_config  # noqa: E402
from proofmesh.croo_provider import CROOProofMeshProvider  # noqa: E402


async def async_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the ProofMesh CROO provider")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process currently pending/paid CROO work and exit instead of listening forever.",
    )
    args = parser.parse_args(argv)

    config = load_config()
    provider = CROOProofMeshProvider(
        config,
        provider_fund_address=os.environ.get("PROOFMESH_PROVIDER_FUND_ADDRESS", ""),
    )
    print(f"ProofMesh provider mode: {config.mode}")
    print(f"Service ID: {config.service_id}")
    print(f"Provider Agent ID: {config.provider_agent_id}")
    try:
        if args.once:
            await provider.reconcile_existing()
            print("Processed currently visible CROO work.")
        else:
            await provider.run_forever()
    finally:
        await provider.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return asyncio.run(async_main(argv))
    except KeyboardInterrupt:
        print("\nProvider stopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
