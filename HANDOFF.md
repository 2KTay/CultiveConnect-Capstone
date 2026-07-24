# CultiveConnect — Session Handoff / Context

> Purpose: let a fresh Claude Code session continue this work with zero prior context.
> Read this top-to-bottom before doing anything.

## STATUS: PART A DONE & VERIFIED. Next up = PART B (USDA investigation).

Part A (RAG /chat) is complete and verified with real curl tests. Generation now uses
**Purdue RCAC GenAI Studio** (NOT Anthropic — the user switched providers). The three A5
tests passed and were genuinely grounded in regulations.json (grapes→USA listed the exact
4 docs; asparagus→Canada gave the exact seasonal windows; bananas→Japan honestly said it
had no info instead of hallucinating). If continuing: do PART B next (see bottom).

The backend server may still be running in the background on http://localhost:8000
(uvicorn, shell id b7qtl86xf). Re-boot instructions are below if not.

## The two goals (STRICT priority order)

**PART A (must be fully working + verified before touching Part B):** a real RAG chat
`/chat` endpoint that answers export-compliance questions by (1) retrieving relevant
chunks from `backend/data/regulations.json` via local embeddings + cosine similarity,
then (2) generating an answer grounded ONLY in those retrieved chunks via the Anthropic
API. Real retrieval — NOT stuffing the whole JSON into a system prompt.

**PART B (only after Part A verified):** investigate whether a REAL, public USDA API
(FAS GATS, AMS, APHIS phytosanitary, etc.) can be called tonight (no key, or instant
key). Report findings HONESTLY first — if the good ones need multi-day key approval or
there's no genuine public endpoint, SAY SO and build nothing. Only build if genuinely
simple + real. A fake/mock "USDA integration" is worse than none. Do NOT start B until
A is done and the user has seen it working.

## Environment facts (Windows)

- Repo: `C:\Users\taemo\OneDrive\Desktop\CultiveConnect-Capstone`
- OS: Windows 11, shell is PowerShell; a Bash tool (Git Bash) is also available.
- Default `python` is **3.14.3** — torch / sentence-transformers have **NO wheels** for
  3.14. **Python 3.11 is installed** (`py -3.11`) and is what the backend venv uses.
- A **venv at `backend/venv`** was created with Python 3.11. Use
  `backend/venv/Scripts/python.exe` and `backend/venv/Scripts/uvicorn.exe`.
- No `ant` CLI, and **no `ANTHROPIC_API_KEY`** in the environment. Part A's generation
  step needs a key — see "BLOCKER" below.
- The React frontend dev server may still be running at http://localhost:5173 (Vite),
  background shell id `bd0q7gm00`. That's the standalone `frontend/src/App.jsx` app; it
  does NOT call the backend. Unrelated to Part A except for the optional A6 chat UI.

## What is DONE (all committed to disk, not to git)

- `backend/requirements.txt` — filled: fastapi, uvicorn[standard], sqlalchemy, pydantic,
  numpy, fpdf2, sentence-transformers, **requests** (anthropic REMOVED), python-dotenv.
- `backend/.env.example` / `backend/.env` — `PURDUE_GENAI_API_KEY=` and
  `PURDUE_GENAI_MODEL=llama3.1:latest`. The real key is in `backend/.env` (gitignored).
- `.gitignore` (repo root) — ignores `backend/venv/`, `.env`, `__pycache__`, node_modules.
- `backend/services/embeddings.py` — loads regulations.json, `build_chunks()` = one chunk
  per product+country as readable English text, `EmbeddingIndex` embeds all chunks with
  `all-MiniLM-L6-v2` (normalized), `search(question, top_k=5, threshold=0.25)` returns
  `[(chunk, score)]` by cosine. `get_index()` is a lazy singleton. `load_regulations()`
  helper. NOTE: `regulations.json` has top-level `metadata`, `USA`, `Canada`; products
  live under USA/Canada. Chunker skips `metadata`. Codes are `hts_code` (USA) or
  `hs_code` (Canada).
