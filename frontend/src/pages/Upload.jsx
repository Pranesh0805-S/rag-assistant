import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

function Upload() {
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleUpload = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    if (!file) {
      setError('Please choose a PDF file first.')
      return
    }
    const formData = new FormData()
    formData.append('file', file)

    setLoading(true)
    try {
      const res = await client.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setSuccess(`Uploaded: ${res.data.filename || file.name}`)
      setFile(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed.')
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
        <h1>Upload Document</h1>
        <div>
            <button onClick={() => navigate('/ask')}>Go to Ask</button>
            <button onClick={handleLogout}>Log out</button>
        </div>
      </div>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  )
}

export default Upload