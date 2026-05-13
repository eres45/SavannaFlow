"use client";

import React, { useState } from 'react';

interface Metric {
  label: string;
  value: string | number;
}

interface PipelineResult {
  name: string;
  answer: string;
  metrics: Metric[];
}

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<PipelineResult[]>([
    {
      name: "LLM Only",
      answer: "No query initiated. Awaiting mission parameters...",
      metrics: [
        { label: "Tokens", value: "---" },
        { label: "Latency", value: "---" },
        { label: "Cost", value: "---" },
        { label: "Accuracy", value: "---" },
      ]
    },
    {
      name: "Basic RAG",
      answer: "Standing by. Vector database indexed and ready.",
      metrics: [
        { label: "Tokens", value: "---" },
        { label: "Latency", value: "---" },
        { label: "Cost", value: "---" },
        { label: "Accuracy", value: "---" },
      ]
    },
    {
      name: "GraphRAG",
      answer: "TigerGraph Knowledge Graph online. Ready for complex inference.",
      metrics: [
        { label: "Tokens", value: "---" },
        { label: "Latency", value: "---" },
        { label: "Cost", value: "---" },
        { label: "Accuracy", value: "---" },
      ]
    }
  ]);

  const handleSend = async () => {
    if (!query) return;
    setLoading(true);
    
    try {
      const apiHost = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiHost}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      
      const data = await response.json();
      if (data.results) {
        setResults(data.results);
      }
    } catch (error) {
      console.error("Failed to fetch results:", error);
      // Fallback or error state
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="command-center">
      <header>
        <div className="brand">
          <div className="status-dot"></div>
          <h1>SAVANNAFLOW // INFERENCE_ENGINE</h1>
        </div>
        <div className="status-badge">
          SYSTEM_STATUS: <span style={{color: '#10b981', marginLeft: '5px'}}>NOMINAL</span>
        </div>
      </header>

      <section className="pipeline-grid">
        {results.map((res, i) => (
          <div key={i} className="pipeline-card">
            <div className="card-header">
              <h2>{res.name}</h2>
            </div>
            <div className="card-content">
              {loading ? (
                <div style={{color: 'var(--text-secondary)', fontStyle: 'italic'}}>Processing inference...</div>
              ) : (
                <p>{res.answer}</p>
              )}
            </div>
            <div className="card-footer">
              {res.metrics.map((m, j) => (
                <div key={j} className="metric-item">
                  <span className="metric-label">{m.label}</span>
                  <span className="metric-value">{m.value}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>

      <div className="query-bar">
        <input 
          type="text" 
          className="query-input" 
          placeholder="Enter mission query (e.g., 'How does the HLS affect Artemis III timeline?')..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="send-btn" onClick={handleSend} disabled={loading}>
          {loading ? "BUSY..." : "EXECUTE"}
        </button>
      </div>
    </main>
  );
}