- `backend/services/rag_service.py` — `answer_question(question, top_k=5, threshold=0.25)`
  → `{"answer": str, "sources": [chunk ids]}`. Retrieves, builds context labeled
  `[Source: USA/Grapes]`, then generates via **Purdue RCAC GenAI Studio** using
  `requests.post` to `https://genai.rcac.purdue.edu/api/chat/completions` (OpenAI-compatible).
  Headers: `Authorization: Bearer {PURDUE_GENAI_API_KEY}`, `Content-Type: application/json`.
  Body: `{"model": PURDUE_GENAI_MODEL, "messages": [system, user], "stream": false}`.
  Parses `resp["choices"][0]["message"]["content"]`; raises on non-200 with status+text.
  Same grounded system prompt as before (answer ONLY from context; say clearly if not in
  context). NO anthropic import anymore. Available models list:
  `curl https://genai.rcac.purdue.edu/api/models -H "Authorization: Bearer <key>"`
  (includes llama3.1:latest, llama3.3:70b, gpt-oss:120b, qwen3:*, mistral:latest, etc.).
- `backend/routes/chat.py` — `POST /chat`, body `{question: str}`, returns
  `{answer, sources}`; 400 on empty, 500 wraps errors.
- `backend/routes/products.py` — `GET /products` lists product+country entries from JSON.
- `backend/main.py` — FastAPI app; `load_dotenv(backend/.env)` FIRST; CORS `*`; builds
  embedding index on startup; routes `/chat`, `/products`, `/health`. Run with
  `uvicorn main:app` from the `backend/` dir.
- `backend/routes/__init__.py`, `backend/services/__init__.py` — empty, make them packages.

## What is IN PROGRESS / PENDING

1. **pip install** was running in the background (`backend/venv/Scripts/python.exe -m pip
   install -r requirements.txt`) — torch is a large download. VERIFY it finished cleanly:
   ```
   backend/venv/Scripts/python.exe -m pip list | grep -iE "torch|sentence-transformers|anthropic|fastapi"
   ```
   If not present, re-run the install from `backend/`:
   ```
   ./venv/Scripts/python.exe -m pip install -r requirements.txt
   ```

2. **BLOCKER for A5 (verification):** need a real `ANTHROPIC_API_KEY`. The user was asked
   to create `backend/.env` with `ANTHROPIC_API_KEY=sk-ant-...`. Check if it exists:
   `ls backend/.env`. If missing, ask the user for it — do NOT fabricate answers.

## NEXT STEPS (do these in order)

### A2 verify (offline, NO key needed) — retrieval works
From `backend/` (first run downloads the ~90MB MiniLM model once):
```
./venv/Scripts/python.exe -c "from services.embeddings import get_index; i=get_index(); print('chunks', len(i.chunks)); [print(round(s,3), c['id']) for c,s in i.search('what documents do I need to export grapes to the USA', top_k=3)]"
```
Expect ~12 chunks and USA/Grapes ranking at/near the top. If sentence-transformers can't
reach huggingface to download the model, that's a network issue — report it; the model
name is `all-MiniLM-L6-v2`.

