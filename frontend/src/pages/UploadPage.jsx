import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

const DOMAIN_OPTIONS = [
  { value: "hiring", label: "🧑‍💼 Hiring & Recruitment" },
  { value: "credit", label: "💳 Credit & Lending" },
  { value: "healthcare", label: "🏥 Healthcare Triage" },
  { value: "criminal_justice", label: "⚖️ Criminal Justice" },
  { value: "general", label: "🔍 General Purpose" },
];

export default function UploadPage({ onScanComplete }) {
  const [file, setFile] = useState(null);
  const [protectedAttr, setProtectedAttr] = useState("");
  const [targetVar, setTargetVar] = useState("");
  const [domain, setDomain] = useState("general");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();
  const navigate = useNavigate();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped?.name.endsWith(".csv")) setFile(dropped);
    else setError("Only CSV files are supported.");
  };

  const handleScan = async () => {
    if (!file || !protectedAttr || !targetVar) {
      setError("Please fill in all fields and upload a CSV file.");
      return;
    }
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("protected_attribute", protectedAttr);
    formData.append("target_variable", targetVar);
    formData.append("domain", domain);

    try {
      const res = await fetch(
        `${process.env.REACT_APP_API_URL}/api/scan/upload`,
        { method: "POST", body: formData }
      );
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      onScanComplete(data);
      navigate("/results");
    } catch (err) {
      setError(`Scan failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Start a Bias Scan</h1>
      <p className="text-gray-500 mb-8">
        Upload your dataset and FairLens AI will compute 8 fairness metrics powered by Vertex AI,
        then generate a plain-English audit report using Gemini.
      </p>

      {/* Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer mb-6 transition-colors
          ${dragOver ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-400"}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileRef.current.click()}
      >
        <input
          ref={fileRef}
          type="file"
          accept=".csv"
          className="hidden"
          onChange={(e) => setFile(e.target.files[0])}
        />
        {file ? (
          <div>
            <p className="text-2xl mb-2">✅</p>
            <p className="font-semibold text-gray-800">{file.name}</p>
            <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
          </div>
        ) : (
          <div>
            <p className="text-4xl mb-3">📂</p>
            <p className="font-semibold text-gray-700">Drop your CSV here or click to browse</p>
            <p className="text-sm text-gray-400 mt-1">Supports CSV files up to 50MB</p>
          </div>
        )}
      </div>

      {/* Configuration */}
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">
            Protected Attribute (sensitive column)
          </label>
          <input
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            placeholder="e.g.  gender, race, age"
            value={protectedAttr}
            onChange={(e) => setProtectedAttr(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">
            Target Variable (outcome column)
          </label>
          <input
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            placeholder="e.g.  hired, loan_approved, income"
            value={targetVar}
            onChange={(e) => setTargetVar(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">
            Domain Template
          </label>
          <select
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
          >
            {DOMAIN_OPTIONS.map((d) => (
              <option key={d.value} value={d.value}>{d.label}</option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm mb-4">
          {error}
        </div>
      )}

      <button
        onClick={handleScan}
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold
                   py-3 rounded-xl transition-colors text-lg"
      >
        {loading ? "🔍 Scanning with Vertex AI + Gemini..." : "🚀 Run Bias Scan"}
      </button>
    </div>
  );
}
