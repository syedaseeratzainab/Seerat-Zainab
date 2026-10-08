import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Local dev: requests to /api go to the FastAPI backend on port 8000.
    // In production (Railway) the frontend calls VITE_API_BASE_URL directly instead.
    proxy: {
      "/api": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
})
