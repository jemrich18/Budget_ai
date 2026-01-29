import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
  },
  preview: {
    host: true,
    allowedHosts: [
      "zippy-joy-production-1d15.up.railway.app",
    ],
  },
});
