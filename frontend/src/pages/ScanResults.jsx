import { useNavigate } from "react-router-dom";

const STATUS_CONFIG = {
  FAIR:     { color: "bg-green-100 text-green-800 border-green-200",  badge: "bg-green-500",  icon: "✅" },
  AT_RISK:  { color: "bg-yellow-100 text-yellow-800 border-yellow-200", badge: "bg-yellow-500", icon: "⚠️" },
  BIASED:   { color: "bg-orange-100 text-orange-800 border-orange-200", badge: "bg-orange-500", icon: "🚨" },
  CRITICAL: { color: "bg-red-100 text-red-800 border-red-200",        badge: "bg-red-600",    icon: "🔴" },
};

function MetricCard({ metric }) {
  const cfg = STATUS_CONFIG[metric.status] || STATUS_CONFIG.FAIR;
  const pct = Math.min(100, (metric.value / (metric.threshold * 2)) * 100);

  return (
    <div className={`border rounded-xl p-5 ${cfg.color}`}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <p className="font-semibold text-sm">{metric.name}</p>
          <p className="text-2xl font-bold mt-1">{metric.value.toFixed(3)}</p>
        </div>
        <span className="text-2xl">{cfg.icon}</span>
      </div>
      <div className="w-full bg-white/60 rounded-full h-2 mb-2">
        <div
          className={`h-2 rounded-full ${cfg.badge}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs opacity-75">Threshold: {metric.threshold}</p>
    </div>
  );
}

export default function ScanResults({ result }) {
  const navigate = useNavigate();

  if (!result) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-500 text-lg">No scan results yet.</p>
        <button
          onClick={() => navigate("/upload")}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg"
        >
          Run a Scan
        </button>
      </div>
    );
  }

  const overallCfg = STATUS_CONFIG[result.overall_severity] || STATUS_CONFIG.FAIR;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Bias Scan Results</h1>
          <p className="text-gray-500 mt-1">
            {result.dataset_name} · {result.total_rows?.toLocaleString()} rows ·
            Protected: <strong>{result.protected_attribute}</strong> ·
            Target: <strong>{result.target_variable}</strong>
          </p>
        </div>
        <div className={`px-4 py-2 rounded-full text-sm font-bold border ${overallCfg.color}`}>
          {overallCfg.icon} {result.overall_severity}
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {result.metrics?.map((m) => <MetricCard key={m.name} metric={m} />)}
      </div>

      {/* Gemini Analysis */}
      {result.gemini_analysis && (
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-2xl">✨</span>
            <h2 className="font-bold text-blue-900 text-lg">Gemini AI Analysis</h2>
          </div>
          <p className="text-blue-900 whitespace-pre-wrap text-sm leading-relaxed">
            {result.gemini_analysis}
          </p>
        </div>
      )}

      {/* Remediation CTA */}
      {result.remediation && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="font-bold text-gray-900 text-lg mb-2">
            🔧 Recommended Fix: {result.remediation.algorithm}
          </h2>
          <p className="text-gray-600 text-sm mb-3">{result.remediation.reason}</p>
          <div className="flex gap-4 text-sm text-gray-500">
            <span>📈 Expected improvement: {result.remediation.expected_improvement}</span>
            <span>🔨 Effort: {result.remediation.implementation_effort}</span>
          </div>
          <button
            onClick={() => navigate("/remediation")}
            className="mt-4 bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
          >
            View Debiasing Code →
          </button>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        <button
          onClick={() => navigate("/upload")}
          className="border border-gray-300 text-gray-700 px-5 py-2 rounded-lg hover:bg-gray-50"
        >
          ← New Scan
        </button>
        <button
          className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
          onClick={() => alert("PDF export — available in full deployment")}
        >
          📄 Export Compliance PDF
        </button>
      </div>
    </div>
  );
}
