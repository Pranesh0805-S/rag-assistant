# PRD — DocuMind: Multi-Document RAG Assistant with Citations

## 1. Summary
DocuMind is a web application where a user uploads multiple PDF documents and asks questions in plain English. The system retrieves the most relevant text chunks across all of that user's uploaded documents, sends them to an LLM, and returns an answer that cites exactly which document and page it came from.

**Positioning:** Not just "chat with PDF." The differentiators are multi-document synthesis, citation grounding down to the page level, and a hand-scored evaluation set that proves real accuracy instead of a happy-path demo.

## 2. Problem Statement
Students, researchers, and professionals accumulate many PDFs (notes, papers, manuals) and waste time manually searching across them for answers. Generic LLM chat doesn't ground answers in the user's own source material or tell them where an answer came from, so answers can't be trusted or verified.

## 3. Target User
- Primary: the builder themself, as a portfolio/resume artifact demonstrating full-stack + RAG engineering ability to interviewers.
- Secondary (realistic usage persona): a student or researcher with a handful of PDFs who wants grounded, cited answers instead of manually skimming documents.

## 4. Goals
- Ship a publicly deployed, working link (not just localhost).
- Demonstrate multi-document retrieval with accurate, page-level citations.
- Produce a documented accuracy number from a hand-written 15–20 question eval set.
- Demonstrate secure, multi-tenant handling of user data (auth + per-user data isolation).

## 5. Non-Goals (for current scope)
- Not a general-purpose chatbot — answers are always grounded in the user's uploaded documents.
- Not optimized for huge document sets (hundreds of PDFs per user) — current scope is a handful of documents per user.
- Not a paid/commercial product — free-tier infrastructure is an accepted constraint, not a defect.

## 6. Core Use Cases
1. A new user signs up, verifies their email via OTP, and logs in.
2. The user uploads one or more PDF documents.
3. The user asks a question in a chat-style interface.
4. The system returns an answer plus a list of citations (document name + page number) that a user can trust and verify.
5. The user can see which of their previously uploaded documents exist and ask further questions against any combination of them.

## 7. Functional Requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | User can sign up with email + password | Must |
| FR-2 | User must verify email via OTP before accessing the app | Must |
| FR-3 | User can log in and receive a JWT | Must |
| FR-4 | User can upload PDF files (validated by extension, size, and MIME/magic bytes) | Must |
| FR-5 | Uploaded PDFs are parsed, chunked, embedded, and stored per-user | Must |
| FR-6 | User can ask a natural-language question against their uploaded documents | Must |
| FR-7 | System retrieves top-k relevant chunks scoped only to that user's documents | Must |
| FR-8 | System generates an answer via Claude, grounded in retrieved chunks | Must |
| FR-9 | Answer includes citations: document name + page number | Must |
| FR-10 | User cannot access another user's documents under any circumstance | Must |
| FR-11 | Project includes a hand-written 15–20 Q&A eval set with a scored accuracy result documented in the README | Must |

## 8. Success Metrics
- Live, publicly accessible deployment (backend + frontend).
- Documented eval accuracy score (e.g., X/18 correct with correct citation).
- Zero cross-user data leakage in testing.
- A README that clearly documents architecture, tech stack, security measures, and known limitations.

## 9. Constraints & Known Trade-offs
- Free-tier hosting (Render 512MB RAM) creates real memory pressure from `torch`/`sentence-transformers`; documented honestly in `KNOWN_LIMITATIONS.md` rather than hidden.
- Single LLM provider (Claude) in current scope; multi-model support is future work.
- No persisted chat history in current scope; each session's Q&A is not saved.

## 10. Out-of-Scope Ideas Deferred to Future Work
See `FUTURE_WORK.md` for the full list: multi-model AI switching, chat history, drag-and-drop multi-upload, inline PDF preview, exportable transcripts, eval dashboard, OAuth logins, optional authenticator-app 2FA, and web-search augmentation.