### Boot the API
From `backend/` (set UTF-8 so any unicode prints don't crash on Windows cp1252):
```
PYTHONUTF8=1 ./venv/Scripts/python.exe -m uvicorn main:app --port 8000
```
Run it backgrounded. Then smoke-test WITHOUT a key:
```
curl -s http://localhost:8000/health      # {"status":"ok","chunks":N}
curl -s http://localhost:8000/products    # product list
```

### A5 verify (NEEDS key in backend/.env) — the 3 required curl tests
Restart uvicorn AFTER the key file exists (dotenv loads at import). Then:
```
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"What documents do I need to export grapes to the USA?"}'
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"What is the seasonal duty window for asparagus to Canada?"}'
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"What HTS code applies to bananas exported to Japan?"}'
```
Show the user the ACTUAL request+response for each. Confirm:
- Grapes answer lists the 4 required docs (Phytosanitary Certificate, Port of Entry
  Inspection, FDA Prior Notice, FDA Food Facility Registration) and cites source USA/Grapes.
- Asparagus/Canada answer gives the seasonal windows (Oct 1–Jun 14 → 0709.20.10;
  Jun 15–Sep 30 → 0709.20.90, both Free).
- The bananas/Japan question is honestly answered "not in the provided regulations"
  (Japan isn't a destination and bananas aren't a product) — NOT hallucinated.
- `sources` are real chunk ids from regulations.json.

### A6 (optional, only if time) — minimal chat UI
Add a simple chat box component in the React frontend (`frontend/src/`) that POSTs to
`http://localhost:8000/chat` and shows `answer` + `sources`. Ugly is fine. CORS is already
`*` on the backend. The current UI entry is `frontend/src/App.jsx` (self-contained). Add a
component and mount it; keep it minimal.

## Known gotchas / decisions already made

- **Model id `claude-sonnet-4-6` is correct and current** (per the claude-api skill's model
  catalog). Do not change it. Client is zero-arg `Anthropic()` so it also works if the key
  is provided via env instead of .env.
- **Windows Unicode bug (separate from Part A):** `backend/compliance_engine.py` and
  `generate_pdf_report.py` print `→ ✓ ✗ ⚠` which crash on Windows cp1252 stdout. Run those
  with `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`. Not required for the API, but noted.
- **Data divergence (pre-existing):** the Python backend `regulations.json` and the React
  `App.jsx` embedded regs disagree (e.g. Asparagus is under BOTH USA and Canada in the
  JSON; App.jsx only has it under Canada). Not Part A's problem; don't "fix" silently.
- Namespace/imports: run uvicorn FROM `backend/` so `from services...` / `from routes...`
  resolve. `__init__.py` files exist to make them regular packages.
- FastAPI `@app.on_event("startup")` is deprecated-but-works; fine for tonight.
- `retrieval threshold=0.25` chosen so clearly-in-data queries pass and clearly-out queries
  return few/no chunks; the grounded system prompt is the real safety net for out-of-data
  questions (model told to say it lacks the info).

## Task list mirror (also tracked in the harness Task tool)

- A1 runnable env — DONE (verify install finished).
- A2 embeddings — code DONE, verify retrieval offline.
- A3 rag service — code DONE.
- A4 chat route + main — code DONE.
- A5 verify curl tests — PENDING (needs key + running server). Do NOT skip.
- A6 chat UI — optional, only if time remains.
- PART B — not started; investigate-and-report before building anything.

## How to report back to the user

Show real command output, not claims. If A5 can't run because there's no key, say so
plainly and stop there rather than inventing responses. Keep Part A green before Part B.

---

# SESSION UPDATE — frontend chat integrated + Part B findings

## Provider switched to Purdue RCAC GenAI Studio (NOT Anthropic)
Generation no longer uses the Anthropic SDK. `backend/services/rag_service.py` now does
`requests.post("https://genai.rcac.purdue.edu/api/chat/completions", ...)` with
`Authorization: Bearer {PURDUE_GENAI_API_KEY}`, body
`{"model": PURDUE_GENAI_MODEL, "messages":[system,user], "stream": false}`, parsing
`resp["choices"][0]["message"]["content"]`, raising on non-200. Config in `backend/.env`:
`PURDUE_GENAI_API_KEY=...` and `PURDUE_GENAI_MODEL=llama3.1:latest` (both also in
`.env.example`; `.env` is gitignored — the live key is NOT committed; user should rotate it
later since it was pasted in chat). `requirements.txt` dropped `anthropic`, added `requests`.
Available models: `curl https://genai.rcac.purdue.edu/api/models -H "Authorization: Bearer <key>"`.

## Part A verified working (backend), 3 grounded answers
Run from `backend/`: `PYTHONUTF8=1 ./venv/Scripts/python.exe -m uvicorn main:app --port 8000`.
`/health` → `{"status":"ok","chunks":12}`. The 3 curl tests returned genuinely grounded
answers (grapes→USA: exact 4 docs; asparagus→Canada: exact seasonal windows 0709.20.10 /
0709.20.90; bananas→Japan: honest "no info", no hallucination). FastAPI interactive page:
http://localhost:8000/docs (expand POST /chat → Try it out).

## Chat is now integrated INTO the dashboard (frontend/src/App.jsx)
Added a `ChatBox()` component (module-level, defined just above `export default function App`)
and render it once as `<ChatBox />` as a full-width card BELOW the two-column dashboard grid
(right before the max-width container closes). It uses the dashboard's own `cardStyle()` /
`inputStyle()` helpers so it matches the theme. It: takes a question, POSTs to
`http://localhost:8000/chat`, shows a loading state, the answer, a plain error on failure,
and a "Sources: ..." line. Backend CORS is `*` so the cross-origin call works. Frontend still
starts the SAME way: `cd frontend && npm run dev` → http://localhost:5173/ (Vite). The edits
to App.jsx are purely additive (component + one render line); existing dashboard logic
untouched; Vite HMR compiled with no errors; PDF button target (`/Compliance_Gap_Report.pdf`)
still serves 200.

## IMPORTANT verification caveat (browser tools)
The Chrome/browser-automation extension was DECLINED earlier this session, so this session
could NOT click the page or screenshot it. Everything was verified programmatically (backend
health, the 3 grounded responses, the frontend serving the integrated panel with no compile
error). The final on-screen click is the user's to do (open http://localhost:5173/, scroll to
the "Compliance AI Assistant" card, ask the 3 questions). If a future session HAS browser
tools, use `/chrome` then the `claude-in-chrome` skill to drive it and screenshot for a true
visual confirm.

