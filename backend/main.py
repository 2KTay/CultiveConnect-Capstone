"""
CultiveConnect API.

Serves the RAG chat over the compliance regulations data, plus a small
products listing. Run from the backend/ directory with:

    uvicorn main:app --reload
"""

import os

from dotenv import load_dotenv

# Load ANTHROPIC_API_KEY (and anything else) from backend/.env before importing
# anything that constructs an Anthropic client.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import chat, products
from services.embeddings import get_index

app = FastAPI(title="CultiveConnect API", version="1.0")

# Allow the Vite dev server (and others, for local dev) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def build_index_on_startup():
    # Build the embedding index once at startup so the first /chat call is fast.
    index = get_index()
    print(f"[startup] Embedding index ready: {len(index.chunks)} regulation chunks.")


@app.get("/health")
def health():
    index = get_index()
    return {"status": "ok", "chunks": len(index.chunks)}


app.include_router(chat.router)
app.include_router(products.router)
