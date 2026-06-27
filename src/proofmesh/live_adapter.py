"""Live/staging CROO readiness adapter.

This module intentionally does not fake a live CROO integration. It prepares the
configuration, service metadata, and dry-run behavior needed once credentials
and the current SDK/API surface are available.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.util import find_spec
from typing import Any

from .auditor import audit_request
from .config import ProofMeshConfig


CROO_KEY_LABEL = "CROO_API_KEY/CROO_SDK_KEY"
PROOFMESH_REPOSITORY_URL = "https://github.com/qu1nty9/CROO-AI-AGENT-Hackathon"


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    ok: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReadinessReport:
    ready: bool
    checks: list[ReadinessCheck]
    config: dict[str, object]
    service_listing: dict[str, Any]
    next_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "checks": [check.to_dict() for check in self.checks],
            "config": self.config,
            "service_listing": self.service_listing,
            "next_steps": self.next_steps,
        }


class LiveCROOAdapter:
    """Live-ready adapter boundary for future CROO SDK integration."""

    def __init__(self, config: ProofMeshConfig) -> None:
        self.config = config

    def build_service_listing(self) -> dict[str, Any]:
        return {
            "agent_name": "ProofMesh",
            "agent_id": self.config.provider_agent_id,
            "service_id": self.config.service_id,
            "service_name": "Source Coverage Audit",
            "short_description": "Paid verification and provenance audit for agent-generated outputs.",
            "tracks": ["Data & Verification Agents", "Research & Intelligence Agents"],
            "price": {
                "amount": self.config.price_croo,
                "token": self.config.payment_token,
                "unit": "per audit",
            },
            "input_schema": {
                "schema_version": "proofmesh.verification.v1",
                "required": ["artifact_type", "claims or artifact_text", "sources"],
                "audit_modes": ["source_coverage"],
            },
            "output_schema": {
                "schema_version": "proofmesh.verification.v1",
                "fields": [
                    "is_verified",
                    "overall_confidence",
                    "source_coverage",
                    "claim_audits",
                    "limitations",
                    "cap_receipt",
                ],
            },
            "repository": PROOFMESH_REPOSITORY_URL,
            "demo_video": "TBD",
        }

    def check_readiness(self) -> ReadinessReport:
        sdk_available = find_spec("croo") is not None
        checks = [
            ReadinessCheck(
                "croo_sdk_key",
                bool(self.config.croo_sdk_key),
                f"{CROO_KEY_LABEL} is set" if self.config.croo_sdk_key else f"{CROO_KEY_LABEL} is missing",
            ),
            ReadinessCheck(
                "croo_sdk_package",
                sdk_available,
                "Python module 'croo' is importable"
                if sdk_available
                else "Python module 'croo' is not installed or not discoverable",
            ),
            ReadinessCheck(
                "croo_api_url",
                self.config.croo_api_url.startswith("https://"),
                self.config.croo_api_url,
            ),
            ReadinessCheck(
                "croo_ws_url",
                self.config.croo_ws_url.startswith("wss://"),
                self.config.croo_ws_url,
            ),
            ReadinessCheck(
                "service_metadata",
                bool(self.config.service_id and self.config.provider_agent_id),
                f"service_id={self.config.service_id}; provider_agent_id={self.config.provider_agent_id}",
            ),
        ]
        ready = all(check.ok for check in checks)
        next_steps = []
        if not self.config.croo_sdk_key:
            next_steps.append("Set CROO_API_KEY from the CROO Agent dashboard; CROO_SDK_KEY is accepted as a legacy alias.")
        if not sdk_available:
            next_steps.append("Install the current CROO Python SDK with `pip install croo-sdk`.")
        if ready:
            next_steps.append("Run a staging/live negotiation and attach the transaction receipt to artifacts.")
        return ReadinessReport(
            ready=ready,
            checks=checks,
            config=self.config.to_dict(redact_secrets=True),
            service_listing=self.build_service_listing(),
            next_steps=next_steps,
        )

    def audit_dry_run(self, requirements: dict[str, Any]) -> dict[str, Any]:
        """Run ProofMesh audit with a live-ready receipt, without calling CROO."""

        report = self.check_readiness()
        payload = dict(requirements)
        payload["cap_receipt"] = {
            "mode": "live_ready_dry_run",
            "settlement_status": "not_submitted",
            "service_id": self.config.service_id,
            "provider_agent_id": self.config.provider_agent_id,
            "api_url": self.config.croo_api_url,
            "ws_url": self.config.croo_ws_url,
            "readiness_ready": report.ready,
            "note": "Dry-run only. No live CROO order or settlement was created.",
        }
        audit = audit_request(payload)
        audit["live_readiness"] = report.to_dict()
        return audit
