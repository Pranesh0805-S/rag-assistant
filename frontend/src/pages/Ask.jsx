import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../api/client'

function Ask() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [citations, setCitations] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleAsk = async (e) => {
    e.preventDefault()
    setError('')
    setAnswer('')
    setCitations([])
    setLoading(true)
    try {
      const res = await client.post('/documents/ask', {
        question,
        top_k: 5,
      })
      setAnswer(res.data.answer)
      setCitations(res.data.citations || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get an answer.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Ask DocuMind</h1>
        <div>
          <Link to="/upload">Upload</Link>
          <button onClick={handleLogout}>Log out</button>
        </div>
      </div>

      <form onSubmit={handleAsk}>
        <input
          type="text"
          placeholder="Ask a question about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {answer && (
        <div className="answer-block">
          <h2>Answer</h2>
          <p>{answer}</p>

          {citations.length > 0 && (
            <div className="citations">
              <h3>Sources</h3>
              <ul>
                {citations.map((c, i) => (
                  <li key={i} className="citation-pill">
                    {c.filename} — Page {c.page_number}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Ask