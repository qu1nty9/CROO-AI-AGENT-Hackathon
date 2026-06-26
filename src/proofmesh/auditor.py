"""Deterministic verification core for the ProofMesh MVP.

The first version is intentionally transparent and dependency-free. It does not
claim semantic truth verification. It checks whether claims have source coverage,
lexical support, and obvious local contradiction markers.
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any

from .schema import SCHEMA_VERSION, default_cap_receipt, normalize_request


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "with",
}

NEGATION_TERMS = {"no", "not", "never", "none", "without", "false", "incorrect"}


def audit_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Audit a structured verification request and return a JSON-serializable report."""

    request = normalize_request(payload)
    claims = _claims_from_request(request)
    sources = request["sources"]
    source_by_id = {source["id"]: source for source in sources}

    claim_audits = [
        _audit_claim(claim, sources=sources, source_by_id=source_by_id)
        for claim in claims
    ]

    supported = sum(1 for item in claim_audits if item["status"] == "supported")
    partial = sum(1 for item in claim_audits if item["status"] == "partial")
    contradicted = sum(1 for item in claim_audits if item["status"] == "contradicted")
    total = len(claim_audits)

    if total == 0:
        overall_confidence = 0.0
    else:
        overall_confidence = round(
            max(0.0, min(1.0, (supported + 0.5 * partial - contradicted) / total)),
            3,
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": request["task_id"],
        "artifact_type": request["artifact_type"],
        "audit_mode": request["audit_mode"],
        "is_verified": total > 0 and supported == total and contradicted == 0,
        "overall_confidence": overall_confidence,
        "source_coverage": {
            "claims_total": total,
            "claims_supported": supported,
            "claims_partial": partial,
            "claims_contradicted": contradicted,
            "claims_unsupported": sum(1 for item in claim_audits if item["status"] == "unsupported"),
            "sources_total": len(sources),
        },
        "claim_audits": claim_audits,
        "limitations": [
            "This MVP performs transparent lexical and source-coverage checks.",
            "It is not a guarantee of factual truth.",
            "Semantic verification, web retrieval, and human calibration are future work.",
        ],
        "cap_receipt": request["cap_receipt"] or default_cap_receipt(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def _audit_claim(
    claim: dict[str, Any],
    *,
    sources: list[dict[str, str]],
    source_by_id: dict[str, dict[str, str]],
) -> dict[str, Any]:
    claim_tokens = _tokens(claim["text"])
    requested_ids = claim.get("source_ids") or []

    candidate_sources = (
        [source_by_id[source_id] for source_id in requested_ids if source_id in source_by_id]
        if requested_ids
        else sources
    )

    scored_sources = []
    contradiction_hits = []
    for source in candidate_sources:
        source_tokens = _tokens(source.get("text", ""))
        overlap = _weighted_overlap(claim_tokens, source_tokens)
        negation_mismatch = _has_negation_mismatch(claim["text"], source.get("text", ""))

        if overlap > 0:
            scored_sources.append(
                {
                    "source_id": source["id"],
                    "title": source.get("title", ""),
                    "url": source.get("url", ""),
                    "support_score": round(overlap, 3),
                }
            )
        if negation_mismatch and overlap >= 0.25:
            contradiction_hits.append(source["id"])

    scored_sources.sort(key=lambda item: item["support_score"], reverse=True)
    best_score = scored_sources[0]["support_score"] if scored_sources else 0.0

    if contradiction_hits:
        status = "contradicted"
        confidence = max(0.0, round(0.35 - min(best_score, 0.25), 3))
    elif best_score >= 0.55:
        status = "supported"
        confidence = round(min(0.95, 0.55 + best_score * 0.4), 3)
    elif best_score >= 0.25:
        status = "partial"
        confidence = round(0.35 + best_score * 0.5, 3)
    else:
        status = "unsupported"
        confidence = 0.1 if sources else 0.0

    return {
        "claim_id": claim["id"],
        "claim": claim["text"],
        "status": status,
        "confidence": confidence,
        "supporting_sources": scored_sources[:3],
        "contradiction_sources": contradiction_hits,
        "notes": _claim_notes(status, requested_ids, scored_sources, contradiction_hits),
    }


def _claims_from_request(request: dict[str, Any]) -> list[dict[str, Any]]:
    if request["claims"]:
        return request["claims"]

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", request["artifact_text"])
        if len(sentence.strip().split()) >= 5
    ]
    return [{"id": f"c{index}", "text": sentence, "source_ids": []} for index, sentence in enumerate(sentences, start=1)]


def _tokens(text: str) -> Counter[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return Counter(word for word in words if word not in STOPWORDS and len(word) > 2)


def _weighted_overlap(claim_tokens: Counter[str], source_tokens: Counter[str]) -> float:
    if not claim_tokens or not source_tokens:
        return 0.0
    shared = sum(min(count, source_tokens[token]) for token, count in claim_tokens.items())
    total = sum(claim_tokens.values())
    return shared / total


def _has_negation_mismatch(claim_text: str, source_text: str) -> bool:
    claim_terms = set(_tokens(claim_text))
    source_terms = set(_tokens(source_text))
    shared = claim_terms & source_terms
    if len(shared) < 2:
        return False

    claim_has_negation = bool(set(re.findall(r"[a-z0-9]+", claim_text.lower())) & NEGATION_TERMS)
    source_has_negation = bool(set(re.findall(r"[a-z0-9]+", source_text.lower())) & NEGATION_TERMS)
    return claim_has_negation != source_has_negation


def _claim_notes(
    status: str,
    requested_ids: list[str],
    scored_sources: list[dict[str, Any]],
    contradiction_hits: list[str],
) -> list[str]:
    notes = []
    if requested_ids and not scored_sources:
        notes.append("Requested source ids were missing or had no lexical support.")
    if status == "unsupported":
        notes.append("No source reached the minimum lexical support threshold.")
    if status == "partial":
        notes.append("Some source overlap exists, but it is below the support threshold.")
    if contradiction_hits:
        notes.append("Potential negation mismatch detected in overlapping source text.")
    if not notes:
        notes.append("Claim has source coverage under the MVP scoring rule.")
    return notes
