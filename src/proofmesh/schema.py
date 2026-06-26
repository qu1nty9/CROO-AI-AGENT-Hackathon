"""Runtime schema helpers for ProofMesh request and response payloads."""

from __future__ import annotations

from typing import Any


SCHEMA_VERSION = "proofmesh.verification.v1"
SUPPORTED_AUDIT_MODES = {"source_coverage"}


class RequestValidationError(ValueError):
    """Raised when a ProofMesh verification request is malformed."""


def normalize_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a ProofMesh verification request."""

    if not isinstance(payload, dict):
        raise RequestValidationError("request payload must be a JSON object")

    audit_mode = str(payload.get("audit_mode") or "source_coverage")
    if audit_mode not in SUPPORTED_AUDIT_MODES:
        allowed = ", ".join(sorted(SUPPORTED_AUDIT_MODES))
        raise RequestValidationError(f"unsupported audit_mode '{audit_mode}'; supported: {allowed}")

    claims = _normalize_claims(payload.get("claims", []))
    artifact_text = str(payload.get("artifact_text") or "")
    if not claims and not artifact_text.strip():
        raise RequestValidationError("request must include either non-empty claims or artifact_text")

    return {
        "schema_version": str(payload.get("schema_version") or SCHEMA_VERSION),
        "task_id": _string_field(payload, "task_id", default="unknown"),
        "artifact_type": _string_field(payload, "artifact_type", default="unknown"),
        "artifact_text": artifact_text,
        "claims": claims,
        "sources": _normalize_sources(payload.get("sources", [])),
        "audit_mode": audit_mode,
        "max_latency_seconds": payload.get("max_latency_seconds"),
        "max_price_croo": payload.get("max_price_croo"),
        "cap_receipt": payload.get("cap_receipt"),
    }


def default_cap_receipt() -> dict[str, str]:
    """Return the local-mode CAP receipt used before mock/live CAP is attached."""

    return {
        "mode": "local",
        "settlement_status": "not_settled",
        "note": "No live CAP settlement attached to this local audit.",
    }


def _string_field(payload: dict[str, Any], field_name: str, *, default: str) -> str:
    value = payload.get(field_name)
    if value is None or str(value).strip() == "":
        return default
    return str(value)


def _normalize_claims(raw_claims: Any) -> list[dict[str, Any]]:
    if raw_claims in (None, ""):
        return []
    if not isinstance(raw_claims, list):
        raise RequestValidationError("claims must be a list when provided")

    normalized = []
    for index, claim in enumerate(raw_claims, start=1):
        if isinstance(claim, str):
            text = claim.strip()
            if text:
                normalized.append({"id": f"c{index}", "text": text, "source_ids": []})
            continue

        if not isinstance(claim, dict):
            raise RequestValidationError(f"claim #{index} must be a string or object")

        text = str(claim.get("text") or "").strip()
        if not text:
            raise RequestValidationError(f"claim #{index} is missing non-empty text")

        source_ids = claim.get("source_ids") or []
        if not isinstance(source_ids, list):
            raise RequestValidationError(f"claim #{index} source_ids must be a list")

        normalized.append(
            {
                "id": str(claim.get("id") or f"c{index}"),
                "text": text,
                "source_ids": [str(source_id) for source_id in source_ids],
            }
        )

    return normalized


def _normalize_sources(raw_sources: Any) -> list[dict[str, str]]:
    if raw_sources in (None, ""):
        return []
    if not isinstance(raw_sources, list):
        raise RequestValidationError("sources must be a list when provided")

    normalized = []
    for index, source in enumerate(raw_sources, start=1):
        if not isinstance(source, dict):
            raise RequestValidationError(f"source #{index} must be an object")

        text = source.get("text") or source.get("excerpt") or source.get("content") or ""
        normalized.append(
            {
                "id": str(source.get("id") or f"s{index}"),
                "title": str(source.get("title") or ""),
                "url": str(source.get("url") or ""),
                "text": str(text),
            }
        )

    return normalized

