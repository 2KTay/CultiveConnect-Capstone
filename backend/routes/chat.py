"""POST /chat — RAG question answering over the regulations data."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from services.rag_service import answer_question

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = (request.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="question must not be empty")
    try:
        result = answer_question(question)
    except Exception as exc:  # surface generation/config errors to the client
        raise HTTPException(status_code=500, detail=f"chat failed: {exc}")
    return result
