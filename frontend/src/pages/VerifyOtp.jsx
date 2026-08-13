import { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import client from '../api/client'

function VerifyOtp() {
  const location = useLocation()
  const navigate = useNavigate()
  const [email, setEmail] = useState(location.state?.email || '')
  const [otp, setOtp] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)
    try {
      const res = await client.post('/auth/verify-otp', { email, otp })
      setSuccess(res.data.message || 'Verified!')
      setTimeout(() => navigate('/login'), 1200)
    } catch (err) {
      setError(err.response?.data?.detail || 'Verification failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <h1>Verify your email</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify'}
        </button>
      </form>
      <p>
        Back to <Link to="/login">Log in</Link>
      </p>
    </div>
  )
}

export default VerifyOtp