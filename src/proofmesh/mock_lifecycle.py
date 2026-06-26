"""Reusable mock CAP lifecycle orchestration for demos and tests."""

from __future__ import annotations

from typing import Any

from .cap_mock import MockCAPNetwork
from .provider import PROOFMESH_SERVICE_ID, ProofMeshProvider


DEFAULT_REQUESTER_AGENT_ID = "cap://research-requester.local"


def run_mock_cap_lifecycle(
    requirements: dict[str, Any],
    *,
    requester_agent_id: str = DEFAULT_REQUESTER_AGENT_ID,
) -> dict[str, Any]:
    """Run one local requester/provider/payment/delivery lifecycle."""

    network = MockCAPNetwork()
    provider = ProofMeshProvider(network)

    negotiation = network.create_negotiation(
        service_id=PROOFMESH_SERVICE_ID,
        requester_agent_id=requester_agent_id,
        requirements=requirements,
    )
    order = provider.handle_negotiation_created(negotiation.negotiation_id)
    payment_entry = network.pay_order(order.order_id)
    delivery = provider.handle_order_paid(order.order_id)
    completed_order = network.get_order(order.order_id)
    audit_report = delivery.deliverable_schema

    return {
        "demo_name": "proofmesh_mock_cap_lifecycle",
        "requester_agent_id": requester_agent_id,
        "provider_agent_id": provider.service_spec.provider_agent_id,
        "service_id": provider.service_spec.service_id,
        "lifecycle_summary": {
            "negotiation_id": negotiation.negotiation_id,
            "order_id": order.order_id,
            "delivery_id": delivery.delivery_id,
            "payment_tx_id": payment_entry.tx_id,
            "payment_block_number": payment_entry.block_number,
            "final_order_status": completed_order.status,
            "audit_is_verified": audit_report["is_verified"],
            "audit_overall_confidence": audit_report["overall_confidence"],
        },
        "delivered_audit": audit_report,
        "network_log": network.export_log(),
    }


def summarize_lifecycle(demo: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, writeup-friendly summary of a lifecycle demo."""

    audit = demo["delivered_audit"]
    coverage = audit["source_coverage"]
    ledger = demo["network_log"]["ledger"]
    paid_amount = sum(entry["amount_croo"] for entry in ledger if entry["event_type"] == "order_paid")
    return {
        "task_id": audit["task_id"],
        "service_id": demo["service_id"],
        "requester_agent_id": demo["requester_agent_id"],
        "provider_agent_id": demo["provider_agent_id"],
        "order_status": demo["lifecycle_summary"]["final_order_status"],
        "is_verified": audit["is_verified"],
        "overall_confidence": audit["overall_confidence"],
        "claims_total": coverage["claims_total"],
        "claims_supported": coverage["claims_supported"],
        "claims_unsupported": coverage["claims_unsupported"],
        "claims_contradicted": coverage["claims_contradicted"],
        "paid_amount_croo": round(paid_amount, 6),
        "event_types": [event["event_type"] for event in demo["network_log"]["events"]],
        "ledger_event_types": [entry["event_type"] for entry in ledger],
        "receipt_mode": audit["cap_receipt"]["mode"],
    }

