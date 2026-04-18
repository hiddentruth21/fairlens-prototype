"""
FairLens AI — Backend API
FastAPI application for bias detection and fairness auditing.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from routes import scan, report, remediation

app = FastAPI(
    title="FairLens AI API",
    description="Real-time bias detection and fairness auditing platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router, prefix="/api/scan", tags=["Bias Scan"])
app.include_router(report.router, prefix="/api/report", tags=["Reports"])
app.include_router(remediation.router, prefix="/api/remediation", tags=["Remediation"])


@app.get("/")
def root():
    return {
        "service": "FairLens AI",
        "version": "1.0.0",
        "status": "running",
        "description": "Bias detection & fairness auditing powered by Gemini + Vertex AI"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
