"""
FairLens AI — Scan Routes
API endpoints for uploading datasets and triggering bias scans.
"""
import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from services.bias_engine import compute_fairness_metrics
from services.gemini_service import generate_audit_report, get_remediation_recommendation

router = APIRouter()


@router.post("/upload")
async def scan_dataset(
    file: UploadFile = File(...),
    protected_attribute: str = Form(...),
    target_variable: str = Form(...),
    domain: str = Form(default="general")
):
    """
    Upload a CSV dataset and run a full fairness bias scan.

    - **file**: CSV file with the dataset
    - **protected_attribute**: Column name of the sensitive attribute (e.g. 'gender', 'race')
    - **target_variable**: Column name of the outcome to audit (e.g. 'hired', 'loan_approved')
    - **domain**: Context template — 'hiring', 'credit', 'healthcare', 'general'
    """
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    # Read CSV
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    # Validate columns exist
    if protected_attribute not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{protected_attribute}' not found. Available: {list(df.columns)}"
        )
    if target_variable not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{target_variable}' not found. Available: {list(df.columns)}"
        )

    # Run bias scan
    scan_result = compute_fairness_metrics(df, protected_attribute, target_variable)

    # Get Gemini analysis
    gemini_report = generate_audit_report(scan_result)
    remediation = get_remediation_recommendation(scan_result)

    scan_result.gemini_analysis = gemini_report
    scan_result.recommended_fix = remediation.get("algorithm", "Reweighing")

    return JSONResponse({
        "scan_id": f"scan_{hash(file.filename)}",
        "dataset_name": file.filename,
        "total_rows": scan_result.total_rows,
        "protected_attribute": scan_result.protected_attribute,
        "target_variable": scan_result.target_variable,
        "overall_severity": scan_result.overall_severity,
        "metrics": [
            {
                "name": m.metric_name,
                "value": m.value,
                "threshold": m.threshold,
                "status": m.status,
                "description": m.description
            }
            for m in scan_result.metrics
        ],
        "gemini_analysis": gemini_report,
        "remediation": remediation,
        "domain": domain
    })


@router.post("/model-endpoint")
async def scan_model_endpoint(
    endpoint_url: str = Form(...),
    sample_data: UploadFile = File(...),
    protected_attribute: str = Form(...),
    target_variable: str = Form(...)
):
    """
    Scan a live model API endpoint by sending sample data and capturing predictions.
    """
    # TODO: Implement live model endpoint scanning
    # 1. Send rows from sample_data to endpoint_url
    # 2. Collect predictions
    # 3. Attach predictions to dataframe as target_variable
    # 4. Run compute_fairness_metrics
    return {"message": "Model endpoint scanning — coming in Phase 2"}


@router.get("/history")
async def get_scan_history(user_id: str):
    """
    Retrieve audit history for a user from BigQuery.
    """
    # TODO: Query BigQuery for past scans by user_id
    return {"scans": [], "message": "BigQuery integration active in production"}
