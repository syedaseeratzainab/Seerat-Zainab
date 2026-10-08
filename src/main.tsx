import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import App from "./App"
import { pingBackend } from "./api"
import "./styles.css"

// Wake the backend as soon as the page opens. If Railway put it to sleep,
// this request starts it up while the user is still logging in.
pingBackend()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)
