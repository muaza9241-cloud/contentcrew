import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const frontendDir = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(frontendDir, "..");

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, rootDir, "");
  const port = Number(env.FRONTEND_PORT || 5173);

  return {
    root: frontendDir,
    envDir: rootDir,
    plugins: [react()],
    server: {
      port,
      proxy: {
        "/api": {
          target: env.VITE_API_URL || "http://127.0.0.1:8000",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
    build: {
      outDir: resolve(frontendDir, "dist"),
      emptyOutDir: true,
    },
  };
});
