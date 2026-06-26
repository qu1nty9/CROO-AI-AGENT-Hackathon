"""Environment-backed configuration for ProofMesh deployment modes."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Mapping

from .provider import PROOFMESH_SERVICE_ID


@dataclass(frozen=True)
class ProofMeshConfig:
    mode: str
    croo_api_url: str
    croo_ws_url: str
    croo_sdk_key: str
    service_id: str
    provider_agent_id: str
    price_croo: float
    payment_token: str

    def to_dict(self, *, redact_secrets: bool = True) -> dict[str, object]:
        data = asdict(self)
        if redact_secrets and data["croo_sdk_key"]:
            data["croo_sdk_key"] = "***redacted***"
        return data


def load_config(environ: Mapping[str, str] | None = None) -> ProofMeshConfig:
    env = environ or os.environ
    return ProofMeshConfig(
        mode=env.get("PROOFMESH_MODE", "local"),
        croo_api_url=env.get("CROO_API_URL", "https://api.croo.network"),
        croo_ws_url=env.get("CROO_WS_URL", "wss://api.croo.network/ws"),
        croo_sdk_key=env.get("CROO_SDK_KEY", ""),
        service_id=env.get("PROOFMESH_SERVICE_ID", PROOFMESH_SERVICE_ID),
        provider_agent_id=env.get("PROOFMESH_PROVIDER_AGENT_ID", "cap://proofmesh-provider.local"),
        price_croo=float(env.get("PROOFMESH_PRICE_CROO", "0.25")),
        payment_token=env.get("PROOFMESH_PAYMENT_TOKEN", "CROO"),
    )

