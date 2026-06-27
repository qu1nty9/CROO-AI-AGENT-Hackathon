"""Live CROO provider runner for ProofMesh.

The module is intentionally thin around the official `croo-sdk` package. It
does not simulate settlement; it accepts real CROO negotiations and delivers a
ProofMesh JSON audit when an order reaches the paid state.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .auditor import audit_request
from .config import ProofMeshConfig
from .provider import _invalid_request_report
from .schema import RequestValidationError, SCHEMA_VERSION


PROOFMESH_DELIVERABLE_SCHEMA = {
    "schema_version": SCHEMA_VERSION,
    "type": "object",
    "required": [
        "schema_version",
        "task_id",
        "is_verified",
        "overall_confidence",
        "source_coverage",
        "claim_audits",
        "limitations",
        "cap_receipt",
    ],
}


def parse_requirements(raw_requirements: str) -> dict[str, Any]:
    """Parse CROO negotiation requirements into a ProofMesh audit request."""

    text = (raw_requirements or "").strip()
    if not text:
        return {
            "task_id": "croo-empty-requirements",
            "artifact_type": "unknown",
            "artifact_text": "",
            "sources": [],
        }

    try:
        decoded = json.loads(text)
    except json.JSONDecodeError:
        return {
            "task_id": "croo-text-requirements",
            "artifact_type": "text",
            "artifact_text": text,
            "sources": [],
        }

    if isinstance(decoded, dict):
        return decoded

    return {
        "task_id": "croo-json-requirements",
        "artifact_type": "json",
        "artifact_text": json.dumps(decoded, sort_keys=True),
        "sources": [],
    }


def build_live_cap_receipt(
    *,
    config: ProofMeshConfig,
    order: Any,
    negotiation: Any | None = None,
) -> dict[str, Any]:
    """Build the live/staging receipt metadata attached to delivered audits."""

    order_data = _object_to_dict(order)
    negotiation_data = _object_to_dict(negotiation) if negotiation is not None else {}
    mode = "croo_staging" if config.mode == "staging" else "croo_live"
    return {
        "mode": mode,
        "settlement_status": order_data.get("status", "unknown"),
        "service_id": order_data.get("service_id") or config.service_id,
        "provider_agent_id": order_data.get("provider_agent_id") or config.provider_agent_id,
        "requester_agent_id": order_data.get("requester_agent_id") or negotiation_data.get("requester_agent_id", ""),
        "negotiation_id": order_data.get("negotiation_id") or negotiation_data.get("negotiation_id", ""),
        "order_id": order_data.get("order_id", ""),
        "chain_order_id": order_data.get("chain_order_id", ""),
        "price": order_data.get("price", ""),
        "payment_token": order_data.get("payment_token", ""),
        "create_tx_hash": order_data.get("create_tx_hash", ""),
        "pay_tx_hash": order_data.get("pay_tx_hash", ""),
        "deliver_tx_hash": order_data.get("deliver_tx_hash", ""),
        "api_url": config.croo_api_url,
        "ws_url": config.croo_ws_url,
    }


def build_delivery_report(
    *,
    config: ProofMeshConfig,
    order: Any,
    negotiation: Any,
) -> dict[str, Any]:
    """Convert CROO order requirements into a ProofMesh audit report."""

    requirements = parse_requirements(getattr(negotiation, "requirements", ""))
    requirements["cap_receipt"] = build_live_cap_receipt(
        config=config,
        order=order,
        negotiation=negotiation,
    )
    try:
        return audit_request(requirements)
    except RequestValidationError as exc:
        return _invalid_request_report(
            order_id=str(getattr(order, "order_id", "")),
            requirements=requirements,
            error=str(exc),
        )


class CROOProofMeshProvider:
    """Async provider process backed by the official CROO Python SDK."""

    def __init__(self, config: ProofMeshConfig, *, provider_fund_address: str = "") -> None:
        self.config = config
        self.provider_fund_address = provider_fund_address
        self._client = _build_croo_client(config)
        self._seen_orders: set[str] = set()

    async def close(self) -> None:
        await self._client.close()

    async def reconcile_existing(self) -> None:
        """Process pending negotiations and already-paid orders visible to this provider."""

        await self._accept_pending_negotiations()
        await self._deliver_paid_orders()

    async def run_forever(self) -> None:
        """Run the provider loop until interrupted."""

        await self.reconcile_existing()
        stream = await self._client.connect_websocket()
        stream.on_any(lambda event: asyncio.create_task(self.handle_event(event)))
        print("ProofMesh CROO provider is listening for negotiations and paid orders.")
        try:
            await asyncio.Event().wait()
        finally:
            await stream.close()

    async def handle_event(self, event: Any) -> None:
        event_type = _event_field(event, "type")
        service_id = _event_field(event, "service_id")
        negotiation_id = _event_field(event, "negotiation_id")
        order_id = _event_field(event, "order_id")

        if service_id and service_id != self.config.service_id:
            return

        if event_type == "order_negotiation_created" and negotiation_id:
            await self.accept_negotiation(negotiation_id)
        elif event_type == "order_paid" and order_id:
            await self.deliver_order(order_id)

    async def accept_negotiation(self, negotiation_id: str) -> None:
        negotiation = await self._client.get_negotiation(negotiation_id)
        if negotiation.service_id != self.config.service_id:
            return
        if negotiation.status != "pending":
            print(f"Skipping negotiation {negotiation_id}: status={negotiation.status}")
            return

        if negotiation.fund_amount or negotiation.fund_token:
            if not self.provider_fund_address:
                raise RuntimeError(
                    "CROO negotiation requires fund transfer, but PROOFMESH_PROVIDER_FUND_ADDRESS is not set. "
                    "ProofMesh should normally keep Require Fund Transfer disabled."
                )
            result = await self._client.accept_negotiation_with_fund_address(
                negotiation_id,
                self.provider_fund_address,
            )
        else:
            result = await self._client.accept_negotiation(negotiation_id)

        print(
            "Accepted negotiation "
            f"{result.negotiation.negotiation_id}; order={result.order.order_id}; status={result.order.status}"
        )

    async def deliver_order(self, order_id: str) -> None:
        if order_id in self._seen_orders:
            return
        order = await self._client.get_order(order_id)
        if order.service_id != self.config.service_id:
            return
        if order.status == "completed":
            print(f"Skipping order {order_id}: already completed")
            self._seen_orders.add(order_id)
            return
        if order.status != "paid":
            print(f"Skipping order {order_id}: status={order.status}")
            return

        negotiation = await self._client.get_negotiation(order.negotiation_id)
        report = build_delivery_report(config=self.config, order=order, negotiation=negotiation)
        deliverable_text = json.dumps(report, indent=2, sort_keys=True)

        from croo import DeliverOrderRequest, DeliverableType

        result = await self._client.deliver_order(
            order_id,
            DeliverOrderRequest(
                deliverable_type=DeliverableType.SCHEMA,
                deliverable_schema=json.dumps(PROOFMESH_DELIVERABLE_SCHEMA, sort_keys=True),
                deliverable_text=deliverable_text,
            ),
        )
        self._seen_orders.add(order_id)
        print(
            "Delivered order "
            f"{result.order.order_id}; delivery={result.delivery.delivery_id}; "
            f"status={result.order.status}; tx={result.tx_hash}"
        )

    async def _accept_pending_negotiations(self) -> None:
        from croo import ListOptions

        negotiations = await self._client.list_negotiations(
            ListOptions(role="provider", agent_id=self.config.provider_agent_id, status="pending")
        )
        for negotiation in negotiations:
            if negotiation.service_id == self.config.service_id:
                await self.accept_negotiation(negotiation.negotiation_id)

    async def _deliver_paid_orders(self) -> None:
        from croo import ListOptions

        orders = await self._client.list_orders(
            ListOptions(role="provider", agent_id=self.config.provider_agent_id, status="paid")
        )
        for order in orders:
            if order.service_id == self.config.service_id:
                await self.deliver_order(order.order_id)


def _build_croo_client(config: ProofMeshConfig) -> Any:
    if not config.croo_sdk_key:
        raise RuntimeError("CROO_API_KEY is required to run the live CROO provider")

    from croo import AgentClient, Config

    return AgentClient(
        Config(base_url=config.croo_api_url, ws_url=config.croo_ws_url),
        config.croo_sdk_key,
    )


def _event_field(event: Any, field_name: str) -> str:
    value = getattr(event, field_name, "")
    if value:
        return str(value)

    raw = getattr(event, "raw", {}) or {}
    if field_name in raw:
        return str(raw[field_name])

    camel = "".join([field_name.split("_")[0], *[part.title() for part in field_name.split("_")[1:]]])
    return str(raw.get(camel, ""))


def _object_to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return dict(value)
    return {
        key: getattr(value, key)
        for key in dir(value)
        if not key.startswith("_") and not callable(getattr(value, key))
    }
