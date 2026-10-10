import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const SERVER_URL = "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    // Same-origin calls in the browser, so the server needs no CORS setup.
    proxy: {
      "/api": {
        target: SERVER_URL,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
