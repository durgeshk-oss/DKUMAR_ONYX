# DKUMAR-_ONYX# README.md

# Project ONYX v3.0 — Enterprise GRC & Cyber Threat Topology Engine

Project ONYX is a world-class, security-focused Governance, Risk, and Compliance (GRC) platform engineered to ingest technical vulnerability telemetry, calculate real-time actuary asset exposure, map risk factors to cross-border regulatory frameworks, and render interactive topological network graphs. 

Built with a high-end, responsive **Neuron Glass UI design system**, the platform delivers deep situational awareness for security architects and enterprise risk executives.

---

## Architecture Overview

Project ONYX abstracts complexity by splitting analytical workloads across specialized decoupled engine pipelines and modules:

1. **`app.py` (Core Orchestration Engine):** Serves as the central backend controller. It establishes data connections with the local encrypted vault (`sovereign_vault.db`), handles raw syslog ingestions, and calculates aggregate financial risk liabilities dynamically.
2. **`predictive_engine.py` (Predictive Risk Framework):** Forecasts 30/60/90-day exploitation probabilities utilizing platform-specific exposure multipliers (e.g., Apache, Linux, MySQL, Windows) and tracking exploit velocity indexes.
3. **`knowledge_graph.py` (Enterprise Risk Topology):** Compiles multi-layered relational network graph maps using `networkx` and `plotly`. It balances system anchors against compliance frameworks via spring layout physics modeling.
4. **`regulation_mapper.py` (Dynamic Cross-Border Mapping):** Employs string-tokenization heuristics to automatically audit vulnerabilities against standard framework domains: **PIPEDA (CAN)**, **NIST SP 800-53 (USA)**, **SOX ITGC**, **PCI DSS v4**, and **GDPR (EU)**.
5. **`remediation_agent.py` & `ai_governance.py` (Autonomous Runbooks & Integrity Check):** Auto-generates defensive engineering action windows, verifies local subprocesses via secure platform-aware diagnostic checks, and scores local LLM response integrity.

---

## Core Features

* **Real-Time Log Ingestion Pipeline:** Accept and parse unstructured alerts, syslog frames, or incident text case-insensitively via manual telemetry inputs or live NVD API integrations.
* **Actuary Financial Exposure Calculations:** Quantify technical debts directly into dollar amounts, matching unique enterprise multipliers relative to infrastructure priorities.
* **Regulatory Compliance Cross-Auditing:** Instantly discover which exact clauses of regional laws are violated by active infrastructure CVE exposures.
* **Topological Clustering Graphs:** Visualize risk vectors anchored dynamically to corresponding business lines, computing graph layout physics based on exploit priority stiffness weights.
* **Executive Memory Exports:** Download standalone binary Audit Reports (.PDF) built via `reportlab` or raw tabular datasets (.XLSX) natively streamed straight from running RAM buffers.

---

## Installation & Setup

### Prerequisites
* Python 3.11+
* Local running instance of **Ollama** (with `gemma2:2b` pulled for the trust boundary chat engine)

### 1. Clone the Repository & Environment Setup
```bash
git clone [https://github.com/yourdomain/project-onyx.git](https://github.com/yourdomain/project-onyx.git)
cd project-onyx
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
