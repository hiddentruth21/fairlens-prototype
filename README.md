# 🔍 FairLens AI — Bias Detection & Fairness Auditing Platform

> **Solution Challenge 2026 | [Unbiased AI Decision] Ensuring Fairness and Detecting Bias in Automated Decisions**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-fairlens--ai.web.app-blue?style=for-the-badge)](https://fairlens-ai.web.app)
[![Demo Video](https://img.shields.io/badge/Demo%20Video-YouTube-red?style=for-the-badge)](https://youtu.be/fairlens-ai-demo-2026)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange?style=for-the-badge)](https://deepmind.google/technologies/gemini/)

---

## 🚨 Problem Statement

AI systems used in **hiring, lending, healthcare, and criminal justice** encode historical biases from training data — leading to discriminatory outcomes for women, minorities, and marginalized communities.

- **76%** of HR teams use AI screening tools with no fairness auditing
- Biased credit models deny loans to qualified applicants from underrepresented groups
- Healthcare AI misdiagnoses patients of color at 3x higher rates
- No accessible, no-code tool exists for non-technical compliance officers to audit AI fairness

---

## 💡 Solution Overview

**FairLens AI** is a real-time bias detection and fairness auditing platform powered by **Google Gemini 1.5 Pro** and **Vertex AI**.

### How It Works:
1. **Upload** your dataset (CSV) or connect a live model API endpoint
2. **Select** protected attributes (gender, race, age) and target variable
3. **Scan** — Vertex AI computes 8 fairness metrics automatically
4. **Explain** — Gemini 1.5 Pro generates plain-English audit reports with root cause analysis
5. **Fix** — Debiasing recommendations with copy-paste Python code
6. **Report** — Auto-generate compliance-ready PDF for EEOC / RBI / EU AI Act

### Key Differentiators:
| Feature | FairLens AI | IBM AIF360 | Google What-If Tool |
|---|---|---|---|
| No-code interface | ✅ | ❌ | ❌ |
| Plain-English reports (Gemini) | ✅ | ❌ | ❌ |
| Auto debiasing suggestions | ✅ | Manual | ❌ |
| Compliance PDF export | ✅ | ❌ | ❌ |
| Multi-domain templates | ✅ | ❌ | ❌ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React.js)                      │
│              Deployed on Firebase Hosting                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────┐
│                  BACKEND API (FastAPI)                       │
│                  Cloud Run (Containerized)                   │
├─────────────┬────────────────┬───────────────────────────────┤
│ Firebase    │  Cloud Storage │  BigQuery                    │
│ Auth (SSO)  │  (Datasets)    │  (Audit Logs)                │
└─────────────┴────────┬───────┴───────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  AI/ML CORE                                  │
│  Vertex AI Custom Jobs  │  Gemini 1.5 Pro API               │
│  (Bias Metrics)         │  (Report Generation)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Cloud account with billing enabled
- Gemini API key

### 1. Clone the Repository
```bash
git clone https://github.com/fairlens-ai/fairlens-prototype.git
cd fairlens-prototype
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY and GCP_PROJECT_ID to .env
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Add REACT_APP_API_URL=http://localhost:8000
npm start
```

### 4. Open in Browser
```
http://localhost:3000
```

---

## 📁 Project Structure

```
fairlens-prototype/
├── frontend/                  # React.js dashboard
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── BiasScoreCard.jsx
│   │   │   ├── MetricChart.jsx
│   │   │   └── UploadZone.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ScanResults.jsx
│   │   │   └── Remediation.jsx
│   │   └── App.jsx
│   └── package.json
├── backend/                   # FastAPI Python backend
│   ├── main.py                # App entry point
│   ├── routes/
│   │   ├── scan.py            # Bias scan endpoints
│   │   ├── report.py          # PDF report generation
│   │   └── remediation.py     # Debiasing suggestions
│   ├── services/
│   │   ├── bias_engine.py     # Fairness metric computation
│   │   ├── gemini_service.py  # Gemini API integration
│   │   └── pdf_generator.py   # Compliance PDF export
│   ├── requirements.txt
│   └── Dockerfile
├── docs/
│   └── architecture.md
├── tests/
│   ├── test_bias_engine.py
│   └── test_gemini_service.py
├── docker-compose.yml
└── README.md
```

---

## 🔬 Fairness Metrics Computed

| Metric | Description | Threshold |
|---|---|---|
| **Disparate Impact Ratio** | Ratio of favorable outcomes across groups | ≥ 0.8 (EEOC 4/5ths rule) |
| **Demographic Parity Difference** | Gap in prediction rates | ≤ 0.1 |
| **Equalized Odds Difference** | TPR/FPR gap across groups | ≤ 0.1 |
| **Predictive Parity** | Precision gap across groups | ≤ 0.1 |
| **Calibration Error** | Confidence calibration by group | ≤ 0.05 |
| **Individual Fairness Score** | Similar people get similar predictions | ≥ 0.9 |
| **Counterfactual Fairness** | Outcome changes if group attribute flipped | Binary pass/fail |
| **Theil Index** | Overall inequality of benefit distribution | ≤ 0.2 |

---

## 🌐 Google Cloud & AI Services Used

- **Google Gemini 1.5 Pro** — Plain-English report generation & root cause analysis
- **Vertex AI** — Custom bias computation jobs & model registry
- **Cloud Run** — Serverless containerized backend API
- **Cloud Storage** — Secure dataset uploads
- **BigQuery** — Audit log warehouse & historical metrics
- **Firebase Auth** — Google SSO authentication
- **Firebase Hosting** — Frontend deployment
- **Cloud Functions** — PDF generation triggers
- **Pub/Sub** — Compliance alert notifications

---

## 📊 Sample Output

**Dataset:** UCI Adult Income (48,842 rows)
**Protected Attribute:** Gender (Male/Female)

```
Fairness Audit Report — FairLens AI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Disparate Impact Ratio:        0.36  ❌ CRITICAL (threshold: ≥ 0.8)
Demographic Parity Difference: 0.19  ⚠️  HIGH RISK (threshold: ≤ 0.1)
Equalized Odds Difference:     0.08  ✅ ACCEPTABLE (threshold: ≤ 0.1)

Gemini Analysis:
"The model predicts high income for male applicants 2.8x more often than
female applicants with identical qualifications. The primary bias source
is the 'occupation' feature, which acts as a proxy for gender due to
historical workplace segregation in the 1994 training data."

Recommended Fix: Reweighing Algorithm
Estimated fairness improvement: +0.44 on Disparate Impact Ratio
```

---

## 👥 Team

**Team Name:** FairLens AI
**Team Leader:** Vaishnavi Gade
**Event:** Solution Challenge 2026 — Build with AI (Hack2Skill × Google)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
