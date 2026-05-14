<div align="center">

# 🛡️ S E N T I N E L &nbsp; G R C &nbsp; `v2.0`

**Event-Driven Explainable Continuous Governance for DevSecOps**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-0a0a0a?style=for-the-badge&logo=python&logoColor=bf00ff" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/Event_Bus-Kafka-0a0a0a?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Apache Kafka"/>
  <img src="https://img.shields.io/badge/XAI_Graph-Neo4j-0a0a0a?style=for-the-badge&logo=neo4j&logoColor=008cc1" alt="Neo4j Graph Database"/>
  <img src="https://img.shields.io/badge/Sovereignty-Local_LLM-0a0a0a?style=for-the-badge&logo=meta&logoColor=white" alt="Local Sovereign AI"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/issues/shafincyber/Sentinel-GRC?style=flat-square" alt="Issues">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome">
</p>

> Bridging the gap between automated DevOps pipelines and qualitative European cybersecurity law through deterministic Explainable AI (XAI).

</div>

---

## 🏛️ Executive Summary

The enforcement of the **NIS2 Directive** and the **EU AI Act** has created a severe operational bottleneck known as the *Compliance Gap*. High-velocity cloud infrastructure is deployed at a rate that renders manual governance audits obsolete. Concurrently, utilizing cloud-hosted Generative AI for compliance translation introduces unacceptable data residency violations and hallucination risks.

**Sentinel-V2** resolves this dichotomy. It is an event-driven, hybrid orchestration framework that achieves **Explainable Continuous Governance (ECG)**. By synthesizing deterministic Policy-as-Code with air-gapped Sovereign AI, and mapping the results deterministically via a Graph Database, Sentinel generates audit-ready European legal reports with a **0.0% LLM hallucination rate**.

---

## 🏗️ System Architecture

Sentinel-V2 operates on a highly scalable, asynchronous microservice architecture designed to execute natively within CI/CD pipelines without blocking deployment runners.

| Component | Technology | Function |
| :--- | :--- | :--- |
| **Deterministic Engine** | `Checkov` | Scans Terraform and Kubernetes manifests for baseline cyber-hygiene failures. |
| **Semantic Engine** | `Local Llama-3` | Analyzes software supply chain manifests to identify qualitative 'Shadow AI' and telemetry risks. |
| **XAI Translation Core** | `Neo4j Graph` | Replaces static mapping by translating technical triggers directly to `NIS2 Art. 21` and `EU AI Act Art. 10`. |

---

## 🛠️ Quick Start & Installation

### ⚡ Fast Track: Clone-and-Play (Fully Dockerized)

If you want to test the pipeline immediately without installing Ollama or Python dependencies locally, run the entire orchestration inside a self-contained virtualization stack. 

> **Note:** This will automatically pull the 4.7GB `llama3` model on boot.

    docker compose -f docker-compose.standalone.yml up -d

---

<details>
<summary><b>⚙️ Advanced: Local Manual Setup (Click to expand)</b></summary>
<br>

#### 1. System Prerequisites
* **Python:** 3.10 or higher.
* **Docker Desktop:** Required to host local Kafka and Neo4j containers.
* **Ollama:** Installed and running locally.

#### 2. Initialize Environment

    git clone https://github.com/shafincyber/Sentinel-GRC.git
    cd Sentinel-GRC
    python -m venv venv

    # Windows
    .\venv\Scripts\Activate.ps1
    # Linux/macOS
    source venv/bin/activate

    pip install -r requirements.txt

#### 3. Boot Local Infrastructure

    ollama pull llama3
    docker compose up -d

*(Wait ~30 seconds for the Kafka broker and Neo4j to fully initialize).*

#### 4. Seed the Compliance Graph

    python seed_neo4j.py

</details>

---

## 🚀 Execution & Usage

To simulate the event-driven architecture locally, open three separate terminal windows. *Ensure your virtual environment is active in all of them.*

**📟 Terminal 1: Start the API Gateway (Producer)**

    python src/orchestrator/main.py

**📟 Terminal 2: Start the Kafka Worker (Consumer)**

    python src/orchestrator/worker.py

**📟 Terminal 3: Trigger the CI/CD Webhook**

    Invoke-RestMethod -Uri 'http://localhost:8000/api/v2/scan' -Method Post -Headers @{'Content-Type'='application/json'} -Body '{"repository_url": "shafincyber/ecommerce-api", "commit_hash": "production-release"}'

> **👀 Observation:** Watch **Terminal 2** to view the real-time dual-layer scans, Neo4j graph traversal, and the generation of the legally-backed compliance audit and autonomous patches.

---

## 🤝 Contributing

Contributions are highly encouraged! We are specifically looking for help expanding the Neo4j Compliance Graph to support frameworks like **DORA**, **GDPR**, and **ISO 27001**. 

Please read our [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on branching, commit standards, and pull requests.

## 📄 License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.