#!/usr/bin/env python3
"""List visible CROO negotiations/orders for diagnosing staging payments."""

from __future__ import annotations

import argparse
import asyncio
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

from proofmesh.config import load_config  # noqa: E402
from proofmesh.croo_provider import _object_to_dict  # noqa: E402


DEFAULT_OUTPUT_JSON = ROOT / "artifacts" / "phase3" / "croo-activity-report.json"
DEFAULT_OUTPUT_MD = ROOT / "artifacts" / "phase3" / "croo-activity-report.md"


ORDER_FIELDS = [
    "order_id",
    "negotiation_id",
    "chain_order_id",
    "service_id",
    "requester_agent_id",
    "provider_agent_id",
    "status",
    "price",
    "payment_token",
    "fee_amount",
    "fund_amount",
    "fund_token",
    "requester_wallet_address",
    "provider_wallet_address",
    "create_tx_hash",
    "pay_tx_hash",
    "deliver_tx_hash",
    "reject_tx_hash",
    "clear_tx_hash",
    "created_at",
    "paid_at",
    "delivered_at",
    "rejected_at",
    "expired_at",
    "created_time",
    "updated_time",
]

NEGOTIATION_FIELDS = [
    "negotiation_id",
    "service_id",
    "requester_agent_id",
    "provider_agent_id",
    "status",
    "reject_reason",
    "expires_at",
    "fund_amount",
    "fund_token",
    "provider_fund_address",
    "created_time",
    "updated_time",
]


async def async_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check visible CROO orders and negotiations")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--agent-id", default="", help="Optional agent id filter. Defaults to no agent filter.")
    parser.add_argument("--service-id", default="", help="Optional service id filter. Defaults to ProofMesh service id.")
    parser.add_argument("--include-all-services", action="store_true")
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args(argv)

    config = load_config()
    if not config.croo_sdk_key:
        raise SystemExit("CROO_API_KEY is missing in this shell. Export it and rerun this command.")

    from croo import AgentClient, Config, ListOptions

    client = AgentClient(Config(base_url=config.croo_api_url, ws_url=config.croo_ws_url), config.croo_sdk_key)
    service_id = args.service_id or config.service_id
    try:
        report: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": config.mode,
            "api_url": config.croo_api_url,
            "configured_provider_agent_id": config.provider_agent_id,
            "service_filter": "" if args.include_all_services else service_id,
            "agent_filter": args.agent_id,
            "negotiations": [],
            "orders": [],
            "errors": [],
        }

        for role in ("provider", "requester"):
            opts = ListOptions(role=role, agent_id=args.agent_id or None, page_size=args.page_size)
            await _collect_negotiations(client, opts, role, report, service_id, args.include_all_services)
            await _collect_orders(client, opts, role, report, service_id, args.include_all_services)

        report["summary"] = _build_summary(report)
    finally:
        await client.close()

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(report) + "\n", encoding="utf-8")

    print(f"CROO activity report: {args.output_json}")
    print(f"Markdown report: {args.output_md}")
    print(render_console_summary(report))
    return 0


async def _collect_negotiations(
    client: Any,
    opts: Any,
    role: str,
    report: dict[str, Any],
    service_id: str,
    include_all_services: bool,
) -> None:
    try:
        negotiations = await client.list_negotiations(opts)
    except Exception as exc:  # noqa: BLE001 - diagnostic script should preserve API errors
        report["errors"].append({"kind": "negotiations", "role": role, "error": str(exc)})
        return

    for negotiation in negotiations:
        item = _select_fields(_object_to_dict(negotiation), NEGOTIATION_FIELDS)
        item["role_query"] = role
        if include_all_services or item.get("service_id") == service_id:
            report["negotiations"].append(item)


async def _collect_orders(
    client: Any,
    opts: Any,
    role: str,
    report: dict[str, Any],
    service_id: str,
    include_all_services: bool,
) -> None:
    try:
        orders = await client.list_orders(opts)
    except Exception as exc:  # noqa: BLE001 - diagnostic script should preserve API errors
        report["errors"].append({"kind": "orders", "role": role, "error": str(exc)})
        return

    for order in orders:
        item = _select_fields(_object_to_dict(order), ORDER_FIELDS)
        item["role_query"] = role
        if include_all_services or item.get("service_id") == service_id:
            report["orders"].append(item)


