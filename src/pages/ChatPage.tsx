import { useCallback, useEffect, useRef, useState, type FormEvent } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import AnswerCard from "../components/AnswerCard"
import {
  askQuestion,
  authApi,
  chatsApi,
  clearToken,
  errorMessage,
  uploadFiles,
  type DocumentItem,
  type Message,
  type Session,
  type User,
} from "../api"

const ACCEPTED = ".pdf,.docx,.txt,.csv"

export default function ChatPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()

  const [user, setUser] = useState<User | null>(null)
  const [chats, setChats] = useState<Session[]>([])
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [question, setQuestion] = useState("")
  const [pendingQuestion, setPendingQuestion] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [notice, setNotice] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const fileInput = useRef<HTMLInputElement>(null)
  const bottom = useRef<HTMLDivElement>(null)

  const loadChats = useCallback(async () => {
    const { data } = await chatsApi.list()
    setChats(data)
  }, [])

  // Load the user and their chats once.
  useEffect(() => {
    authApi.me().then(({ data }) => setUser(data)).catch(() => {})
    loadChats().catch((err) => setError(errorMessage(err)))
  }, [loadChats])

  // Load the open chat's documents and messages whenever the URL changes.
  useEffect(() => {
    setError(null)
    setNotice(null)
    setSidebarOpen(false)
    if (!sessionId) {
      setDocuments([])
      setMessages([])
      return
    }
    Promise.all([chatsApi.documents(sessionId), chatsApi.messages(sessionId)])
      .then(([docs, msgs]) => {
        setDocuments(docs.data)
        setMessages(msgs.data)
      })
      .catch((err) => setError(errorMessage(err, "Couldn't open this chat.")))
  }, [sessionId])

  useEffect(() => {
    bottom.current?.scrollIntoView({ block: "end" })
  }, [messages, pendingQuestion])

  async function handleFiles(fileList: FileList | null) {
    const files = Array.from(fileList ?? [])
    if (files.length === 0) return
    setUploading(true)
    setError(null)
    setNotice(null)
    try {
      const { data } = await uploadFiles(files, sessionId)
      setNotice(`Indexed ${files.length} file(s) into ${data.chunk_count} chunk(s). Ask a question below.`)
      await loadChats()
      if (data.session_id !== sessionId) {
        navigate(`/chat/${data.session_id}`)
      } else {
        const docs = await chatsApi.documents(data.session_id)
        setDocuments(docs.data)
      }
    } catch (err) {
      setError(errorMessage(err, "Upload failed."))
    } finally {
      setUploading(false)
      if (fileInput.current) fileInput.current.value = ""
    }
  }

  async function ask(text: string) {
    const trimmed = text.trim()
    if (!trimmed || !sessionId || pendingQuestion) return
    setQuestion("")
    setError(null)
    setNotice(null)
    setPendingQuestion(trimmed)
    try {
      const { data } = await askQuestion(sessionId, trimmed)
      setMessages((previous) => [...previous, { ...data, id: `local-${Date.now()}` }])
      loadChats().catch(() => {})
    } catch (err) {
      setError(errorMessage(err, "Couldn't get an answer."))
      setQuestion(trimmed)
    } finally {
      setPendingQuestion(null)
    }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    ask(question)
  }

  async function deleteChat(id: string) {
    if (!window.confirm("Delete this chat, its documents and its messages?")) return
    try {
      await chatsApi.remove(id)
      await loadChats()
      if (id === sessionId) navigate("/chat")
    } catch (err) {
      setError(errorMessage(err, "Couldn't delete the chat."))
    }
  }

  async function deleteDocument(document: DocumentItem) {
    if (!sessionId || !window.confirm(`Remove ${document.file_name} from this chat?`)) return
    try {
      await chatsApi.deleteDocument(sessionId, document.id)
      setDocuments((previous) => previous.filter((d) => d.id !== document.id))
      loadChats().catch(() => {})
    } catch (err) {
      setError(errorMessage(err, "Couldn't remove the document."))
    }
  }

  function logout() {
    clearToken()
    navigate("/login", { replace: true })
  }

  const currentChat = chats.find((chat) => chat.id === sessionId)
  const canAsk = Boolean(sessionId) && documents.length > 0 && !pendingQuestion

  return (
    <div className="layout">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-top">
          <p className="brand">Smart RAG</p>
          <Link to="/chat" className="btn primary block">+ New chat</Link>
        </div>

        <nav className="chat-list" aria-label="Your chats">
          {chats.length === 0 && <p className="muted small">No chats yet.</p>}
          {chats.map((chat) => (
            <div key={chat.id} className={`chat-item ${chat.id === sessionId ? "active" : ""}`}>
              <Link to={`/chat/${chat.id}`}>
                <span className="chat-title">{chat.title || "Untitled chat"}</span>
                <span className="chat-sub">
                  {chat.document_count} doc · {chat.message_count} msg
                </span>
              </Link>
              <button className="icon" onClick={() => deleteChat(chat.id)} aria-label="Delete chat" title="Delete chat">
                ×
              </button>
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <span className="small muted ellipsis">{user?.email}</span>
          <button className="btn ghost" onClick={logout}>Log out</button>
        </div>
      </aside>

      <main className="main" onClick={() => sidebarOpen && setSidebarOpen(false)}>
        <header className="topbar">
          <button className="btn ghost menu" onClick={() => setSidebarOpen((open) => !open)}>
            Chats
          </button>
          <h1 className="ellipsis">{currentChat?.title || "New chat"}</h1>
          <button className="btn" onClick={() => fileInput.current?.click()} disabled={uploading}>
            {uploading ? "Indexing…" : "Upload document"}
          </button>
          <input
            ref={fileInput}
            type="file"
            accept={ACCEPTED}
            multiple
            hidden
            onChange={(e) => handleFiles(e.target.files)}
          />
        </header>

        {documents.length > 0 && (
          <div className="doc-bar" aria-label="Documents in this chat">
            {documents.map((document) => (
              <span key={document.id} className="doc-chip">
                {document.file_name}
                {document.page_count ? <small> · {document.page_count} p</small> : null}
                <button className="icon" onClick={() => deleteDocument(document)} aria-label={`Remove ${document.file_name}`}>
                  ×
                </button>
              </span>
            ))}
          </div>
        )}

        <section className="thread">
          {documents.length === 0 && messages.length === 0 && (
            <div className="empty">
              <h2>Start with a document</h2>
              <p className="muted">
                Upload a PDF, Word, text or CSV file. It's split into chunks, embedded and stored, and every
                answer is built only from those chunks and then checked by Gemini.
              </p>
              <button className="btn primary" onClick={() => fileInput.current?.click()} disabled={uploading}>
                {uploading ? "Indexing…" : "Upload document"}
              </button>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id} className="turn">
              <p className="question">{message.question}</p>
              <AnswerCard answer={message} onFollowUp={ask} />
            </div>
          ))}

          {pendingQuestion && (
            <div className="turn">
              <p className="question">{pendingQuestion}</p>
              <div className="answer pending">
                <span className="spinner" aria-hidden="true" />
                <span role="status">Searching from your documents…</span>
              </div>
            </div>
          )}

          {notice && <p className="notice">{notice}</p>}
          {error && <p className="error" role="alert">{error}</p>}
          <div ref={bottom} />
        </section>

        <form className="composer" onSubmit={handleSubmit}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                ask(question)
              }
            }}
            placeholder={documents.length ? "Ask a question about your documents…" : "Upload a document first"}
            disabled={!sessionId || documents.length === 0}
            rows={2}
          />
          <button type="submit" className="btn primary" disabled={!canAsk || !question.trim()}>
            Ask
          </button>
        </form>
      </main>
    </div>
  )
}
