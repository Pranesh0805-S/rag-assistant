# Implementation Plan — Build Order

Status legend: ✅ complete · 🔄 in progress · ⬜ not started

## Phase 0 — Scaffolding ✅
- Repo initialized, pushed to GitHub.
- Backend health endpoint.
- ChromaDB wired up locally.
- `pydantic-settings` config in place.

## Phase 1 — Auth ✅
- Signup endpoint (bcrypt password hashing).
- Gmail SMTP OTP email verification.
- Login endpoint issuing JWT.
- JWT-protected routes via `HTTPBearer` dependency.
- `/auth/me` tested and working.
- Pushed to GitHub.

## Phase 2 — Document Upload ✅
- PDF validation pipeline: extension → size → magic-byte MIME → PyMuPDF parse.
- Chunking via `tiktoken` (`cl100k_base`), ~500-token chunks, 50-token overlap.
- Chunks stored in MongoDB `chunks` collection (`doc_id`, `owner_id`, `page_number`, `chunk_index`, `text`) and ChromaDB.

## Phase 3 — Embeddings + ChromaDB ✅
- `all-MiniLM-L6-v2` embedding model integrated.
- Per-user isolation via `user_id` metadata filtering on every Chroma query.
- Retrieval confirmed working.

## Phase 4 — Generation ✅
- `/documents/ask` endpoint wiring `retrieve_chunks()` + `generate_answer()`.
- Claude prompted to return strict JSON: `{"answer": ..., "used_chunks": [...]}`.
- Response mapped to `doc_id` / `filename` / `page_number` citations.

## Phase 5 — Frontend ✅
- Full auth flow: signup → OTP → verify → login → JWT stored in `localStorage`.
- Upload page and Ask page.
- Axios client with JWT interceptor + 401 auto-redirect.
- Brutalist/amber design system (Space Grotesk, Inter, IBM Plex Mono).
- Landing page with animated flow strip.

## Phase 6 — Deployment 🔄
- ✅ MongoDB migrated to Atlas (confirmed data landing in `documind.users`).
- ✅ Render free-tier OOM fixed via lazy-loading the embedding model (`_get_model()` cached function replacing module-level init in `embedding_service.py`).
- 🔄 Redeployment pushed — health confirmation pending.
- ⬜ Update hardcoded API base URL from `127.0.0.1:8000` to the deployed Render URL.
- ⬜ Update CORS `allow_origins` to the Vercel domain.
- ⬜ Deploy frontend to Vercel.
- ⬜ Write 15–20 Q&A eval set, run against the pipeline, score accuracy.
- ⬜ Finalize README with architecture, tech stack, eval score, and security section.
- ⬜ Make GitHub repo public.

## Phase 7 — Documentation & Wrap-Up ⬜
- ⬜ `KNOWN_LIMITATIONS.md` — honest write-up of the Render free-tier memory ceiling.
- ⬜ `FUTURE_WORK.md` — remaining Phase 6 items + longer-term feature roadmap.
- ⬜ Final README pass tying everything together with the public link.

## Suggested Immediate Next Steps
1. Confirm Render redeployment is healthy post lazy-loading fix.
2. Update frontend API base URL + backend CORS allow-list.
3. Deploy frontend to Vercel.
4. Build the eval set against the local server (doesn't require live deployment).
5. Finalize README, `KNOWN_LIMITATIONS.md`, and `FUTURE_WORK.md`.
6. Make the repo public.