## How to run the whole thing (fresh session)
1. Backend: `cd backend && PYTHONUTF8=1 ./venv/Scripts/python.exe -m uvicorn main:app --port 8000`
   (venv is Python 3.11 at backend/venv; already has all deps). Confirm `/health`.
   Needs `backend/.env` with PURDUE_GENAI_API_KEY (present locally; NOT in git).
2. Frontend: `cd frontend && npm run dev` → open http://localhost:5173/.
3. Scroll to the "Compliance AI Assistant" card at the bottom of the dashboard; ask questions.

## PART B (USDA API) — investigated, NOT built, awaiting user "go"
- **APHIS PExD/PCIT** (phytosanitary import requirements by commodity+country) = the perfect
  fit, but NO public API — login-gated (eAuth). Not callable tonight.
- **USDA FAS Open Data API** = REAL and callable now. Base `https://api.fas.usda.gov/api/...`,
  fronted by api.data.gov, auth via `?api_key=...`. `DEMO_KEY` works for testing; a personal
  key is instant self-service at api.data.gov/signup (no multi-day approval). Verified live
  (HTTP 200 JSON): `.../api/esr/commodities?api_key=DEMO_KEY`,
  `.../api/esr/countries?api_key=DEMO_KEY`,
  `.../api/esr/exports/commodityCode/104/allCountries/marketYear/2024?api_key=DEMO_KEY`,
  `.../api/gats/commodities?api_key=DEMO_KEY`.
- CAVEAT: ESR has only 44 bulk commodities (wheat/corn/soy/cotton/meats) — NONE of
  CultiveConnect's products (grapes/asparagus/coffee/quinoa/blueberries). GATS is the on-topic
  one (keyed by HS codes, covers fruits, trade values by country) but returns trade STATISTICS,
  not compliance REQUIREMENTS. So any build should be a clearly-labeled "live USDA trade data"
  widget next to the regulations — NOT a "USDA compliance" feed. Do NOT build until user says go.

## Latest user prompt (verbatim) — what they asked for this round
> The frontend is already running at http://localhost:5173/ ... I want the RAG chat added
> directly INTO this same dashboard, live ... STEP 1 confirm backend up; STEP 2 add a chat
> panel directly into App.jsx on the same dashboard view (keep existing style; text input +
> submit "Ask about compliance requirements...", POST /chat with {question}, display answer +
> sources labeled, loading state, plain error on failure); STEP 3 hot-reload/verify live in
> browser with the 3 questions; STEP 4 confirm product selection / gap analysis / PDF button
> still work; report yes/no with what was actually seen. Also: give context md with the new
> prompt so the next AI knows everything, and commit to GitHub so the other AI can see changes.

This session did STEP 1 (backend up), STEP 2 (panel integrated + styled), verified frontend
serves it with no compile error, and COMMITTED to GitHub. STEP 3/4 visual click is pending on
the user (no browser tools this session).
