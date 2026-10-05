import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

export default function App() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setHealth)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <main className="page">
      <h1>ContentCrew</h1>
      <p>Frontend workspace for content production.</p>
      {health ? (
        <p className="ok">API: {health.status}</p>
      ) : (
        <p className="muted">{error || "Checking API…"}</p>
      )}
    </main>
  );
}
