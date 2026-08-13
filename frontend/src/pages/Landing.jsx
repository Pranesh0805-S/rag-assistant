import { Link } from 'react-router-dom'

const STEPS = [
  { n: '01', title: 'Upload', desc: 'Drop in multiple PDFs — notes, papers, manuals. Each file is validated and stored per user.' },
  { n: '02', title: 'Chunk', desc: 'Text is split into ~500-token pieces with overlap, tagged with document and page number.' },
  { n: '03', title: 'Embed', desc: 'Every chunk becomes a 384-dim vector via sentence-transformers, stored in ChromaDB.' },
  { n: '04', title: 'Retrieve', desc: 'Your question is embedded too — the top matching chunks across all your docs are pulled, scoped only to you.' },
  { n: '05', title: 'Generate', desc: 'Claude reads the retrieved chunks and writes an answer grounded strictly in your documents.' },
  { n: '06', title: 'Cite', desc: 'Every answer comes back with exact document and page citations — no guessing where it came from.' },
]

const FEATURES = [
  { title: 'Multi-doc synthesis', desc: 'Ask across every uploaded PDF at once, not just one file at a time.' },
  { title: 'Citation grounding', desc: 'Answers are traceable to an exact document and page — never a black box.' },
  { title: 'Per-user isolation', desc: 'Every retrieval is scoped server-side to your account. Your docs stay yours.' },
  { title: 'JWT authentication', desc: 'Signup, OTP email verification, and token-based sessions out of the box.' },
  { title: 'Fast local embeddings', desc: 'sentence-transformers runs locally — no per-embedding API cost.' },
  { title: 'Claude-powered answers', desc: 'Generation grounded strictly in retrieved chunks, not free-floating memory.' },
]

const UPCOMING = [
  'Chat history & saved conversations',
  'Drag-and-drop multi-file upload',
  'Inline PDF preview alongside citations',
  'Exportable answer transcripts',
  'Eval dashboard with accuracy scoring',
]

function Landing() {
  return (
    <div className="landing">
      <header className="landing-hero">
        <p className="landing-eyebrow">Multi-document RAG assistant</p>
        <h1 className="landing-title">
          Ask your documents.
          <br />
          Get answers with <span className="landing-accent">receipts</span>.
        </h1>
        <p className="landing-sub">
          Upload multiple PDFs, ask questions in plain English, and get answers
          that cite the exact document and page they came from.
        </p>
        <div className="landing-cta">
          <Link to="/signup" className="landing-btn-primary">Get started</Link>
          <Link to="/login" className="landing-btn-secondary">Log in</Link>
        </div>
      </header>

      <div className="flow-strip" aria-hidden="true">
        <div className="flow-track">
          {Array.from({ length: 3 }).map((_, i) => (
            <div className="flow-set" key={i}>
              {STEPS.map((s) => (
                <span className="flow-dot" key={s.n}>
                  <span className="flow-dot-core" />
                  <span className="flow-dot-label">{s.title}</span>
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>

      <section className="landing-pipeline">
        <p className="landing-section-label">How it works</p>
        <div className="pipeline-track">
          {STEPS.map((step, i) => (
            <div className="pipeline-step" style={{ animationDelay: `${i * 0.12}s` }} key={step.n}>
              <span className="pipeline-num">{step.n}</span>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
              {i < STEPS.length - 1 && <span className="pipeline-arrow">→</span>}
            </div>
          ))}
        </div>
      </section>

      <section className="landing-features">
        <p className="landing-section-label">Features</p>
        <div className="features-grid">
          {FEATURES.map((f) => (
            <div className="feature-card" key={f.title}>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="landing-upcoming">
        <p className="landing-section-label">Upcoming</p>
        <ul className="upcoming-list">
          {UPCOMING.map((item) => (
            <li key={item}>
              <span>{item}</span>
              <span className="upcoming-badge">Soon</span>
            </li>
          ))}
        </ul>
      </section>

      <footer className="landing-footer">
        <p>Built with FastAPI, ChromaDB, sentence-transformers, and Claude.</p>
      </footer>
    </div>
  )
}

export default Landing