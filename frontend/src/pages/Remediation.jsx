import { useNavigate } from "react-router-dom";

export default function Remediation({ result }) {
  const navigate = useNavigate();

  if (!result) {
    return (
      <div style={{ textAlign: "center", padding: "4rem 0" }}>
        <p style={{ color: "#64748b" }}>No scan results yet.</p>
        <button onClick={() => navigate("/upload")} style={{ marginTop: "1rem", background: "#2563eb", color: "#fff", border: "none", borderRadius: "8px", padding: "8px 20px", cursor: "pointer" }}>
          Run a Scan
        </button>
      </div>
    );
  }

  const algorithm = result?.remediation?.algorithm || "Reweighing";
  const code = `from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing
import pandas as pd

df = pd.read_csv("your_dataset.csv")
privileged_groups = [{'${result.protected_attribute}': 1}]
unprivileged_groups = [{'${result.protected_attribute}': 0}]

dataset = BinaryLabelDataset(
    df=df,
    label_names=['${result.target_variable}'],
    protected_attribute_names=['${result.protected_attribute}']
)

RW = Reweighing(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
debiased_dataset = RW.fit_transform(dataset)
debiased_df, _ = debiased_dataset.convert_to_dataframe()
debiased_df.to_csv("debiased_dataset.csv", index=False)
print("Retrain your model on debiased_dataset.csv")`;

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "24px", fontWeight: 500, marginBottom: "8px" }}>Remediation</h1>
      <p style={{ color: "#64748b", marginBottom: "1.5rem" }}>Recommended fix: <strong>{algorithm}</strong></p>
      <div style={{ background: "#0f172a", borderRadius: "12px", padding: "1.25rem", marginBottom: "1.5rem" }}>
        <p style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "8px" }}>Python — copy and run this code</p>
        <pre style={{ color: "#e2e8f0", fontSize: "12px", margin: 0, lineHeight: 1.8, overflowX: "auto" }}>{code}</pre>
      </div>
      <button onClick={() => navigate("/results")} style={{ border: "0.5px solid #e2e8f0", background: "transparent", borderRadius: "8px", padding: "8px 20px", cursor: "pointer" }}>
        Back to Results
      </button>
    </div>
  );
}
