# Known Limitations

DocuMind is deployed on free-tier infrastructure. This document explains the real constraints honestly, rather than hiding them — understanding these trade-offs is part of the engineering story.

## 1. Backend Memory Ceiling (Render Free Tier)
**Symptom:** Occasional failures on the embedding/generation step, especially on cold start.

**Root cause:** Render's free tier caps each web service at 512MB RAM. The embedding pipeline (`sentence-transformers` + `torch`) plus ChromaDB plus the rest of the FastAPI app can approach or exceed that ceiling, particularly on a cold start where everything initializes at once.

**What was done about it:** The embedding model was originally loaded at module import time, guaranteeing it consumed memory on every process start regardless of whether it was needed yet. This was changed to lazy-loading — a cached `_get_model()` function that only loads `all-MiniLM-L6-v2` on first actual use — which meaningfully reduced baseline memory pressure.

**What remains:** Even with lazy-loading, a cold start under load (e.g., the very first request after a period of inactivity, when Render's free tier spins the instance down) can still hit the memory ceiling. This is a platform/tier constraint, not a code defect — the fix beyond this point is a paid tier or offloading embeddings to a hosted API, both deliberately out of scope for a free-tier student project.

**Confirmed via:** Render's own platform message: "An instance of your Web Service documind-backend exceeded its memory limit."

## 2. Email Delivery (Gmail SMTP on Free Hosting)
**Symptom:** OTP emails may be delayed or occasionally blocked in production.

**Root cause:** Free-tier cloud hosts commonly restrict or throttle outbound SMTP traffic, which Gmail SMTP relies on for OTP delivery. This differs from local development, where outbound SMTP is unrestricted.

**What remains:** A transactional email API (e.g., a dedicated email-sending service) would remove this constraint but is deferred — see `FUTURE_WORK.md`.

## 3. No Persisted Chat History
Each session's questions and answers are not currently saved. Every question is answered independently against the retrieval pipeline; there is no conversation memory or saved history across sessions. See `FUTURE_WORK.md`.

## 4. Single LLM Provider
Generation currently runs exclusively through the Claude API. There is no multi-provider switching (Gemini, ChatGPT, local Ollama models) in the current build. See `FUTURE_WORK.md`.

## 5. Single-Factor Login Only
Authentication currently supports email/password + OTP email verification at signup. There is no ongoing two-factor authentication step at login, and no third-party OAuth login (Google/GitHub/Microsoft). See `FUTURE_WORK.md`.

## 6. No Web Search Augmentation
Answers are grounded exclusively in the user's uploaded documents. There is no fallback to live web search when the answer isn't contained in the uploaded PDFs. See `FUTURE_WORK.md`.

## Why These Limitations Are Documented, Not Hidden
A portfolio project that ships with an honest, specific limitations write-up demonstrates more engineering maturity than one that simply omits the parts that didn't scale. Nearly every one of these limitations is a direct, explainable trade-off of choosing free-tier infrastructure for a resource-heavy ML pipeline — that trade-off itself is worth being able to explain clearly in an interview.
