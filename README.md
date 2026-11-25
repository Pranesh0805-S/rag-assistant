# DocuMind — Multi-Document RAG Assistant with Citations

DocuMind is a full-stack web app where you upload multiple PDFs and ask questions in plain English. It retrieves the most relevant text across **all** of your uploaded documents, sends it to Claude, and returns an answer that **cites the exact document and page** it came from.

**What sets it apart from a basic "chat with your PDF" tool:** multi-document synthesis, page-level citation grounding, strict per-user data isolation, and a hand-written evaluation set with a documented accuracy score.

**Live demo:** https://documind-five-blush.vercel.app/

> **Heads up:** the backend runs on a free tier and sleeps when idle. The first request after a quiet period can take 30+ seconds while it wakes up. Details in [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md).

---

## Screenshots

_Add 2–3 screenshots or a short demo GIF here: upload → ask a question → answer with citations._

## Live Deployment

| Part | Link |
|---|---|
| Frontend (Vercel) | https://documind-five-blush.vercel.app/ |
| Backend API docs (Render) | _add Render URL + `/docs`_ |

## Eval Accuracy

_Add the scored result once the 15–20 question eval set is complete (for example, "16/18 correct, with correct citation")._

---

## How It Works

1. **Upload** PDFs. Each file is validated by extension, size and MIME/magic bytes.
2. **Chunk** the text (~500 tokens, 50-token overlap) and keep page numbers.
3. **Embed** the chunks with `all-MiniLM-L6-v2` and store them in a per-user ChromaDB collection.
4. **Retrieve** the top-k chunks, scoped strictly to the requesting user's documents.
5. **Generate** a grounded answer with Claude, returned as structured JSON.
6. **Cite** every answer with document name and page number.

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

## Core Features

- **Auth:** signup, OTP email verification, JWT login
- **Upload:** PDF-only, validated by extension, size and magic bytes
- **Multi-document retrieval:** one question searches across all your documents
- **Citations:** every answer paired with document name and page
- **Per-user isolation:** no user can retrieve another user's documents
- **Eval set:** 15–20 hand-written Q&A pairs scored for answer and citation accuracy

## Security

- API keys live only in the backend `.env`, never in frontend code or git history.
- Every upload, chat and retrieval endpoint requires a valid JWT.
- **Data isolation:** every database and vector-store query is scoped server-side by the authenticated user's ID, never by a client-supplied value.
- PDF uploads are validated by extension, size limit and MIME/magic bytes, not by extension alone.
- CORS is restricted to the actual frontend domain, never `*`.

## Run Locally

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # add your keys
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

_Adjust folder names, entry file and env variable names to match the repo._

## Known Limitations

Free-tier hosting has real constraints: the Render 512 MB memory ceiling (partly fixed by lazy-loading the embedding model), SMTP throttling for OTP emails, no saved chat history, a single LLM provider and single-factor login. See [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) for the full, honest breakdown.

## Roadmap

Multi-model switching, saved chat history, drag-and-drop multi-file upload, inline PDF preview next to citations, exportable transcripts, an eval dashboard, OAuth login, optional authenticator-app 2FA and web-search augmentation. See [FUTURE_WORK.md](./FUTURE_WORK.md).

## Project Documentation

| Document | Purpose |
|---|---|
| [1-PRD-Product-Requirements.md](./1-PRD-Product-Requirements.md) | Product goals, use cases, functional requirements |
| [2-TRD-Technical-Requirements.md](./2-TRD-Technical-Requirements.md) | Architecture, tech stack, pipeline internals |
| [3-App-Flow-User-Journey.md](./3-App-Flow-User-Journey.md) | End-to-end user journey and edge cases |
| [4-UI-UX-Design-Brief.md](./4-UI-UX-Design-Brief.md) | Design system, key screens, interaction principles |
| [5-Backend-Schema-Data-Auth.md](./5-Backend-Schema-Data-Auth.md) | Database schemas, auth flow, data isolation guarantee |
| [6-Implementation-Plan-Build-Order.md](./6-Implementation-Plan-Build-Order.md) | Phase-by-phase build status and next steps |
| [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) | Current infrastructure constraints |
| [FUTURE_WORK.md](./FUTURE_WORK.md) | Long-term feature roadmap |

## Author

**Pranesh S** — Full-stack developer, Coimbatore, India
GitHub: [Pranesh0805-S](https://github.com/Pranesh0805-S) · LinkedIn: [pranesh0805](https://www.linkedin.com/in/pranesh0805/)
