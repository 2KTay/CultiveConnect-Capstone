"""
RAG service: retrieve relevant regulation chunks, then generate an answer with
Purdue's RCAC GenAI Studio API grounded strictly in that retrieved context.

Generation uses the GenAI Studio OpenAI-compatible chat completions endpoint
(https://genai.rcac.purdue.edu/api/chat/completions) via plain HTTP.
"""

import os
from typing import List, Dict

import requests

from services.embeddings import get_index

# Purdue RCAC GenAI Studio config (loaded from backend/.env by main.py).
GENAI_URL = "https://genai.rcac.purdue.edu/api/chat/completions"
DEFAULT_MODEL = "llama3.1:latest"

SYSTEM_PROMPT = (
    "You are CultiveConnect's export-compliance assistant. You help Latin American "
    "agricultural producers understand export requirements for the USA and Canada.\n\n"
    "Answer the user's question using ONLY the regulation context provided in the user "
    "message. Follow these rules strictly:\n"
    "- Base every fact (HTS/HS codes, duty rates, seasonal windows, required documents, "
    "authorities) only on the provided context. Never invent or guess these values.\n"
    "- If the answer is not contained in the provided context, say clearly that you do not "
    "have that information in the current regulations data. Do not make it up.\n"
    "- Be concise and practical. When relevant, name the specific documents, codes, or "
    "seasonal windows from the context.\n"
    "- The context is the source of truth; do not rely on outside knowledge of tariffs."
)


def _build_context(matches: List) -> str:
    if not matches:
        return "(No relevant regulation entries were found for this question.)"
    blocks = []
    for chunk, score in matches:
        blocks.append(f"[Source: {chunk['id']}]\n{chunk['text']}")
    return "\n\n".join(blocks)


def _generate(system_prompt: str, user_content: str) -> str:
    """Call the Purdue GenAI Studio chat completions endpoint (non-streaming)."""
    api_key = os.environ.get("PURDUE_GENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "PURDUE_GENAI_API_KEY is not set. Add it to backend/.env "
            "(see backend/.env.example)."
        )
    model = os.environ.get("PURDUE_GENAI_MODEL", DEFAULT_MODEL)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "stream": False,
    }

    response = requests.post(GENAI_URL, headers=headers, json=body, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(
            f"Purdue GenAI request failed: {response.status_code} {response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def answer_question(question: str, top_k: int = 5, threshold: float = 0.25) -> Dict:
    """Retrieve relevant chunks and generate a grounded answer.

    Returns {"answer": str, "sources": [chunk ids used]}.
    """
    index = get_index()
    matches = index.search(question, top_k=top_k, threshold=threshold)
    context = _build_context(matches)
    sources = [chunk["id"] for chunk, _score in matches]

    user_content = (
        f"Regulation context:\n\n{context}\n\n"
        f"---\n"
        f"Question: {question}\n\n"
        f"Answer using only the regulation context above."
    )

    answer = _generate(SYSTEM_PROMPT, user_content)
    return {"answer": answer, "sources": sources}
