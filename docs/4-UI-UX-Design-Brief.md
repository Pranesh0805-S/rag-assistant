# UI/UX Design Brief — DocuMind

## 1. Design Philosophy
Brutalist / amber design system — a deliberate departure from the generic rounded-corner, soft-shadow "SaaS starter template" look, chosen to make the portfolio piece visually memorable to reviewers/interviewers rather than blending in.

## 2. Typography
| Role | Font |
|---|---|
| Display / headings | Space Grotesk |
| Body text | Inter |
| Code / technical / citations / metadata | IBM Plex Mono |

## 3. Color Direction
- Amber as the primary accent against a high-contrast neutral (light or dark) base.
- Deliberate, sharp contrast rather than muted pastel tones — consistent with the brutalist direction.
- Citation elements and technical metadata rendered in monospace to visually separate "system output you can verify" from generated prose.

## 4. Key Screens
1. **Landing Page**
   - Animated flow strip visualizing Upload → Ask → Cited Answer.
   - Clear, single primary CTA (Sign Up / Log In).
2. **Sign Up / OTP Verify / Login**
   - Minimal, single-column forms; no distractions during the auth flow.
   - Clear inline validation errors (bad password, invalid OTP, expired OTP).
3. **Upload Page**
   - File picker with visible constraints (PDF only, max size).
   - Upload status feedback (parsing → chunking → embedding → done), since processing isn't instantaneous.
4. **Ask Page**
   - Chat-style input for natural-language questions.
   - Answer rendered with a visually distinct citations block (document name + page number) beneath or alongside the answer — citations should look like verifiable metadata, not part of the generated prose.

## 5. Interaction Principles
- Every AI-generated answer must be visually paired with its citations — never shown without them.
- Processing states (upload, embedding, retrieval, generation) should be visible to the user rather than a silent spinner, since this is a portfolio piece meant to demonstrate the pipeline, not just hide it.
- Errors (auth, upload validation, retrieval failures) are shown as clear, specific inline messages — never a generic "something went wrong."

## 6. Accessibility Baseline
- Sufficient color contrast between amber accents and background (verify against WCAG AA for text).
- All forms keyboard-navigable.
- Citation links/buttons have visible focus states.

## 7. Future UI Considerations (see FUTURE_WORK.md)
- Inline PDF preview alongside citations.
- Drag-and-drop multi-file upload.
- Chat history sidebar for saved conversations.
- Model-switcher UI element for multi-provider AI selection.
