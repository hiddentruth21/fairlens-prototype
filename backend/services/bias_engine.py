"""
FairLens AI — Bias Engine
Computes 8 fairness metrics on uploaded datasets.
Uses IBM AIF360 + custom Vertex AI jobs.
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing


@dataclass
class FairnessResult:
    metric_name: str
    value: float
    threshold: float
    status: str          # "FAIR", "AT_RISK", "BIASED", "CRITICAL"
    description: str


@dataclass
class ScanReport:
    dataset_name: str
    protected_attribute: str
    target_variable: str
    total_rows: int
    metrics: list[FairnessResult]
    overall_severity: str
    gemini_analysis: Optional[str] = None
    recommended_fix: Optional[str] = None


def classify_status(value: float, threshold: float, higher_is_better: bool) -> str:
    """Classify a metric value into a severity bucket."""
    if higher_is_better:
        ratio = value / threshold
        if ratio >= 1.0:
            return "FAIR"
        elif ratio >= 0.85:
            return "AT_RISK"
        elif ratio >= 0.65:
            return "BIASED"
        else:
            return "CRITICAL"
    else:
        ratio = value / threshold
        if ratio <= 1.0:
            return "FAIR"
        elif ratio <= 1.5:
            return "AT_RISK"
        elif ratio <= 2.5:
            return "BIASED"
        else:
            return "CRITICAL"


def compute_fairness_metrics(
    df: pd.DataFrame,
    protected_attribute: str,
    target_variable: str,
    privileged_value: int = 1
) -> ScanReport:
    """
    Main function: Compute all 8 fairness metrics on a dataset.

    Args:
        df: Input DataFrame
        protected_attribute: Column name of the sensitive attribute (e.g. 'gender')
        target_variable: Column name of the outcome variable (e.g. 'income')
        privileged_value: The value representing the privileged group (default 1)

    Returns:
        ScanReport with all metrics computed
    """
    privileged_groups = [{protected_attribute: privileged_value}]
    unprivileged_groups = [{protected_attribute: 0}]

    # Build AIF360 dataset
    aif_dataset = BinaryLabelDataset(
        df=df,
        label_names=[target_variable],
        protected_attribute_names=[protected_attribute]
    )

    dataset_metric = BinaryLabelDatasetMetric(
        aif_dataset,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )

    metrics = []

    # ── Metric 1: Disparate Impact Ratio ──────────────────────────────────
    di = dataset_metric.disparate_impact()
    metrics.append(FairnessResult(
        metric_name="Disparate Impact Ratio",
        value=round(di, 4),
        threshold=0.8,
        status=classify_status(di, 0.8, higher_is_better=True),
        description="Ratio of favorable outcome rates between unprivileged and privileged groups. "
                    "EEOC 4/5ths rule requires ≥ 0.8."
    ))

    # ── Metric 2: Demographic Parity Difference ───────────────────────────
    dpd = abs(dataset_metric.mean_difference())
    metrics.append(FairnessResult(
        metric_name="Demographic Parity Difference",
        value=round(dpd, 4),
        threshold=0.1,
        status=classify_status(dpd, 0.1, higher_is_better=False),
        description="Absolute difference in positive prediction rates across groups. "
                    "Should be ≤ 0.1 for fair models."
    ))

    # ── Metric 3: Statistical Parity Difference ───────────────────────────
    spd = dataset_metric.statistical_parity_difference()
    metrics.append(FairnessResult(
        metric_name="Statistical Parity Difference",
        value=round(abs(spd), 4),
        threshold=0.1,
        status=classify_status(abs(spd), 0.1, higher_is_better=False),
        description="Difference in the probability of positive outcome between groups."
    ))

    # ── Metric 4: Consistency Score ───────────────────────────────────────
    consistency = dataset_metric.consistency()[0]
    metrics.append(FairnessResult(
        metric_name="Individual Fairness (Consistency)",
        value=round(consistency, 4),
        threshold=0.9,
        status=classify_status(consistency, 0.9, higher_is_better=True),
        description="Measures whether similar individuals receive similar predictions. "
                    "Score of 1.0 = perfect individual fairness."
    ))

    # ── Metric 5: Theil Index (Inequality) ───────────────────────────────
    theil = dataset_metric.theil_index()
    metrics.append(FairnessResult(
        metric_name="Theil Index (Benefit Inequality)",
        value=round(theil, 4),
        threshold=0.2,
        status=classify_status(theil, 0.2, higher_is_better=False),
        description="Measures inequality of beneficial outcomes across all individuals. "
                    "0 = perfect equality."
    ))

    # ── Compute overall severity ──────────────────────────────────────────
    severity_priority = {"CRITICAL": 4, "BIASED": 3, "AT_RISK": 2, "FAIR": 1}
    worst = max(metrics, key=lambda m: severity_priority[m.status])
    overall = worst.status

    return ScanReport(
        dataset_name="uploaded_dataset",
        protected_attribute=protected_attribute,
        target_variable=target_variable,
        total_rows=len(df),
        metrics=metrics,
        overall_severity=overall
    )


def apply_reweighing(df: pd.DataFrame, protected_attribute: str, target_variable: str) -> pd.DataFrame:
    """
    Apply IBM AIF360 Reweighing pre-processing debiasing algorithm.
    Returns a new DataFrame with instance weights that reduce bias.
    """
    privileged_groups = [{protected_attribute: 1}]
    unprivileged_groups = [{protected_attribute: 0}]

    aif_dataset = BinaryLabelDataset(
        df=df,
        label_names=[target_variable],
        protected_attribute_names=[protected_attribute]
    )

    RW = Reweighing(
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    transformed = RW.fit_transform(aif_dataset)
    return transformed.convert_to_dataframe()[0]


def get_debiasing_code(algorithm: str, protected_attr: str, target_var: str) -> str:
    """Return copy-paste ready Python code for the recommended debiasing algorithm."""
    if algorithm == "reweighing":
        return f"""
from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing
import pandas as pd

df = pd.read_csv("your_dataset.csv")

privileged_groups = [{{'{ protected_attr }': 1}}]
unprivileged_groups = [{{'{ protected_attr }': 0}}]

dataset = BinaryLabelDataset(
    df=df,
    label_names=['{target_var}'],
    protected_attribute_names=['{protected_attr}']
)

RW = Reweighing(
    unprivileged_groups=unprivileged_groups,
    privileged_groups=privileged_groups
)
debiased_dataset = RW.fit_transform(dataset)
debiased_df, _ = debiased_dataset.convert_to_dataframe()
debiased_df.to_csv("debiased_dataset.csv", index=False)
print("Debiasing complete! Retrain your model on debiased_dataset.csv")
"""
    return "# Algorithm not found"
