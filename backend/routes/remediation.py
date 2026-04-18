"""
FairLens AI — Remediation Routes
Returns debiasing algorithm recommendations and code snippets.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from services.bias_engine import get_debiasing_code

router = APIRouter()

class RemediationRequest(BaseModel):
    protected_attribute: str
    target_variable: str
    algorithm: str = "reweighing"

@router.post("/code")
def get_remediation_code(req: RemediationRequest):
    """Return copy-paste Python debiasing code for the recommended algorithm."""
    code = get_debiasing_code(req.algorithm, req.protected_attribute, req.target_variable)
    return {
        "algorithm": req.algorithm,
        "code": code,
        "instructions": "Run this code on your dataset, then retrain your model on the output."
    }

@router.get("/algorithms")
def list_algorithms():
    """List all supported debiasing algorithms."""
    return {
        "algorithms": [
            {
                "id": "reweighing",
                "name": "Reweighing",
                "type": "Pre-processing",
                "effort": "Low",
                "description": "Assigns weights to training examples to reduce bias before model training."
            },
            {
                "id": "adversarial_debiasing",
                "name": "Adversarial Debiasing",
                "type": "In-processing",
                "effort": "Medium",
                "description": "Trains model to maximize accuracy while minimizing ability to predict protected attribute."
            },
            {
                "id": "calibrated_eq_odds",
                "name": "Calibrated Equalized Odds",
                "type": "Post-processing",
                "effort": "Low",
                "description": "Adjusts model predictions after training to equalize error rates across groups."
            }
        ]
    }
