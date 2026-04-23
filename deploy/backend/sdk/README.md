# FairLens SDK

Enterprise AI bias detection SDK for ML models — detect, monitor, and remediate unfairness.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import fairlens

report = fairlens.audit(model, X_test, y_test, sensitive_cols=["gender", "race"])
print(report.to_json())
print(f"Passed: {report.passed}")
```
