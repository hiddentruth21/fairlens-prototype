const STATUS_COLORS = {
  FAIR:     { bg: "#f0fdf4", text: "#166534", border: "#bbf7d0" },
  AT_RISK:  { bg: "#fffbeb", text: "#92400e", border: "#fde68a" },
  BIASED:   { bg: "#fff7ed", text: "#9a3412", border: "#fed7aa" },
  CRITICAL: { bg: "#fef2f2", text: "#991b1b", border: "#fecaca" },
};

export default function BiasScoreCard({ metric }) {
  const colors = STATUS_COLORS[metric.status] || STATUS_COLORS.FAIR;
  return (
    <div style={{ background: colors.bg, border: `0.5px solid ${colors.border}`, borderRadius: "12px", padding: "1rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
        <p style={{ fontSize: "13px", fontWeight: 500, color: colors.text, margin: 0 }}>{metric.name}</p>
        <span style={{ fontSize: "11px", background: colors.border, color: colors.text, padding: "2px 8px", borderRadius: "20px" }}>{metric.status}</span>
      </div>
      <p style={{ fontSize: "28px", fontWeight: 500, color: colors.text, margin: "0 0 4px" }}>{metric.value?.toFixed(3)}</p>
      <p style={{ fontSize: "11px", color: colors.text, opacity: 0.7, margin: 0 }}>Threshold: {metric.threshold}</p>
    </div>
  );
}
