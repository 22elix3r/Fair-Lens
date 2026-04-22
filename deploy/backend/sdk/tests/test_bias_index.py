import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from fairlens.bias_index import compute_ebi

def test_ebi_perfect_model_scores_near_100():
    metrics = {
        "demographic_parity_difference": {"race": 0.0},
        "disparate_impact_ratio": {"race": 1.0},
        "equalized_odds_difference": {"race": 0.0}
    }
    result = compute_ebi(metrics, trend=[1.0]*30, sensitive_cols=["race"])
    assert result.enterprise_bias_index > 90
    assert result.risk_tier == "GREEN"

def test_ebi_biased_model_scores_below_60():
    metrics = {
        "demographic_parity_difference": {"race": 0.4},
        "disparate_impact_ratio": {"race": 0.4},
        "equalized_odds_difference": {"race": 0.3}
    }
    result = compute_ebi(metrics, trend=[0.5]*30, sensitive_cols=["race"])
    assert result.enterprise_bias_index < 60
    assert result.risk_tier in ["RED", "CRITICAL"]

def test_ebi_has_6_dimensions():
    result = compute_ebi({}, [])
    d = result.to_dict()["dimensions"]
    assert len(d) == 6
    assert "metric_coverage" in d
    assert "severity_weighted" in d

def test_ebi_improvement_priority_sorted():
    metrics = {
        "demographic_parity_difference": {"race": 0.5}, # Very bad
    }
    result = compute_ebi(metrics, [])
    assert len(result.improvement_priority) >= 1
    # The dimension with the lowest score should be in the list
    assert any("Metric threshold violations" in p or "High-magnitude" in p for p in result.improvement_priority)

if __name__ == "__main__":
    pytest.main([__file__])
