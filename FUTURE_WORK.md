# Future Work

This document captures remaining Phase 6 deployment steps plus the longer-term feature roadmap for DocuMind beyond the current MVP.

## A. Remaining Phase 6 Deployment Steps (Short-Term)
- [ ] Confirm Render redeployment is healthy after the lazy-loading memory fix.
- [ ] Update the frontend's hardcoded API base URL (`127.0.0.1:8000`) to the deployed Render URL.
- [ ] Update backend CORS `allow_origins` to the Vercel domain.
- [ ] Deploy the frontend to Vercel.
- [ ] Write a 15–20 question hand-scored eval set and document the accuracy result in the README.
- [ ] Make the GitHub repository public once deployment is finalized.

## B. Feature Roadmap (Long-Term)

### 1. Multi-Model AI Switching (Gemini / Claude / ChatGPT / Ollama)
Allow the user to switch between multiple LLM providers — Gemini, Claude, ChatGPT (OpenAI), and a free-tier local Ollama model — at any point during a conversation, on a per-document or per-conversation basis, for each individual user.
- Requires an abstraction layer in the generation service so `generate_answer()` can route to any configured provider behind a common interface.
- Requires storing the selected model per conversation/message so history reflects which model produced which answer.
- Ollama integration implies a local/self-hosted inference path distinct from the hosted-API providers — worth documenting as a distinct code path (no API key, different latency/availability characteristics).

### 2. Chat History & Saved Conversations
Persist conversations per user so questions and answers survive across sessions, rather than existing only in the current session.
- New `conversations` and `messages` collections scoped by `owner_id`, mirroring the same per-user isolation guarantee already enforced on documents/chunks.
- Frontend: a history sidebar to browse and resume past conversations.

### 3. Drag-and-Drop Multi-File Upload
Replace/extend the current single-file picker with a drag-and-drop zone supporting multiple PDFs in one action, with per-file progress and validation feedback.

### 4. Inline PDF Preview Alongside Citations
When a citation references "Document X, Page Y," let the user view that exact page inline next to the answer, rather than only seeing the citation as text metadata.
- Likely requires serving/rendering the stored PDF (or a per-page rendering) securely, still scoped to the owning user.

### 5. Exportable Answer Transcripts
Let a user export a Q&A session (or a full conversation) as a document — e.g., PDF or Markdown — including the answer text and its citations, for reference outside the app.

### 6. Eval Dashboard with Accuracy Scoring
Turn the current one-off hand-written eval set into a persistent, re-runnable dashboard: store the eval questions/expected answers, run them against the live pipeline on demand, and visualize pass/fail and citation-accuracy trends over time as the pipeline changes.

### 7. Google / GitHub / Microsoft OAuth Login
Add third-party OAuth login options alongside the existing email/password + OTP flow, giving users a faster signup/login path without weakening the existing security model.

### 8. Optional Authenticator-App Two-Factor Authentication
Add a separate, standalone authenticator-app-based (TOTP) two-step verification option.
- Strictly opt-in: the user chooses whether to enable it — it is never mandatory, and the platform owner does not force it on any account.
- Once enabled by a user, it is enforced only for that user's own login flow, fully reversible at the user's own discretion.

### 9. Web Search to Enrich Answers About Uploaded Documents
Allow the system to optionally supplement an answer with live web search results related to the uploaded document's topic — for example, providing broader context or recent developments connected to the material — while keeping the core answer still grounded primarily in the user's own documents.

### 10. Web Search as a Retention Feature, Not a Primary Pillar
Position web search as a secondary, supportive capability rather than a headline feature: its purpose is to keep the user productive inside DocuMind for tasks adjacent to their documents, reducing the need to leave the app to search elsewhere — not to turn DocuMind into a general-purpose search engine.

## C. Sequencing Notes
These are intentionally listed as future work rather than current scope: shipping the MVP (auth, upload, retrieval, citation-grounded generation, eval score, honest limitations doc) is the priority that makes DocuMind a complete, defensible portfolio piece today. Each roadmap item above is a natural "if I had more time" answer for an interview, and can be picked up independently without blocking the current deployment.
