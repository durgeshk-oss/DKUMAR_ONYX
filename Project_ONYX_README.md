# Project ONYX — Enterprise GRC Intelligence Platform

> **From infrastructure telemetry to board-ready risk intelligence.**

[![Status](https://img.shields.io/badge/status-architecture%20reference-teal)](#)
[![Type](https://img.shields.io/badge/type-GRC%20%2F%20Cybersecurity-blue)](#)
[![AI](https://img.shields.io/badge/AI%20inference-local--first-green)](#)
[![Frameworks](https://img.shields.io/badge/frameworks-NIST%20%7C%20SOC2%20%7C%20ISO27001%20%7C%20PCI--DSS%20%7C%20HIPAA-orange)](#)

---

## Overview

Project ONYX is an enterprise GRC and cybersecurity intelligence platform designed for regulated industries. It ingests infrastructure telemetry, maps detected risks to compliance frameworks in real time, translates technical exposure into financial impact estimates, and generates remediation guidance through secure, local AI inference.

**Target sectors:** Financial services · Healthcare · Defense & public sector · Cloud infrastructure · Enterprise SaaS

**Target users:** CISOs · GRC Analysts · Compliance Officers · Auditors · Infrastructure Engineers · Executive Leadership

> This is a portfolio-grade, architect-designed reference system — not a production deployment. It is presented as a reference architecture and functional prototype demonstrating depth in GRC platform design, AI governance, and enterprise security systems thinking.

---

## Problem Statement

Most enterprise GRC programs evolved from compliance checklists, not risk intelligence systems. As organizations scaled, they bolted on additional point tools — each solving a discrete problem while adding to operational fragmentation. The result:

| Problem | Impact |
|---|---|
| Disconnected SecOps and compliance workflows | Risk findings rarely reach compliance posture before audits |
| Static, point-in-time auditing | Exposure windows between quarterly cycles go undetected |
| No financial risk translation | CISOs cannot present risk in dollar terms to boards |
| Cloud AI data residency concerns | Regulated entities cannot safely route infrastructure data to third-party AI |
| Manual remediation workflows | Engineers research fixes ad hoc; runbooks are not pre-staged |
| Multi-framework compliance burden | Overlapping controls assessed redundantly across NIST, SOC 2, ISO 27001 |

**The core problem is not a lack of tooling — it is a lack of integration.**

---

## Architecture

### Four-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│  L1 · UI LAYER                                              │
│  Unified dashboard — risk topology · compliance posture ·   │
│  financial exposure · executive reporting                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  L2 · ORCHESTRATION ENGINE                                  │
│  Ingestion coordination · module sequencing · AI dispatch · │
│  output delivery                                            │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  L3 · ANALYTICAL PROCESSING LAYER                           │
│  Risk scoring · financial exposure engine · compliance      │
│  mapping · sandboxed local AI inference                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  L4 · SECURE DATA VAULT                                     │
│  Encrypted log storage · audit trail · framework config ·   │
│  remediation runbook repository                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Infrastructure logs
        │
        ▼
  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐
  │  Parse &    │────▶│  Risk Score │────▶│  Compliance Mapping │
  │  Normalize  │     │  + Exposure │     │  (NIST/SOC2/ISO...) │
  └─────────────┘     └─────────────┘     └──────────┬──────────┘
                                                      │
                             ┌────────────────────────▼──────────┐
                             │  Local AI Remediation Generation  │
                             │  (sandboxed · audit-logged ·      │
                             │   human-reviewed)                 │
                             └────────────────────────┬──────────┘
                                                      │
                             ┌────────────────────────▼──────────┐
                             │  Dashboard Visualization          │
                             │  Risk topology · heatmaps ·       │
                             │  remediation queue                │
                             └───────────────────────────────────┘
```

---

## Core Modules

### 1. Log Ingestion & Parsing Engine
Accepts structured and semi-structured telemetry from multiple source types. A normalization layer transforms raw events into a common schema before downstream processing.

**Supported sources:** Syslog · Windows Event Log · AWS CloudTrail · Azure Monitor · Endpoint detection feeds

**Key capabilities:**
- Multi-source telemetry ingestion with schema normalization
- Deduplication and classification by severity, asset, and event type
- Connector-based extensibility for new source types

---

### 2. Risk Scoring & Financial Exposure Engine
Applies a multi-factor risk model to normalized events, then translates high-severity findings into estimated dollar exposure ranges.

**Scoring factors:** Likelihood · Asset criticality · Threat context

**Key capabilities:**
- Multi-factor risk scoring per event
- Financial impact estimation expressed as dollar exposure ranges
- Risk-based remediation queue ordering (business-risk-led, not CVSS-score-led)

---

### 3. Multi-Framework Compliance Mapping
Maintains a unified control library across major compliance frameworks. A finding mapped once propagates to all relevant frameworks simultaneously.

**Supported frameworks:** NIST SP 800-53 · SOC 2 Type II · ISO 27001 · PCI-DSS 4.0 · HIPAA Security Rule · CIS Controls

**Key capabilities:**
- Real-time control status updates driven by infrastructure events
- Unified mapping eliminates manual cross-walk for overlapping control sets
- Control-level pass/fail/partial/gap status

---

### 4. Remediation & Runbook Generation
Generates step-by-step remediation runbooks scoped to the specific asset, platform, and control family. AI-assisted for novel findings, with human-in-the-loop validation.

**Key capabilities:**
- Pre-staged runbooks for known vulnerability classes
- Local AI-assisted generation for novel findings
- Human review gate before runbook commit
- Versioned runbook store linked to audit trail

---

### 5. Risk Topology Visualization
A graph-based visualization layer rendering the risk landscape as an interactive topology — linking assets, findings, compliance gaps, and financial exposure.

**Key capabilities:**
- Drill-down from compliance heatmap to originating infrastructure events
- Supports both analyst investigation and executive reporting use cases
- Real-time posture update as new events are processed

---

## AI Governance Design

ONYX integrates AI inference without introducing data residency, privacy, or auditability risks through a **local-first architecture** with five governance controls:

| Control | Design Rationale |
|---|---|
| **Local & offline inference** | All processing within the customer security boundary. Supports air-gapped deployments. No cloud AI dependency. |
| **Context-grounded processing** | Inference engine receives only structured context from the orchestration layer. No persistent memory, no raw data access. |
| **Full audit logging** | Every AI output logged with model version, input context hash, and timestamp. Creates a traceable evidence chain. |
| **Sandboxed execution** | Resource-limited, output-constrained isolated process. AI layer cannot affect platform state beyond its designated output channel. |
| **Data containment** | Sensitive fields (hostnames, IPs, user identities) masked or tokenized before inference. Model never sees raw PII. |
| **Human-in-the-loop review** | AI-generated runbooks are drafts pending analyst approval. The platform does not auto-execute AI recommendations. |

> **Why local-first matters:** Regulated entities subject to FedRAMP, HIPAA, SOX, or GDPR face significant legal and compliance complexity when routing infrastructure data to third-party cloud AI providers. Local inference removes this constraint by design.

---

## Business Impact

These are design objectives, not measured production outcomes:

- **Improved audit readiness** — continuous compliance mapping replaces periodic manual evidence gathering
- **Faster incident response** — pre-staged runbooks eliminate the research phase for known vulnerability classes
- **Executive risk visibility** — financial exposure translation enables board-level risk communication
- **Reduced compliance effort** — unified multi-framework mapping eliminates duplicated control cross-walk work
- **Effective risk prioritization** — remediation queue ordered by business risk impact, not CVSS score
- **Regulatory defensibility** — documented audit trail and AI governance record for regulatory examination

---

## Key Differentiators

| Dimension | Conventional GRC | ONYX |
|---|---|---|
| Compliance basis | Self-reported survey assertions | Telemetry-derived from live infrastructure events |
| Update frequency | Quarterly or annual | Real-time as events occur |
| Risk language | CVSS scores and severity labels | Dollar exposure ranges for executive communication |
| AI approach | Cloud-based third-party inference | Local-first, sandboxed, within customer boundary |
| Interface | Multiple disconnected point tools | Unified dashboard from telemetry to board view |

---

## User Personas

| Role | Primary Pain Point | Platform Value |
|---|---|---|
| **CISO / VP Security** | Needs real-time risk posture without aggregating across tools | Financial exposure dashboard + compliance posture for board reporting |
| **GRC Analyst** | Spends time manually mapping findings to compliance controls | Automated mapping replaces manual cross-walk exercises |
| **Compliance Officer** | No unified view across NIST, SOC 2, ISO 27001, HIPAA, PCI-DSS | Unified multi-framework control library with real-time status |
| **Internal / External Auditor** | Receives inconsistent, manually assembled evidence packages | Structured, timestamped, machine-generated evidence traceable to source events |
| **Infrastructure Engineer** | Receives findings without actionable remediation context | Pre-staged runbooks delivered alongside the finding |
| **Executive / Board** | Risk briefings full of technical terminology that doesn't translate | Dollar-range exposure view enables risk-grounded investment decisions |

---

## Future Roadmap

### Phase 1 — Operational Integrations
- SIEM connectors: Splunk, Microsoft Sentinel, IBM QRadar
- Ticketing integration: JIRA, ServiceNow, Azure DevOps (bidirectional)
- Expanded cloud log ingestion: GCP Cloud Audit Logs, AWS Security Hub, AWS Config
- API-based evidence export for audit platforms

### Phase 2 — Intelligence & Automation
- Predictive risk modeling via historical telemetry trend analysis
- Automated control testing and active validation
- Regulatory update tracking with control impact analysis
- Enhanced financial exposure modeling with sector-specific benchmarks

### Phase 3 — Advanced Telemetry & Scale
- Network telemetry: NetFlow, DNS query logs, east-west traffic analysis
- Third-party / TPRM module integrated into unified risk topology view
- Multi-tenant deployment model for MSSPs and GRC consulting firms
- AI model governance, version tracking, and output quality monitoring

---

## Design Principles

1. **Telemetry-driven over assertion-driven** — compliance posture derived from observable infrastructure state, not survey responses
2. **Financial translation as first-class output** — risk in dollar terms is a core module output, not a post-processing step
3. **Local-first AI as a compliance decision** — on-premises inference is an architectural constraint in regulated environments
4. **Human accountability in the AI chain** — AI outputs are always advisory, always reviewed; no auto-execution of AI recommendations
5. **Unified data layer for all personas** — analysts, engineers, and executives work from the same underlying risk intelligence

---

## About This Project

Project ONYX is a portfolio-grade reference architecture demonstrating enterprise GRC platform design, AI governance in regulated environments, and security-compliance orchestration. It is intended for use in technical interviews, portfolio presentations, and architectural discussions.

**Key domains demonstrated:** GRC platform architecture · TPRM · AI governance · Risk quantification · Compliance automation · SecOps integration · Enterprise security systems thinking

---

*Built by DK (Durgeshkumar Nonare) — GRC & Cybersecurity Architect | CISSP · CISM · CTIA · CCNA*