def _select_fields(data: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {field: data.get(field, "") for field in fields if data.get(field, "") not in ("", None)}


def _build_summary(report: dict[str, Any]) -> dict[str, Any]:
    order_status_counts = Counter(order.get("status", "unknown") for order in report["orders"])
    negotiation_status_counts = Counter(item.get("status", "unknown") for item in report["negotiations"])
    tx_hashes = []
    for order in report["orders"]:
        for field in ("create_tx_hash", "pay_tx_hash", "deliver_tx_hash", "reject_tx_hash", "clear_tx_hash"):
            if order.get(field):
                tx_hashes.append({"order_id": order.get("order_id", ""), "field": field, "tx_hash": order[field]})

    paid_like_statuses = {"paid", "delivering", "completed"}
    paid_like_orders = [
        order for order in report["orders"] if str(order.get("status", "")).lower() in paid_like_statuses
    ]
    return {
        "orders_total": len(report["orders"]),
        "negotiations_total": len(report["negotiations"]),
        "order_status_counts": dict(order_status_counts),
        "negotiation_status_counts": dict(negotiation_status_counts),
        "tx_hashes": tx_hashes,
        "paid_like_orders": len(paid_like_orders),
        "diagnosis": _diagnose(report["orders"], report["negotiations"], tx_hashes),
    }


def _diagnose(orders: list[dict[str, Any]], negotiations: list[dict[str, Any]], tx_hashes: list[dict[str, str]]) -> str:
    if not orders and not negotiations:
        return (
            "No visible CROO orders or negotiations for this SDK key/filter. "
            "If USDC is missing, check the wallet transaction history and chain/network first."
        )
    if any(str(order.get("status", "")).lower() in {"paid", "delivering", "completed"} for order in orders):
        return (
            "At least one order is paid/delivering/completed. Funds may have moved into a CROO order or settlement flow; "
            "inspect pay_tx_hash and order status."
        )
    if any(str(order.get("status", "")).lower() == "pay_failed" for order in orders):
        return "At least one order has pay_failed status. Inspect create/pay tx hashes and wallet balance on the payment chain."
    if tx_hashes:
        return "CROO returned transaction hashes, but no paid/completed order is visible. Inspect those hashes on the chain explorer."
    return "CROO activity is visible, but no paid order is visible yet. Inspect pending/created order status in CROO UI."


def render_console_summary(report: dict[str, Any]) -> str:
    summary = report["summary"]
    return "\n".join(
        [
            f"Orders: {summary['orders_total']} {summary['order_status_counts']}",
            f"Negotiations: {summary['negotiations_total']} {summary['negotiation_status_counts']}",
            f"Tx hashes: {len(summary['tx_hashes'])}",
            f"Diagnosis: {summary['diagnosis']}",
        ]
    )


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# CROO Activity Report",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Mode: `{report['mode']}`",
        f"- API URL: `{report['api_url']}`",
        f"- Configured provider agent: `{report['configured_provider_agent_id']}`",
        f"- Service filter: `{report['service_filter'] or 'all services'}`",
        f"- Agent filter: `{report['agent_filter'] or 'none'}`",
        "",
        "## Summary",
        "",
        f"- Orders total: `{summary['orders_total']}`",
        f"- Negotiations total: `{summary['negotiations_total']}`",
        f"- Order statuses: `{summary['order_status_counts']}`",
        f"- Negotiation statuses: `{summary['negotiation_status_counts']}`",
        f"- Transaction hashes found: `{len(summary['tx_hashes'])}`",
        f"- Diagnosis: {summary['diagnosis']}",
        "",
        "## Orders",
        "",
    ]
    if report["orders"]:
        lines.extend(_render_table(report["orders"], ["role_query", "order_id", "status", "price", "payment_token", "pay_tx_hash"]))
    else:
        lines.append("No matching orders returned by CROO.")

    lines.extend(["", "## Negotiations", ""])
    if report["negotiations"]:
        lines.extend(_render_table(report["negotiations"], ["role_query", "negotiation_id", "status", "requester_agent_id", "provider_agent_id"]))
    else:
        lines.append("No matching negotiations returned by CROO.")

    lines.extend(["", "## Transaction Hashes", ""])
    if summary["tx_hashes"]:
        lines.extend(_render_table(summary["tx_hashes"], ["order_id", "field", "tx_hash"]))
    else:
        lines.append("No transaction hashes returned by CROO.")

    if report["errors"]:
        lines.extend(["", "## API Errors", ""])
        lines.extend(_render_table(report["errors"], ["kind", "role", "error"]))
    return "\n".join(lines)


def _render_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def main(argv: list[str] | None = None) -> int:
    return asyncio.run(async_main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
