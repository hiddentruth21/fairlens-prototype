import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import ScanResults from "./pages/ScanResults";
import Remediation from "./pages/Remediation";
import UploadPage from "./pages/UploadPage";

export default function App() {
  const [scanResult, setScanResult] = useState(null);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route
              path="/upload"
              element={<UploadPage onScanComplete={setScanResult} />}
            />
            <Route
              path="/results"
              element={<ScanResults result={scanResult} />}
            />
            <Route
              path="/remediation"
              element={<Remediation result={scanResult} />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
