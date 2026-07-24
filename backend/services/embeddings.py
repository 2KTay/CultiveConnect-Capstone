"""
Embeddings service for the RAG chat.

Loads data/regulations.json, turns each product+country entry into one
readable text chunk, embeds every chunk with a local sentence-transformers
model (all-MiniLM-L6-v2, no external API), and keeps the vectors in memory so
the /chat endpoint can retrieve the most relevant chunks by cosine similarity.
"""

import json
import os
from typing import List, Dict, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGULATIONS_FILE = os.path.join(BASE_DIR, "data", "regulations.json")

# Small, fast, fully local embedding model. First load downloads ~90 MB once.
MODEL_NAME = "all-MiniLM-L6-v2"


def load_regulations() -> dict:
    with open(REGULATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _humanize(name: str) -> str:
    # "Coffee_Green" -> "Coffee Green"
    return name.replace("_", " ").strip()


def _format_chunk(country: str, product: str, data: dict) -> str:
    """Turn one product+country regulation record into readable English text."""
    code = data.get("hts_code") or data.get("hs_code") or "not specified"
    description = data.get("hts_description") or data.get("hs_description") or ""
    base_duty = data.get("base_duty", "not specified")
    duty_notes = data.get("duty_notes", "")

    lines = []
    lines.append(f"Product: {_humanize(product)} exported to {country}.")
    lines.append(f"Tariff classification code (HTS/HS): {code}.")
    if description:
        lines.append(f"Classification description: {description}.")
    lines.append(f"Base duty rate: {base_duty}.")
    if duty_notes:
        lines.append(f"Duty notes: {duty_notes}")

    seasonal = data.get("seasonal_adjustment", {})
    if seasonal.get("applies"):
        lines.append("Seasonal tariff windows apply:")
        for window in seasonal.get("windows", []):
            period = window.get("period", "")
            subheading = window.get("subheading", "")
            duty = window.get("duty", "")
            notes = window.get("notes", "")
            window_line = f"  - During {period}: use subheading {subheading}, duty {duty}."
            if notes:
                window_line += f" {notes}"
            lines.append(window_line)
        if seasonal.get("note"):
            lines.append(f"Seasonal note: {seasonal['note']}")
    else:
        note = seasonal.get("note", "No seasonal tariff windows; duty is year-round.")
        lines.append(f"Seasonal tariff windows: none. {note}")

    required_docs = data.get("required_docs", [])
    if required_docs:
        lines.append("Required export/compliance documents: " + ", ".join(required_docs) + ".")

    sps = data.get("sps_requirements", {})
    if sps:
        authority = sps.get("authority", "")
        if authority:
            lines.append(f"Regulatory authority: {authority}.")
        lines.append(
            "Phytosanitary certificate required: "
            + ("yes" if sps.get("phytosanitary_certificate") else "no")
            + "; port of entry inspection required: "
            + ("yes" if sps.get("port_inspection") else "no")
            + "; treatment required: "
            + ("yes" if sps.get("treatment_required") else "no")
            + "."
        )
        if sps.get("systems_approach"):
            lines.append(f"Systems approach / notes: {sps['systems_approach']}")

    return "\n".join(lines)


def build_chunks() -> List[Dict]:
    """One chunk per product+country combination."""
    regulations = load_regulations()
    chunks: List[Dict] = []
    for country, products in regulations.items():
        if country == "metadata":
            continue
        if not isinstance(products, dict):
            continue
        for product, data in products.items():
            if not isinstance(data, dict):
                continue
            chunks.append(
                {
                    "id": f"{country}/{product}",
                    "country": country,
                    "product": product,
                    "text": _format_chunk(country, product, data),
                }
            )
    return chunks


class EmbeddingIndex:
    """In-memory vector index over the regulation chunks."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.chunks = build_chunks()
        texts = [c["text"] for c in self.chunks]
        # normalize so cosine similarity is a plain dot product
        self.embeddings = self.model.encode(
            texts, normalize_embeddings=True, convert_to_numpy=True
        ).astype(np.float32)

    def search(
        self, question: str, top_k: int = 5, threshold: float = 0.25
    ) -> List[Tuple[Dict, float]]:
        """Return up to top_k (chunk, score) pairs above the similarity threshold."""
        query_vec = self.model.encode(
            [question], normalize_embeddings=True, convert_to_numpy=True
        ).astype(np.float32)[0]
        scores = self.embeddings @ query_vec  # cosine similarity (vectors are normalized)
        order = np.argsort(scores)[::-1]  # highest score first
        results: List[Tuple[Dict, float]] = []
        for idx in order[:top_k]:
            score = float(scores[idx])
            if score >= threshold:
                results.append((self.chunks[idx], score))
        return results


# Lazily-built singleton so the model + embeddings are computed once at startup.
_index: Optional[EmbeddingIndex] = None


def get_index() -> EmbeddingIndex:
    global _index
    if _index is None:
        _index = EmbeddingIndex()
    return _index
