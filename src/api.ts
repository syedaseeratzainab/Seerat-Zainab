// Everything the frontend sends to the backend goes through this file.
import axios from "axios"

// ---------- Where is the backend? ----------
// Local dev: leave VITE_API_BASE_URL empty and Vite proxies /api to localhost:8000.
// Railway: set VITE_API_BASE_URL to the backend's public URL. Vite bakes this value into
// the bundle at BUILD time, so changing it requires redeploying the frontend.
function getApiBaseUrl(): string {
  let url = (import.meta.env.VITE_API_BASE_URL || "").trim().replace(/\/+$/, "")
  if (!url) return "/api"
  if (!/^https?:\/\//.test(url) && !url.startsWith("/")) url = `https://${url}`
  if (!url.endsWith("/api")) url = `${url}/api`
  return url
}

export const API_BASE_URL = getApiBaseUrl()

// ---------- Login token ----------
const TOKEN_KEY = "smart-rag-lite-token"
export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const setToken = (token: string) => localStorage.setItem(TOKEN_KEY, token)
export const clearToken = () => localStorage.removeItem(TOKEN_KEY)

export const api = axios.create({ baseURL: API_BASE_URL })

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Expired or invalid token: log out and go back to the login page.
    if (error.response?.status === 401 && getToken()) {
      clearToken()
      window.location.assign("/login")
    }
    return Promise.reject(error)
  }
)

export function errorMessage(error: unknown, fallback = "Something went wrong. Try again."): string {
  if (axios.isAxiosError(error)) {
    if (!error.response) return "Can't reach the backend. Check that it is running."
    const detail = error.response.data?.detail
    if (typeof detail === "string") return detail
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg
  }
  return fallback
}

// ---------- Types (mirror the backend's response schemas) ----------
export interface User {
  id: string
  email: string
  full_name: string | null
}

export interface Session {
  id: string
  title: string | null
  created_at: string
  document_count: number
  message_count: number
}

export interface DocumentItem {
  id: string
  file_name: string
  file_type: string
  page_count: number | null
}

export interface Citation {
  source_type: "document" | "web"
  document_name?: string | null
  page_number?: number | null
  chunk_index?: number | null
  title?: string | null
  url?: string | null
  text?: string | null
}

export interface Message {
  id: string
  question: string
  answer: string
  source: "documents" | "web" | "ai_knowledge" | string
  citations: Citation[]
  trace: string[]
  confidence: number
  grounded: boolean
  follow_up_questions: string[]
  response_time_ms: number
}

// ---------- API calls ----------
export const pingBackend = () => api.get("/health").catch(() => {})

export const authApi = {
  signup: (email: string, password: string, full_name: string) =>
    api.post<{ access_token: string }>("/auth/signup", { email, password, full_name }),
  login: (email: string, password: string) =>
    api.post<{ access_token: string }>("/auth/login", { email, password }),
  me: () => api.get<User>("/auth/me"),
}

export const chatsApi = {
  list: () => api.get<Session[]>("/sessions"),
  remove: (id: string) => api.delete(`/sessions/${id}`),
  documents: (id: string) => api.get<DocumentItem[]>(`/sessions/${id}/documents`),
  deleteDocument: (id: string, documentId: string) =>
    api.delete(`/sessions/${id}/documents/${documentId}`),
  messages: (id: string) => api.get<Message[]>(`/sessions/${id}/messages`),
}

export function uploadFiles(files: File[], sessionId?: string) {
  const form = new FormData()
  files.forEach((file) => form.append("files", file))
  if (sessionId) form.append("session_id", sessionId)
  return api.post<{ session_id: string; chunk_count: number; trace: string[] }>("/uploads", form)
}

export function askQuestion(sessionId: string, question: string) {
  return api.post<Omit<Message, "id"> & { session_id: string }>("/chat", {
    session_id: sessionId,
    question,
  })
}
