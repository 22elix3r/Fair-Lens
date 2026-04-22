# FairLens — Live Demo

**Console:** https://fairlens-console.vercel.app
**API:**     https://YOUR-URL.up.railway.app
**API Explorer:** https://YOUR-URL.up.railway.app/docs (Interactive Swagger — try any endpoint without Postman)
**Docs:**    /docs (FastAPI Swagger auto-generated)

## Quick Demo Path (3 minutes)
1. Open Console → click "Demo Mode" on login
2. Dashboard → click "Credit-Risk-V3" bar (equity 0.71)
3. See violations + EBI score of 54 (CRITICAL)
4. Go to Incidents → click "Generate Playbook" on INC-001
5. Read Gemini strategies → "Approve & Execute"
6. Go to Compliance → Generate EEOC Report → Download PDF
7. Go to Benchmarks → see industry comparison

## Run Locally (30 seconds)
```bash
pip install fairlens
python -c "
import fairlens, pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
# ... (demo script)
"
```
