"""Dependency-free mock CROO CAP lifecycle for local demos and tests."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ServiceSpec:
    service_id: str
    provider_agent_id: str
    price_croo: float
    payment_token: str = "CROO"
    delivery_window_seconds: int = 300

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NegotiationRecord:
    negotiation_id: str
    service_id: str
    requester_agent_id: str
    provider_agent_id: str
    requirements: dict[str, Any]
    status: str
    price_croo: float
    payment_token: str
    created_at: str
    accepted_at: str | None = None
    reject_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OrderRecord:
    order_id: str
    negotiation_id: str
    service_id: str
    requester_agent_id: str
    provider_agent_id: str
    status: str
    price_croo: float
    payment_token: str
    created_at: str
    paid_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DeliveryRecord:
    delivery_id: str
    order_id: str
    deliverable_type: str
    deliverable_schema: dict[str, Any]
    status: str
    submitted_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LedgerEntry:
    tx_id: str
    event_type: str
    order_id: str
    negotiation_id: str
    amount_croo: float
    payment_token: str
    block_number: int
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MockCAPNetwork:
    """A minimal in-memory CAP-like network for reproducible local evidence."""

    def __init__(self, *, base_block: int = 9_000_000) -> None:
        self._block_number = base_block
        self.services: dict[str, ServiceSpec] = {}
        self.negotiations: dict[str, NegotiationRecord] = {}
        self.orders: dict[str, OrderRecord] = {}
        self.deliveries: dict[str, DeliveryRecord] = {}
        self.ledger: list[LedgerEntry] = []
        self.events: list[dict[str, Any]] = []

    def register_service(self, spec: ServiceSpec) -> None:
        self.services[spec.service_id] = spec
        self._record_event(
            "service_registered",
            {
                "service_id": spec.service_id,
                "provider_agent_id": spec.provider_agent_id,
                "price_croo": spec.price_croo,
                "payment_token": spec.payment_token,
            },
        )

    def create_negotiation(
        self,
        *,
        service_id: str,
        requester_agent_id: str,
        requirements: dict[str, Any],
    ) -> NegotiationRecord:
        service = self._require_service(service_id)
        negotiation = NegotiationRecord(
            negotiation_id=f"neg_{uuid4().hex[:10]}",
            service_id=service.service_id,
            requester_agent_id=requester_agent_id,
            provider_agent_id=service.provider_agent_id,
            requirements=requirements,
            status="pending",
            price_croo=service.price_croo,
            payment_token=service.payment_token,
            created_at=utc_now(),
        )
        self.negotiations[negotiation.negotiation_id] = negotiation
        self._record_event("negotiation_created", negotiation.to_dict())
        return negotiation

    def accept_negotiation(self, negotiation_id: str) -> OrderRecord:
        negotiation = self.get_negotiation(negotiation_id)
        if negotiation.status != "pending":
            raise ValueError(f"negotiation {negotiation_id} is not pending")

        negotiation.status = "accepted"
        negotiation.accepted_at = utc_now()
        order = OrderRecord(
            order_id=f"order_{uuid4().hex[:10]}",
            negotiation_id=negotiation.negotiation_id,
            service_id=negotiation.service_id,
            requester_agent_id=negotiation.requester_agent_id,
            provider_agent_id=negotiation.provider_agent_id,
            status="created",
            price_croo=negotiation.price_croo,
            payment_token=negotiation.payment_token,
            created_at=utc_now(),
        )
        self.orders[order.order_id] = order
        self._record_event(
            "negotiation_accepted",
            {"negotiation": negotiation.to_dict(), "order": order.to_dict()},
        )
        return order

    def reject_negotiation(self, negotiation_id: str, reason: str) -> NegotiationRecord:
        negotiation = self.get_negotiation(negotiation_id)
        if negotiation.status != "pending":
            raise ValueError(f"negotiation {negotiation_id} is not pending")
        negotiation.status = "rejected"
        negotiation.reject_reason = reason
        self._record_event("negotiation_rejected", negotiation.to_dict())
        return negotiation

    def pay_order(self, order_id: str) -> LedgerEntry:
        order = self.get_order(order_id)
        if order.status != "created":
            raise ValueError(f"order {order_id} must be created before payment")

        order.status = "paid"
        order.paid_at = utc_now()
        ledger_entry = self._append_ledger(
            event_type="order_paid",
            order_id=order.order_id,
            negotiation_id=order.negotiation_id,
            amount_croo=order.price_croo,
            payment_token=order.payment_token,
        )
        self._record_event(
            "order_paid",
            {"order": order.to_dict(), "ledger_entry": ledger_entry.to_dict()},
        )
        return ledger_entry

    def deliver_order(
        self,
        order_id: str,
        deliverable_schema: dict[str, Any],
        *,
        deliverable_type: str = "schema",
    ) -> DeliveryRecord:
        order = self.get_order(order_id)
        if order.status != "paid":
            raise ValueError(f"order {order_id} must be paid before delivery")

        delivery = DeliveryRecord(
            delivery_id=f"del_{uuid4().hex[:10]}",
            order_id=order.order_id,
            deliverable_type=deliverable_type,
            deliverable_schema=deliverable_schema,
            status="submitted",
            submitted_at=utc_now(),
        )
        self.deliveries[delivery.delivery_id] = delivery
        order.status = "completed"
        order.completed_at = delivery.submitted_at
        self._append_ledger(
            event_type="order_delivered",
            order_id=order.order_id,
            negotiation_id=order.negotiation_id,
            amount_croo=0.0,
            payment_token=order.payment_token,
        )
        self._record_event(
            "order_completed",
            {"order": order.to_dict(), "delivery": delivery.to_dict()},
        )
        return delivery

    def get_negotiation(self, negotiation_id: str) -> NegotiationRecord:
        try:
            return self.negotiations[negotiation_id]
        except KeyError as exc:
            raise KeyError(f"negotiation not found: {negotiation_id}") from exc

    def get_order(self, order_id: str) -> OrderRecord:
        try:
            return self.orders[order_id]
        except KeyError as exc:
            raise KeyError(f"order not found: {order_id}") from exc

    def get_delivery_for_order(self, order_id: str) -> DeliveryRecord:
        for delivery in self.deliveries.values():
            if delivery.order_id == order_id:
                return delivery
        raise KeyError(f"delivery not found for order: {order_id}")

    def build_cap_receipt(self, order_id: str) -> dict[str, Any]:
        order = self.get_order(order_id)
        negotiation = self.get_negotiation(order.negotiation_id)
        payment_entries = [
            entry for entry in self.ledger
            if entry.order_id == order_id and entry.event_type == "order_paid"
        ]
        payment_entry = payment_entries[-1] if payment_entries else None
        return {
            "mode": "mock_cap",
            "settlement_status": order.status,
            "service_id": order.service_id,
            "requester_agent_id": order.requester_agent_id,
            "provider_agent_id": order.provider_agent_id,
            "negotiation_id": negotiation.negotiation_id,
            "order_id": order.order_id,
            "price_croo": order.price_croo,
            "payment_token": order.payment_token,
            "payment_tx_id": payment_entry.tx_id if payment_entry else "",
            "payment_block_number": payment_entry.block_number if payment_entry else 0,
            "note": "Mock CAP receipt for local reproducibility; not a live CROO settlement.",
        }

    def export_log(self) -> dict[str, Any]:
        return {
            "network": "mock_cap",
            "services": {key: value.to_dict() for key, value in self.services.items()},
            "negotiations": {key: value.to_dict() for key, value in self.negotiations.items()},
            "orders": {key: value.to_dict() for key, value in self.orders.items()},
            "deliveries": {key: value.to_dict() for key, value in self.deliveries.items()},
            "ledger": [entry.to_dict() for entry in self.ledger],
            "events": self.events,
        }

    def _require_service(self, service_id: str) -> ServiceSpec:
        try:
            return self.services[service_id]
        except KeyError as exc:
            raise KeyError(f"service not registered: {service_id}") from exc

    def _append_ledger(
        self,
        *,
        event_type: str,
        order_id: str,
        negotiation_id: str,
        amount_croo: float,
        payment_token: str,
    ) -> LedgerEntry:
        self._block_number += 1
        entry = LedgerEntry(
            tx_id=f"0xmock{uuid4().hex[:24]}",
            event_type=event_type,
            order_id=order_id,
            negotiation_id=negotiation_id,
            amount_croo=round(amount_croo, 6),
            payment_token=payment_token,
            block_number=self._block_number,
            timestamp=utc_now(),
        )
        self.ledger.append(entry)
        return entry

    def _record_event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append(
            {
                "event_id": f"evt_{uuid4().hex[:10]}",
                "event_type": event_type,
                "timestamp": utc_now(),
                "payload": payload,
            }
        )

