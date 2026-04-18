import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();
  const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/upload", label: "New Scan" },
    { path: "/results", label: "Results" },
    { path: "/remediation", label: "Remediation" },
  ];

  return (
    <nav style={{ background: "#0f172a", padding: "0 2rem", display: "flex", alignItems: "center", gap: "2rem", height: "56px" }}>
      <span style={{ color: "#60a5fa", fontWeight: 500, fontSize: "16px" }}>FairLens AI</span>
      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          style={{
            color: location.pathname === item.path ? "#ffffff" : "#94a3b8",
            fontSize: "14px",
            textDecoration: "none",
          }}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
