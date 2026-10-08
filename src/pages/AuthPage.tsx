import { useState, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { authApi, errorMessage, setToken } from "../api"

export default function AuthPage({ mode }: { mode: "login" | "signup" }) {
  const navigate = useNavigate()
  const isSignup = mode === "signup"
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const { data } = isSignup
        ? await authApi.signup(email, password, fullName)
        : await authApi.login(email, password)
      setToken(data.access_token)
      navigate("/chat", { replace: true })
    } catch (err) {
      setError(errorMessage(err, isSignup ? "Couldn't create the account." : "Couldn't log in."))
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="auth">
      <section className="auth-card">
        <p className="brand">Smart RAG</p>
        <h1>{isSignup ? "Create your account" : "Log in"}</h1>
        <p className="muted">
          Upload a document, ask about it, and get answers Gemini has checked against the text.
        </p>

        <form onSubmit={handleSubmit} className="stack">
          {isSignup && (
            <label>
              Full name
              <input value={fullName} onChange={(e) => setFullName(e.target.value)} autoComplete="name" />
            </label>
          )}
          <label>
            Email
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              required
              minLength={isSignup ? 8 : undefined}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={isSignup ? "new-password" : "current-password"}
            />
            {isSignup && <small className="muted">At least 8 characters.</small>}
          </label>

          {error && <p className="error" role="alert">{error}</p>}

          <button type="submit" className="btn primary" disabled={busy}>
            {busy ? "Please wait…" : isSignup ? "Create account" : "Log in"}
          </button>
        </form>

        <p className="muted switch">
          {isSignup ? (
            <>Already have an account? <Link to="/login">Log in</Link></>
          ) : (
            <>New here? <Link to="/signup">Create an account</Link></>
          )}
        </p>
      </section>
    </main>
  )
}
