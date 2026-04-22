"""
Enterprise Bias Index (EBI) — FairLens proprietary scoring system.

A composite 0-100 score measuring enterprise AI fairness risk across
6 dimensions. Higher = fairer. Below 60 = regulatory risk.

EBI = Σ(dimension_score × weight) / Σ(weights)
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, List, Dict


THRESHOLDS = {
    "demographic_parity_difference": 0.10,
    "equalized_odds_difference": 0.10,
    "disparate_impact_ratio": 0.80,      # higher is better
    "calibration_error": 0.05,
    "theil_index": 0.10,
    "statistical_parity_difference": 0.10,
    "average_odds_difference": 0.10,
    "equal_opportunity_difference": 0.10,
}

RATIO_METRICS = {"disparate_impact_ratio"}  # higher is better

WEIGHTS = {
    "metric_coverage": 0.20,
    "severity_weighted": 0.25,
    "temporal_stability": 0.20,
    "intersectional": 0.15,
    "remediation_velocity": 0.10,
    "regulatory_alignment": 0.10,
}

RISK_TIERS = [
    (90, "GREEN",    "Excellent — exceeds regulatory standards"),
    (75, "AMBER",    "Good — minor improvements recommended"),
    (60, "RED",      "At Risk — regulatory exposure likely"),
    (0,  "CRITICAL", "Non-Compliant — immediate remediation required"),
]


@dataclass
class EBIResult:
    # Composite
    enterprise_bias_index: float      # 0-100
    risk_tier: str                    # GREEN / AMBER / RED / CRITICAL
    risk_description: str
    percentile_rank: float            # vs industry (simulated)
    
    # Dimension scores (0-100 each)
    metric_coverage_score: float
    severity_weighted_score: float
    temporal_stability_score: float
    intersectional_score: float
    remediation_velocity_score: float
    regulatory_alignment_score: float
    
    # Explainability
    biggest_risk_factor: str
    improvement_priority: List[str]
    
    def to_dict(self) -> dict:
        return {
            "enterprise_bias_index": round(self.enterprise_bias_index, 1),
            "risk_tier": self.risk_tier,
            "risk_description": self.risk_description,
            "percentile_rank": round(self.percentile_rank, 1),
            "dimensions": {
                "metric_coverage": round(self.metric_coverage_score, 1),
                "severity_weighted": round(self.severity_weighted_score, 1),
                "temporal_stability": round(self.temporal_stability_score, 1),
                "intersectional": round(self.intersectional_score, 1),
                "remediation_velocity": round(self.remediation_velocity_score, 1),
                "regulatory_alignment": round(self.regulatory_alignment_score, 1),
            },
            "biggest_risk_factor": self.biggest_risk_factor,
            "improvement_priority": self.improvement_priority,
        }


def compute_ebi(
    metrics: Dict[str, Dict[str, float]],
    trend: List[float],
    incidents: List[dict] = None,
    sensitive_cols: List[str] = None,
) -> EBIResult:
    """
    Compute the Enterprise Bias Index.
    """
    incidents = incidents or []
    sensitive_cols = sensitive_cols or []
    
    # ── Dimension 1: Metric Coverage (20%)
    passing = 0
    total = len(THRESHOLDS)
    for metric, threshold in THRESHOLDS.items():
        if metric not in metrics:
            continue
        values = list(metrics[metric].values())
        if not values:
            continue
        worst = max(values) if metric not in RATIO_METRICS else min(values)
        if metric in RATIO_METRICS:
            passing += 1 if worst >= threshold else 0
        else:
            passing += 1 if worst <= threshold else 0
    metric_coverage_score = (passing / total) * 100
    
    # ── Dimension 2: Severity Weighted Score (25%)
    violation_penalties = []
    for metric, threshold in THRESHOLDS.items():
        if metric not in metrics:
            continue
        values = list(metrics[metric].values())
        if not values:
            continue
        worst = max(values) if metric not in RATIO_METRICS else min(values)
        if metric in RATIO_METRICS:
            if worst < threshold:
                gap = (threshold - worst) / threshold
                violation_penalties.append(gap)
        else:
            if worst > threshold:
                gap = (worst - threshold) / max(threshold, 0.01)
                violation_penalties.append(min(gap, 2.0))
    
    if violation_penalties:
        avg_penalty = np.mean(violation_penalties)
        severity_weighted_score = max(0, 100 - (avg_penalty * 100))
    else:
        severity_weighted_score = 100.0
    
    # ── Dimension 3: Temporal Stability (20%)
    if len(trend) >= 7:
        variance = np.var(trend)
        mean_score = np.mean(trend)
        stability = max(0, 1 - (variance * 50))
        temporal_stability_score = ((stability * 0.5) + (mean_score * 0.5)) * 100
    else:
        temporal_stability_score = 75.0 # default for new models
    
    # ── Dimension 4: Intersectional Coverage (15%)
    if len(sensitive_cols) == 0:
        intersectional_score = 30.0
    elif len(sensitive_cols) == 1:
        intersectional_score = 65.0
    elif len(sensitive_cols) == 2:
        intersectional_score = 82.0
    else:
        intersectional_score = 95.0
    
    # ── Dimension 5: Remediation Velocity (10%)
    if not incidents:
        remediation_velocity_score = 80.0
    else:
        resolved = 0
        for inc in incidents:
            if inc.get("status") in ("Resolved", "Accepted"):
                resolved += 1
            elif inc.get("status") == "In-Progress":
                resolved += 0.5
        remediation_velocity_score = (resolved / len(incidents)) * 100
    
    # ── Dimension 6: Regulatory Alignment (10%)
    dir_values = list(metrics.get("disparate_impact_ratio", {}).values())
    if dir_values:
        dir_score = min(dir_values)
        regulatory_alignment_score = min(100, (dir_score / 0.80) * 80)
    else:
        regulatory_alignment_score = 70.0
    
    # ── Composite EBI
    scores = {
        "metric_coverage": metric_coverage_score,
        "severity_weighted": severity_weighted_score,
        "temporal_stability": temporal_stability_score,
        "intersectional": intersectional_score,
        "remediation_velocity": remediation_velocity_score,
        "regulatory_alignment": regulatory_alignment_score,
    }
    ebi = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    
    # ── Risk Tier
    tier, description = "CRITICAL", "Non-Compliant"
    for cutoff, t, d in RISK_TIERS:
        if ebi >= cutoff:
            tier, description = t, d
            break
    
    # ── Percentile
    percentile = min(99, max(1, (ebi - 30) / 0.65))
    
    # ── Explainability
    lowest_dim = min(scores, key=scores.get)
    dim_labels = {
        "metric_coverage": "Metric threshold violations",
        "severity_weighted": "High-magnitude bias violations",
        "temporal_stability": "Equity score instability over time",
        "intersectional": "Insufficient protected attribute coverage",
        "remediation_velocity": "Slow incident resolution",
        "regulatory_alignment": "Disparate impact below EEOC threshold",
    }
    priorities = sorted(scores.keys(), key=lambda k: scores[k])[:3]
    
    return EBIResult(
        enterprise_bias_index=ebi,
        risk_tier=tier,
        risk_description=description,
        percentile_rank=percentile,
        metric_coverage_score=metric_coverage_score,
        severity_weighted_score=severity_weighted_score,
        temporal_stability_score=temporal_stability_score,
        intersectional_score=intersectional_score,
        remediation_velocity_score=remediation_velocity_score,
        regulatory_alignment_score=regulatory_alignment_score,
        biggest_risk_factor=dim_labels[lowest_dim],
        improvement_priority=[dim_labels[p] for p in priorities],
    )
