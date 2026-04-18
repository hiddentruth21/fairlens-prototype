import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 0" }}>
      <h1 style={{ fontSize: "28px", fontWeight: 500, marginBottom: "8px" }}>FairLens AI</h1>
      <p style={{ color: "#64748b", marginBottom: "2rem" }}>
        Real-time bias detection and fairness auditing powered by Google Gemini 1.5 Pro and Vertex AI.
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px", marginBottom: "2rem" }}>
        {[
          { label: "Total Scans", value: "0" },
          { label: "Datasets Audited", value: "0" },
          { label: "Critical Issues Found", value: "0" },
          { label: "Reports Generated", value: "0" },
        ].map((stat) => (
          <div key={stat.label} style={{ background: "#f8fafc", borderRadius: "12px", padding: "1rem", border: "0.5px solid #e2e8f0" }}>
            <p style={{ fontSize: "12px", color: "#64748b", margin: "0 0 4px" }}>{stat.label}</p>
            <p style={{ fontSize: "28px", fontWeight: 500, margin: 0 }}>{stat.value}</p>
          </div>
        ))}
      </div>
      <button
        onClick={() => navigate("/upload")}
        style={{ background: "#2563eb", color: "#fff", border: "none", borderRadius: "10px", padding: "12px 28px", fontSize: "15px", cursor: "pointer" }}
      >
        Start a Bias Scan
      </button>
    </div>
  );
}
