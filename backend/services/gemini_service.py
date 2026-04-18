"""
FairLens AI — Gemini Service
Uses Google Gemini 1.5 Pro to generate plain-English audit reports
and root cause analysis from raw fairness metrics.
"""
import os
import json
import google.generativeai as genai
from services.bias_engine import ScanReport


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")


AUDIT_PROMPT_TEMPLATE = """
You are an expert AI ethics auditor. Analyze the following fairness scan results
and provide a clear, actionable audit report for a non-technical compliance officer.

SCAN RESULTS:
- Dataset: {dataset_name} ({total_rows} rows)
- Protected Attribute: {protected_attribute}
- Target Variable: {target_variable}
- Overall Severity: {overall_severity}

FAIRNESS METRICS:
{metrics_json}

Please provide:
1. PLAIN ENGLISH SUMMARY (2-3 sentences explaining what the bias means in real-world terms)
2. ROOT CAUSE ANALYSIS (Why does this bias likely exist? What in the training data causes it?)
3. BUSINESS IMPACT (What groups are harmed and how? What legal/regulatory risk does this create?)
4. RECOMMENDED ACTION (Which debiasing algorithm should they apply and why?)

Be specific, empathetic, and actionable. Avoid jargon. Write as if explaining to a senior HR executive.
"""

REMEDIATION_PROMPT_TEMPLATE = """
You are an AI fairness engineer. Based on these bias metrics, recommend the single best
debiasing approach from: [Reweighing, Adversarial Debiasing, Calibrated Equalized Odds,
Prejudice Remover, Learning Fair Representations].

METRICS:
{metrics_json}

Severity: {overall_severity}
Protected Attribute: {protected_attribute}

Respond in JSON format:
{{
  "algorithm": "<algorithm name>",
  "reason": "<2 sentence explanation>",
  "expected_improvement": "<estimated improvement in Disparate Impact Ratio>",
  "implementation_effort": "Low|Medium|High",
  "trade_off": "<accuracy vs fairness trade-off to expect>"
}}
"""


def generate_audit_report(scan_report: ScanReport) -> str:
    """
    Call Gemini 1.5 Pro to generate a plain-English audit report.

    Args:
        scan_report: Completed ScanReport with all metrics

    Returns:
        Natural language audit report string
    """
    metrics_json = json.dumps(
        [
            {
                "metric": m.metric_name,
                "value": m.value,
                "threshold": m.threshold,
                "status": m.status,
                "description": m.description
            }
            for m in scan_report.metrics
        ],
        indent=2
    )

    prompt = AUDIT_PROMPT_TEMPLATE.format(
        dataset_name=scan_report.dataset_name,
        total_rows=scan_report.total_rows,
        protected_attribute=scan_report.protected_attribute,
        target_variable=scan_report.target_variable,
        overall_severity=scan_report.overall_severity,
        metrics_json=metrics_json
    )

    response = model.generate_content(prompt)
    return response.text


def get_remediation_recommendation(scan_report: ScanReport) -> dict:
    """
    Call Gemini to recommend the best debiasing algorithm for this specific case.

    Returns:
        Dict with algorithm, reason, expected_improvement, trade_off
    """
    metrics_json = json.dumps(
        [{"metric": m.metric_name, "value": m.value, "status": m.status}
         for m in scan_report.metrics],
        indent=2
    )

    prompt = REMEDIATION_PROMPT_TEMPLATE.format(
        metrics_json=metrics_json,
        overall_severity=scan_report.overall_severity,
        protected_attribute=scan_report.protected_attribute
    )

    response = model.generate_content(prompt)

    # Parse JSON from Gemini response
    text = response.text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    return json.loads(text)


def generate_executive_summary(scan_report: ScanReport) -> str:
    """
    Generate a one-paragraph executive summary for the PDF compliance report.
    """
    prompt = f"""
    Write a one-paragraph executive summary (4-5 sentences) for a compliance PDF report.
    Dataset has {scan_report.total_rows} rows. Protected attribute: {scan_report.protected_attribute}.
    Overall bias severity: {scan_report.overall_severity}.
    Worst metric: {scan_report.metrics[0].metric_name} = {scan_report.metrics[0].value}
    (threshold: {scan_report.metrics[0].threshold}).
    Write in formal, professional language suitable for a regulatory submission.
    """
    response = model.generate_content(prompt)
    return response.text
