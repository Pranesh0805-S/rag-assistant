# TRD — DocuMind Technical Requirements

## 1. Architecture Overview
```
[React/Vite Frontend] --HTTPS--> [FastAPI Backend] --> [MongoDB Atlas]  (users, doc metadata, chunks)
                                        |
                                        --> [ChromaDB]      (vector store, per-user scoped)
                                        |
                                        --> [Claude API]     (generation)
                                        |
                                        --> [Gmail SMTP]     (OTP email verification)

Backend deployed on Render. Frontend deployed on Vercel.
```

## 2. Tech Stack
| Layer | Technology |
|---|---|
| Backend framework | FastAPI (Python), Uvicorn |
| Frontend framework | React + Vite |
| Database (metadata) | MongoDB (Atlas in production) |
| Vector store | ChromaDB |
| Embedding model | `sentence-transformers` — `all-MiniLM-L6-v2` (384-dim) |
| LLM (generation) | Anthropic Claude API |
| PDF parsing | PyMuPDF (`fitz`) |
| MIME validation | `python-magic` (Linux) / `python-magic-bin` (Windows dev only) |
| Chunking | `tiktoken` (`cl100k_base` encoding) |
| Auth | JWT (HTTPBearer) + bcrypt password hashing |
| Email/OTP | Gmail SMTP |
| Backend hosting | Render (free tier) |
| Frontend hosting | Vercel |

## 3. Backend Structure
```
backend/
  main.py                # FastAPI app instance (app = FastAPI()) lives here
  app/
    routers/              # route handlers (auth, documents, ask, etc.)
    services/              # business logic (embedding, chunking, retrieval, generation)
    core/
      config.py            # pydantic-settings configuration
      database.py           # MongoDB connection
      security.py           # JWT + bcrypt helpers
      deps.py               # FastAPI dependencies (auth guard, etc.)
      otp.py                # OTP generation/verification logic
    models/                # Pydantic schemas / data models
```
Start command: `uvicorn main:app` (not `app.main:app`) — `app = FastAPI()` is defined in top-level `backend/main.py`, while `app/` is the routers/services subfolder.

## 4. Document Processing Pipeline
1. **Validation:** file extension check → file size check → MIME/magic-byte check → PyMuPDF open-and-parse check. Reject at the earliest failing stage.
2. **Text extraction:** PyMuPDF extracts text per page, preserving page numbers.
3. **Chunking:** `tiktoken` (`cl100k_base`) splits text into ~500-token chunks with 50-token overlap.
4. **Storage:** each chunk stored in MongoDB `chunks` collection with `doc_id`, `owner_id`, `page_number`, `chunk_index`, `text`, and also embedded and stored in ChromaDB with `user_id` metadata for retrieval-time filtering.

## 5. Retrieval & Generation Pipeline
1. User submits a question via `/documents/ask`.
2. Question is embedded with the same `all-MiniLM-L6-v2` model.
3. ChromaDB is queried for top-k nearest chunks, filtered by `user_id` metadata so no cross-user leakage is possible.
4. Retrieved chunks + question are sent to Claude with a strict-JSON response contract: `{"answer": ..., "used_chunks": [...]}`.
5. `used_chunks` indices are mapped back to `doc_id` / `filename` / `page_number` to build the citation list returned to the frontend.

## 6. Non-Functional Requirements
| Category | Requirement |
|---|---|
| Security | Per-user data isolation enforced server-side on every Chroma query and DB lookup; JWT required on every protected endpoint |
| Performance | Free-tier constraint: embedding model must be lazy-loaded (not loaded at import time) to avoid OOM on 512MB RAM |
| Reliability | Distinguish auth failures (expired JWT → re-auth) from actual bugs during testing |
| Portability | `requirements.txt` must be project-specific (fresh venv, direct deps only — no global-venv pollution) |
| Compatibility | `python-magic-bin` is Windows-only; production (Render/Linux) requires plain `python-magic` |
| CORS | Explicit `CORSMiddleware` allow-list — Vite dev origin locally, Vercel domain in production; never `*` |

## 7. Environment & Config
- `.env` holds all secrets (Claude API key, Mongo URI, JWT secret, SMTP credentials) — never committed, `.gitignore`'d from commit #1.
- Separate `.env` values for local dev vs production; production DB credentials never reused locally.
- `pydantic-settings` config class defines exact casing for all settings — must match usage exactly (e.g., `settings.MONGO_URI` vs `settings.mongo_uri` is a real bug class encountered in this project).

## 8. Known Technical Risks
- Render free-tier 512MB RAM ceiling vs. `torch` + `sentence-transformers` + `chromadb` combined footprint — mitigated via lazy model loading, but cold-start OOM is still possible under load. See `KNOWN_LIMITATIONS.md`.
- Gmail SMTP has practical limits/blocks on some free hosting egress — relevant to OTP delivery reliability in production.
