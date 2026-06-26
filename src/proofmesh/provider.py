"""ProofMesh provider wrapper for mock CAP and future live CAP adapters."""

from __future__ import annotations

from typing import Any

from .auditor import audit_request
from .cap_mock import DeliveryRecord, MockCAPNetwork, OrderRecord, ServiceSpec
from .schema import RequestValidationError


PROOFMESH_SERVICE_ID = "proofmesh-source-coverage-audit"
PROOFMESH_PROVIDER_AGENT_ID = "cap://proofmesh-provider.local"


class ProofMeshProvider:
    """Provider agent that accepts paid audit jobs and delivers ProofMesh reports."""

    def __init__(
        self,
        network: MockCAPNetwork,
        *,
        service_id: str = PROOFMESH_SERVICE_ID,
        provider_agent_id: str = PROOFMESH_PROVIDER_AGENT_ID,
        price_croo: float = 0.25,
    ) -> None:
        self.network = network
        self.service_spec = ServiceSpec(
            service_id=service_id,
            provider_agent_id=provider_agent_id,
            price_croo=price_croo,
        )
        self.network.register_service(self.service_spec)

    def handle_negotiation_created(self, negotiation_id: str) -> OrderRecord:
        negotiation = self.network.get_negotiation(negotiation_id)
        if negotiation.service_id != self.service_spec.service_id:
            return self.network.reject_negotiation(
                negotiation_id,
                f"unsupported service_id: {negotiation.service_id}",
            )
        return self.network.accept_negotiation(negotiation_id)

    def handle_order_paid(self, order_id: str) -> DeliveryRecord:
        order = self.network.get_order(order_id)
        if order.service_id != self.service_spec.service_id:
            raise ValueError(f"unsupported service_id: {order.service_id}")

        negotiation = self.network.get_negotiation(order.negotiation_id)
        requirements = dict(negotiation.requirements)
        requirements["cap_receipt"] = self.network.build_cap_receipt(order_id)

        try:
            audit_report = audit_request(requirements)
        except RequestValidationError as exc:
            audit_report = _invalid_request_report(
                order_id=order_id,
                requirements=requirements,
                error=str(exc),
            )

        return self.network.deliver_order(order_id, audit_report)


def _invalid_request_report(
    *,
    order_id: str,
    requirements: dict[str, Any],
    error: str,
) -> dict[str, Any]:
    return {
        "schema_version": "proofmesh.verification.v1",
        "task_id": str(requirements.get("task_id") or "unknown"),
        "artifact_type": str(requirements.get("artifact_type") or "unknown"),
        "audit_mode": str(requirements.get("audit_mode") or "source_coverage"),
        "is_verified": False,
        "overall_confidence": 0.0,
        "source_coverage": {
            "claims_total": 0,
            "claims_supported": 0,
            "claims_partial": 0,
            "claims_contradicted": 0,
            "claims_unsupported": 0,
            "sources_total": 0,
        },
        "claim_audits": [],
        "limitations": [
            "The provider could not execute the audit because the request failed schema validation.",
            error,
        ],
        "cap_receipt": requirements.get("cap_receipt") or {
            "mode": "mock_cap",
            "settlement_status": "paid",
            "order_id": order_id,
        },
    }

