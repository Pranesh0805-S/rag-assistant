# App Flow — User Journey

## 1. First-Time User Journey
1. **Landing page** — user sees an overview of DocuMind, an animated flow strip explaining "upload → ask → cited answer," and a Sign Up / Log In call to action.
2. **Sign up** — user enters email + password.
3. **OTP verification** — backend sends a one-time code to the user's email via Gmail SMTP; user enters the code to verify their account. Access is blocked until verification succeeds.
4. **Login** — user logs in with verified credentials; backend issues a JWT, stored in `localStorage` on the frontend.
5. **Redirected to app** — axios client attaches JWT to all subsequent requests via interceptor; a 401 response anywhere triggers auto-redirect back to login.

## 2. Core Loop: Upload → Ask → Cited Answer
1. **Upload page** — user selects a PDF file.
   - Frontend sends file to backend.
   - Backend validates extension → size → MIME/magic bytes → PyMuPDF parse.
   - On success: text is extracted per page, chunked (~500 tokens, 50-token overlap), embedded, and stored (MongoDB + ChromaDB, scoped to `user_id`).
   - User sees upload confirmation (or a clear validation error if rejected).
2. **Ask page** — user types a question in natural language.
   - Question is sent to `/documents/ask`.
   - Backend retrieves top-k relevant chunks across all of that user's documents.
   - Claude generates an answer grounded only in those chunks.
   - Response includes the answer text plus a citation list (document name + page number).
3. **Answer display** — user sees the answer with clickable/visible citations referencing "Document X, Page Y," so they can verify the source themselves.

## 3. Returning User Journey
1. User logs in (JWT reissued).
2. User can upload additional documents, which join their existing document set.
3. User asks new questions; retrieval spans all previously uploaded documents for that user (not just the most recent one).

## 4. Error & Edge-Case Flows
| Scenario | Behavior |
|---|---|
| Non-PDF file uploaded | Rejected at extension/MIME/magic-byte check with a clear error message |
| File exceeds size limit | Rejected before parsing begins |
| Expired JWT | 401 → frontend auto-redirects to login |
| Question asked with zero documents uploaded | System returns a clear "no documents to search" response rather than a hallucinated answer |
| Backend cold-start under free-tier memory pressure | Slow first request while embedding model lazy-loads; documented in `KNOWN_LIMITATIONS.md` |

## 5. Journey Map Summary
```
Landing → Sign Up → OTP Verify → Login
   → Upload PDF(s) → (validate → parse → chunk → embed → store)
   → Ask Question → (retrieve top-k → generate via Claude → map citations)
   → View Answer + Citations
   → (repeat: upload more docs / ask more questions)
```
