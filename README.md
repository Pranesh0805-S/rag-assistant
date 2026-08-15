# DocuMind — Multi-Document RAG Assistant with Citations

DocuMind is a full-stack web application where a user uploads multiple PDF documents and asks questions in plain English. The system retrieves the most relevant text across *all* of that user's uploaded documents, sends it to Claude, and returns an answer that **cites exactly which document and page it came from** — not just a generic "chat with your PDF" clone.

**What makes this different from a basic PDF-chat clone:** multi-document synthesis, page-level citation grounding, and a hand-written evaluation set with a documented accuracy score — the three things that demonstrate real retrieval engineering rather than "I called an API."

---

## Live Deployment
- Frontend: _add Vercel URL once Phase 6 is finalized_
- Backend API docs: _add Render URL + `/docs` once Phase 6 is finalized_

## Eval Accuracy
_Add the scored result here once the 15–20 question eval set is complete (e.g., "16/18 correct with correct citation")._

---

## Tech Stack
| Layer | Tool |
|---|---|
| Backend | FastAPI (Python), Uvicorn |
| Frontend | React + Vite |
| Database | MongoDB (Atlas in production) |
| Vector store | ChromaDB |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| LLM | Anthropic Claude API |
| PDF parsing | PyMuPDF |
| Auth | JWT + bcrypt, Gmail SMTP OTP email verification |
| Deployment | Render (backend), Vercel (frontend) |

## Architecture
```
React/Vite Frontend --HTTPS--> FastAPI Backend --> MongoDB Atlas (users, doc metadata, chunks)
                                     |
                                     --> ChromaDB (per-user scoped vector store)
                                     |
                                     --> Claude API (generation)
                                     |
                                     --> Gmail SMTP (OTP email)
```

## Core Features
1. Auth — signup, OTP email verification, JWT login.
2. Upload — PDF-only, validated by extension + size + MIME/magic bytes.
3. Chunking — ~500-token chunks with 50-token overlap (`tiktoken`, `cl100k_base`).
4. Embedding + storage — `all-MiniLM-L6-v2`, per-user isolation in ChromaDB.
5. Retrieval — top-k relevant chunks, scoped strictly to the requesting user's documents.
6. Generation — Claude answers grounded in retrieved chunks, returning structured JSON.
7. Citations — every answer is paired with document name + page number.
8. Eval set — 15–20 hand-written Q&A pairs scored for accuracy and citation correctness.

## Security
- API keys live only in backend `.env`, never in frontend code or git history.
- Every upload/chat/retrieval endpoint requires a valid JWT.
- **Data isolation:** a user can never retrieve or query another user's documents — every database and vector-store query is scoped server-side by the authenticated user's ID, never a client-supplied value.
- PDF uploads validated by extension, size limit, and MIME/magic bytes (not extension alone).
- CORS restricted to the actual frontend domain, never `*`.
- Full checklist and rationale in the project spec.

## Known Limitations
Free-tier hosting introduces real, documented constraints — see [`KNOWN_LIMITATIONS.md`](./KNOWN_LIMITATIONS.md) for an honest breakdown, including the Render 512MB memory ceiling and the fix that was applied (lazy-loading the embedding model).

## Roadmap
The full feature roadmap — multi-model AI switching, chat history, drag-and-drop upload, inline PDF preview, exportable transcripts, an eval dashboard, OAuth logins, optional authenticator-app 2FA, and web-search augmentation — is documented in [`FUTURE_WORK.md`](./FUTURE_WORK.md).

## Project Documentation
| Document | Purpose |
|---|---|
| [`1-PRD-Product-Requirements.md`](./1-PRD-Product-Requirements.md) | Product goals, use cases, functional requirements |
| [`2-TRD-Technical-Requirements.md`](./2-TRD-Technical-Requirements.md) | Architecture, tech stack, pipeline internals |
| [`3-App-Flow-User-Journey.md`](./3-App-Flow-User-Journey.md) | End-to-end user journey and edge cases |
| [`4-UI-UX-Design-Brief.md`](./4-UI-UX-Design-Brief.md) | Design system, key screens, interaction principles |
| [`5-Backend-Schema-Data-Auth.md`](./5-Backend-Schema-Data-Auth.md) | Database schemas, auth flow, data isolation guarantee |
| [`6-Implementation-Plan-Build-Order.md`](./6-Implementation-Plan-Build-Order.md) | Phase-by-phase build status and next steps |
| [`KNOWN_LIMITATIONS.md`](./KNOWN_LIMITATIONS.md) | Honest write-up of current infrastructure constraints |
| [`FUTURE_WORK.md`](./FUTURE_WORK.md) | Full long-term feature roadmap |

## What "Done" Looks Like
- Deployed, working link (not just localhost).
- README with architecture, tech stack, eval accuracy number, and a security section.
- 2–3 sentences ready for an interview: retrieval strategy used, why chunking was done this way, and a real bug/failure mode hit and fixed along the way (e.g., the Render free-tier OOM and the lazy-loading fix).
