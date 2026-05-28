import { useMemo, useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'auth_token'

function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isFormValid = useMemo(
    () => username.trim().length > 0 && password.trim().length > 0,
    [password, username],
  )

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!isFormValid) {
      return
    }

    setError('')
    setIsSubmitting(true)

    try {
      const response = await fetch(`${API_BASE_URL}/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      if (!response.ok) {
        setError('Credenciales inválidas. Intenta nuevamente.')
        return
      }

      const data = await response.json()
      sessionStorage.setItem(TOKEN_KEY, data.access_token)
      navigate('/welcome', { replace: true })
    } catch {
      setError('No se pudo conectar con el backend.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="page">
      <main className="card card-base">
        <h1>Iniciar sesión</h1>
        <p className="subtitle">
          Usa tus credenciales para ingresar a la plataforma.
        </p>
        <form className="login-form" onSubmit={handleSubmit}>
          <label htmlFor="username">Usuario</label>
          <input
            id="username"
            className="text-input"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
          />

          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            className="text-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
          />

          {error ? <p className="error">{error}</p> : null}

          <button
            className="button-primary"
            type="submit"
            disabled={!isFormValid || isSubmitting}
          >
            {isSubmitting ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </main>
    </div>
  )
}

function WelcomePage() {
  const navigate = useNavigate()

  const handleLogout = () => {
    sessionStorage.removeItem(TOKEN_KEY)
    navigate('/login', { replace: true })
  }

  return (
    <div className="page">
      <main className="card card-base">
        <h1>Bienvenido</h1>
        <p className="subtitle">
          Has iniciado sesión correctamente y tu token está activo en la sesión.
        </p>
        <button className="button-primary" type="button" onClick={handleLogout}>
          Cerrar sesión
        </button>
      </main>
    </div>
  )
}

function ProtectedRoute({ children }) {
  const token = sessionStorage.getItem(TOKEN_KEY)
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/welcome"
        element={
          <ProtectedRoute>
            <WelcomePage />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

export default App
