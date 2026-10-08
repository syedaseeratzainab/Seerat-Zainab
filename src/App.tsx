import type { ReactNode } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import { getToken } from "./api"
import AuthPage from "./pages/AuthPage"
import ChatPage from "./pages/ChatPage"

function RequireLogin({ children }: { children: ReactNode }) {
  return getToken() ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<AuthPage mode="login" />} />
      <Route path="/signup" element={<AuthPage mode="signup" />} />
      <Route path="/chat" element={<RequireLogin><ChatPage /></RequireLogin>} />
      <Route path="/chat/:sessionId" element={<RequireLogin><ChatPage /></RequireLogin>} />
      <Route path="*" element={<Navigate to={getToken() ? "/chat" : "/login"} replace />} />
    </Routes>
  )
}
