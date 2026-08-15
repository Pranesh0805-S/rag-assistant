# Backend Schema, Data & Auth — DocuMind

## 1. Data Stores
- **MongoDB (Atlas in production)** — users, document metadata, chunk text/metadata.
- **ChromaDB** — vector embeddings for retrieval, metadata-filtered by `user_id`.

## 2. Collections / Schemas

### `users`
| Field | Type | Notes |
|---|---|---|
| `_id` | ObjectId | primary key |
| `email` | string | unique, used for login |
| `password_hash` | string | bcrypt hash (bcrypt==4.0.1 pinned for passlib compatibility) |
| `is_verified` | bool | set true after OTP verification |
| `created_at` | datetime | |

### `otps`
| Field | Type | Notes |
|---|---|---|
| `_id` | ObjectId | |
| `user_id` / `email` | ref | who this OTP belongs to |
| `code` | string | one-time code |
| `expires_at` | datetime | short-lived |
| `used` | bool | prevents replay |

### `documents`
| Field | Type | Notes |
|---|---|---|
| `_id` / `doc_id` | ObjectId | |
| `owner_id` | ObjectId | references `users._id`; enforced on every query |
| `filename` | string | |
| `page_count` | int | |
| `uploaded_at` | datetime | |
| `status` | string | e.g. `processing`, `ready`, `failed` |

### `chunks`
| Field | Type | Notes |
|---|---|---|
| `_id` | ObjectId | |
| `doc_id` | ObjectId | references `documents._id` |
| `owner_id` | ObjectId | duplicated here for fast per-user scoping without a join |
| `page_number` | int | source page |
| `chunk_index` | int | order within document |
| `text` | string | raw chunk text (~500 tokens, 50-token overlap) |

### ChromaDB collection
- Vectors keyed to the same `chunk_id`/`doc_id`.
- Metadata includes `user_id` (or `owner_id`) — every retrieval query filters on this metadata field server-side, never trusting a client-supplied user id.

## 3. Auth Flow
1. **Signup:** email + password received → password hashed with bcrypt → user created with `is_verified: false`.
2. **OTP:** code generated, emailed via Gmail SMTP, stored with expiry.
3. **Verify:** user submits code → matched against stored OTP (unexpired, unused) → `is_verified` set true.
4. **Login:** credentials checked against `password_hash` → JWT issued (HTTPBearer scheme).
5. **Protected routes:** JWT required via a FastAPI dependency (`deps.py`); expired/invalid tokens return 401.
6. **`/auth/me`:** returns the authenticated user's identity — used to confirm the auth flow end-to-end.

## 4. Data Isolation Guarantee
- Every document/chunk/vector query is scoped server-side by the authenticated user's ID extracted from the verified JWT — never from a client-supplied field.
- This is the single most important security invariant in the system: **user A must never be able to retrieve or query user B's documents**, enforced identically at the MongoDB layer and the ChromaDB layer.

## 5. Secrets & Config
- `.env` (never committed): Claude API key, `MONGO_URI`, JWT signing secret, SMTP credentials.
- `pydantic-settings` config class is the single source of truth for setting names — casing must match exactly where referenced in code.
- Separate `.env` values for local vs. production; production credentials never reused locally.

## 6. Known Auth-Related Gotchas (from build experience)
- JWT expiry during testing produces 401s that look like bugs but are just expired tokens — re-authenticate before debugging.
- CORS must be explicitly configured (`CORSMiddleware`) or the frontend fails silently against a working backend.
