# FairLens — Demo Script (3-Minute Video)

> **Target:** Google Solutions Challenge 2026  
> **SDG Alignment:** SDG 10 (Reduced Inequalities), SDG 16 (Peace, Justice & Strong Institutions)
> **Theme:** "Algorithms shouldn't decide who gets left behind."

---

## Act 1: The Human Cost (0:00 – 0:35)

**Visual:** Fade in on a blurred, fast-paced montage of people looking at phones and laptops—some smiling, some distressed. The screen pauses on a rejected loan application. 

**Narration:** *"Meet Sarah. She was just denied a critical medical loan. Not because of her credit history, but because a machine learning model found a hidden statistical proxy for her demographic. The engineers who built this model had the best intentions, but they had no idea it was biased."*

**Visual:** Text on screen: **AI bias isn't just a technical glitch. It's a human crisis.**

**Narration:** *"As AI takes over hiring, healthcare, and finance, algorithms are deciding who gets an opportunity and who gets left behind. That is why we built **FairLens**—an enterprise-grade AI governance platform designed to detect, explain, and eliminate algorithmic bias before it ruins lives."*

---

## Act 2: The Discovery (0:35 – 1:10)

**Visual:** Quick cut to a developer's IDE (VS Code). Typing a single line of Python code.

**Narration:** *"For engineering teams, finding these biases used to be like finding a needle in a haystack. But with the FairLens Python SDK, it takes just one line of code to compute eight industry-standard fairness metrics."*

**Visual:** Transition from the terminal to the **FairLens Governance Console**. The camera pans across the Dashboard. It zooms in on a red alert for the "Loan Approval Engine."

**Narration:** *"Instead of finding out about the bias when someone like Sarah complains, the risk team sees this critical alert on the FairLens Console instantly. We can see exactly where the model is failing—in this case, the Equal Opportunity metric is severely violating our thresholds."*

---

## Act 3: The Resolution (1:10 – 1:50)

**Visual:** The user clicks into the Incident. The screen shows the "Root Cause Analysis" and the "Generate Playbook" button. The user clicks it.

**Narration:** *"Knowing a model is biased is only half the battle. How do you fix a complex, black-box algorithm without destroying its accuracy? This is where FairLens shines. Powered by Google's Gemini, FairLens automatically generates a remediation playbook."*

**Visual:** The slide panel opens, revealing step-by-step strategies (Threshold Calibration, Data Reweighting). The user clicks "Approve & Execute."

**Narration:** *"Gemini explains exactly *why* the model is biased—pointing out the specific proxy variables—and provides actionable, mathematically sound strategies to fix it. With a single click, the team approves the playbook, the model is adjusted, and fairness is restored."*

---

## Act 4: The Promise (1:50 – 2:20)

**Visual:** Show the "Compliance" tab. A PDF report is generated. A lock icon appears, indicating cryptographic signing via Cloud KMS. 

**Narration:** *"But we need to ensure this never happens to anyone else. FairLens cryptographically signs a comprehensive compliance report using Google Cloud KMS, proving to regulators that the model meets the EU AI Act standards."*

**Visual:** Show a GitHub PR being automatically blocked by a red `fairlens-gate` check.

**Narration:** *"And to prevent future bias, FairLens integrates directly into the CI/CD pipeline. If a developer accidentally pushes a biased model update tomorrow, the deployment is automatically blocked. Fairness isn't an afterthought; it's a structural guarantee."*

---

## Act 5: The Vision (2:20 – 3:00)

**Visual:** A clean, animated architecture diagram showing BigQuery, Cloud Run, Vertex AI, and Gemini working together seamlessly.

**Narration:** *"FairLens is built entirely on Google Cloud—utilizing BigQuery for massive analytics, Cloud Run for scalable deployment, and Gemini for deep explainability."*

**Visual:** Cut back to the human element—a montage of diverse individuals succeeding (getting a home keys, shaking hands for a job). Fade to the FairLens Logo.

**Narration:** *"When we build AI, we aren't just building software. We are building the infrastructure of human opportunity. With FairLens, we can ensure that future is fair, transparent, and equitable for everyone. Thank you."*

---

## Production Notes & GCP Services Used

| Service | Purpose in Demo |
|---------|---------|
| **BigQuery** | Stores the massive audit logs and telemetry data |
| **Cloud Run** | Hosts the React frontend and FastAPI backend |
| **Gemini** | Powers the automated root-cause analysis and playbooks |
| **Cloud KMS** | Cryptographically signs the compliance PDFs for legal immutability |
| **Cloud Build** | Runs the CI/CD pipeline fairness gate |
