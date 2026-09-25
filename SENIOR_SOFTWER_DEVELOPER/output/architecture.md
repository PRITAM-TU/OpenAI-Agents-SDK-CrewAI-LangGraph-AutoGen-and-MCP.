# Multi‑Agent Software Development Workflow (MASDW) – Implementation‑Ready Technical Design  

**Version:** 1.0 – 2026‑09‑25  
**Prepared by:** Senior Software Architect  

---  

## Table of Contents
1. [Scope & Assumptions](#scope--assumptions)  
2. [Actors & Roles](#actors--roles)  
3. [User Flow (End‑to‑End Sequence)](#user-flow-end‑to‑end-sequence)  
4. [Requirements Traceability](#requirements-traceability)  
5. [System Architecture & Component Diagram](#system-architecture--component-diagram)  
6. [Data Model](#data-model)  
7. [Module Boundaries & Public APIs](#module-boundaries--public-apis)  
8. [Technology Choices & Rationale](#technology-choices--rationale)  
9. [Component‑Level Design](#component‑level-design)  
10. [Acceptance Criteria (Mapped to FR/US)](#acceptance-criteria-mapped-to-frus)  
11. [Implementation Risks & Mitigations](#implementation-risks--mitigations)  
12. [Open Issues & Future Enhancements](#open-issues--future-enhancements)  

---  

## 1. Scope & Assumptions  

| # | Statement |
|---|-----------|
| **A‑1** | Teams already use **GitHub** (or GitLab) with a CI pipeline that can accept a PR from a bot account. |
| **A‑2** | Requests are well‑formed: at least a short description and acceptance criteria. |
| **A‑3** | Access to a managed **LLM inference endpoint** (e.g., OpenAI GPT‑4‑Turbo) with ≤ 500 ms/token latency. |
| **A‑4** | Compute (GPU/CPU) for agents runs in a cloud‑native environment with **Kubernetes** autoscaling. |
| **A‑5** | Human final sign‑off is mandatory – the system never merges automatically. |
| **A‑6** | Execution of generated code is allowed inside **network‑isolated containers** (no outbound internet). |
| **A‑7** | Projects use standard Python (`pytest`) or TypeScript (`jest`) test frameworks. |
| **A‑8** | Licensing compliance scanning is out of scope for Phase 1. |
| **A‑9** | All configuration (lint rules, LLM prompts, language plugins) is stored in a **GitOps‑style repo** that the platform watches. |
| **A‑10** | The platform must be operable by a small team (≤ 4 engineers). |

---  

## 2. Actors & Roles  

| Actor | Description | Primary Interactions |
|-------|-------------|----------------------|
| **Software Engineer (User‑Developer)** | Submits feature/bug request, reviews PR, gives final approval. | UI → Request Service; Review UI → Approve/Reject. |
| **Product Owner** | Creates high‑level requests, monitors delivery speed. | UI → Request Service; Dashboard → Metrics. |
| **Team Lead / Tech Lead** | Oversees quality, sets lint/style policies. | Settings UI → Config Service; Review UI. |
| **DevOps / CI Engineer** | Provides CI hooks, ensures sandbox security, monitors scaling. | CI Hook Service → Repository; Observability Service. |
| **Platform Engineer (Ops)** | Deploys MASDW platform, configures autoscaling, manages secrets. | Kubernetes manifests; Secrets store. |
| **Analysis Agent** | LLM‑driven service that extracts functional specs & design. | Consumes request payload, outputs design markdown. |
| **Implementation Agent** | LLM‑driven service that writes source code files. | Consumes design markdown, outputs code diff. |
| **Test Generation Agent** | LLM‑driven service that writes focused unit tests. | Consumes code diff, outputs test files. |
| **Verification Engine** | Orchestrates sandbox execution of tests + static analysis. | Runs container jobs, returns pass/fail status. |
| **Orchestration Engine** | State machine (Temporal) that sequences the agents & handles retries. | Drives the whole workflow. |
| **Observability Service** | Emits Prometheus metrics, forwards logs to Loki/ELK, powers Grafana dashboard. | Receives events from all components. |

---  

## 3. User Flow (End‑to‑End Sequence)  

```
┌─────────────────┐   1. POST /requests   ┌─────────────────────┐
│   UI / API      │─────────────────────►│ Request Service      │
└─────────────────┘                      └───────┬─────────────┘
                                               │
                                               ▼
                                      ┌─────────────────────┐
                                      │  Persistence (DB)   │
                                      └───────┬─────────────┘
                                              │
   2. Orchestration (Temporal)                │
   ┌──────────────────────────────────────────▼─────────────────────────────────────┐
   │  State: RECEIVED → ANALYZING → IMPLEMENTING → TESTING → VERIFICATION → READY │
   │                                                                              │
   │  ──► Analysis Agent (LLM) ──► design.md (stored)                           │
   │  ──► Implementation Agent (LLM) ──► code diff (tmp repo)                    │
   │  ──► Test Generation Agent (LLM) ──► tests (tmp repo)                      │
   │  ──► Verification Engine (Docker sandbox) ──► pass/fail + logs            │
   └──────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                                 ┌─────────────────────────────┐
                                 │ Review UI (Web)               │
                                 │ - design.md                   │
                                 │ - code diff                   │
                                 │ - test summary + logs         │
                                 │ - Approve / Reject / Edit     │
                                 └───────┬─────────────────────┘
                                         │
                     3a. Approve         │   3b. Reject / Edit
   ┌─────────────────────▼───────────────────────┐
   │ CI‑Integration Hook (GitHub Bot)            │
   │ - Create feature branch                      │
   │ - Commit code + tests                        │
   │ - Open PR with label “AI‑generated”          │
   │ - Trigger downstream CI (existing pipeline) │
   └─────────────────────┬───────────────────────┘
                         │
                         ▼
                ┌─────────────────────┐
                │ PR Review + Merge   │
                └─────────────────────┘
```

*Key SLA points* (derived from **NFR‑1**):  
- **Full cycle** (request → verified PR) ≤ 5 min → measured from `POST /requests` to `Verification Engine` PASS.  
- **Human latency** (Review UI) not part of SLA; must be < 30 min to meet **BG‑1**.

---  

## 4. Requirements Traceability  

| Req ID | Type | Description | Design Artifact(s) |
|--------|------|-------------|--------------------|
| **FR‑1** | Functional | Request Intake API/UI | `Request Service` (REST endpoint), UI form, JSON Schema |
| **FR‑2** | Functional | Analysis Agent produces design markdown | Agent Prompt Library, `analysis_agent` module |
| **FR‑3** | Functional | Implementation Agent generates lint‑compliant code | `implementation_agent`, Lint Config Loader |
| **FR‑4** | Functional | Test Generation Agent produces focused unit tests | `testgen_agent` |
| **FR‑5** | Functional | Verification Engine runs tests in sandbox, all must pass | `sandbox_runner`, Docker image |
| **FR‑6** | Functional | Human‑in‑the‑Loop Review UI | `review_ui` (React), API `GET /requests/{id}` |
| **FR‑7** | Functional | CI Integration Hook publishes PR | `ci_hook_service` (GitHub Bot) |
| **FR‑8** | Should | Multi‑language plug‑in framework | `language_plugin` interface, plugin registry |
| **FR‑9** | Should | Configurable coding style | `style_config_service` |
| **FR‑10** | Could | Suggest alternative designs | `design_alternatives` extension in Analysis Agent |
| **FR‑11** | Could | Automated refactoring of existing code | Future `refactor_agent` |
| **NFR‑1** | Non‑functional | Latency ≤ 5 min per full cycle | Temporal timeouts, async worker pool |
| **NFR‑2** | Non‑functional | Secure sandbox execution | Docker security profile, network‑policy |
| **NFR‑3** | Non‑functional | Observability (metrics, logs) | Prometheus exporter, Grafana dashboards |
| **NFR‑4** | Should | Support ≥ 20 concurrent requests | Horizontal pod autoscaling, queue length monitoring |
| **BG‑1‑BG‑4** | Business | Map to success metrics shown in dashboard | Observability + SLA enforcement |

---  

## 5. System Architecture & Component Diagram  

```
+-------------------+          +-------------------+          +-------------------+
|   Front‑End UI    |  <---->  |   API Gateway     |  <---->  |   Request Service |
+-------------------+          +-------------------+          +-------------------+
                                   |   ^   |
                                   |   |   |   (REST/JSON)
                                   ▼   |   ▼
                               +-------------------+          +-------------------+
                               |   Auth & Rate‑Lim |          |   Persistence DB |
                               +-------------------+          +-------------------+
                                   |
                                   ▼
                            +--------------------+
                            | Orchestration (Temporal) |
                            +--------------------+
                                   |
            +----------------------+----------------------+----------------------+
            |                      |                      |                      |
            ▼                      ▼                      ▼                      ▼
   +----------------+   +-------------------+   +-------------------+   +-------------------+
   | Analysis Agent |   | Implementation   |   | Test Generation   |   | Verification Eng. |
   +----------------+   | Agent            |   | Agent             |   +-------------------+
                        +-------------------+   +-------------------+   |
                              |                       |               |
                              ▼                       ▼               ▼
                     +----------------+        +----------------+   +-------------------+
                     | Prompt Library |        | Prompt Library |   | Sandbox Runner    |
                     +----------------+        +----------------+   +-------------------+
                                   |                         |
                                   ▼                         ▼
                           +--------------------+   +--------------------+
                           | Temporary Git Repo |   | Docker Sandbox     |
                           +--------------------+   +--------------------+

                                    |
                                    ▼
                           +--------------------+
                           | Review UI (React)  |
                           +--------------------+
                                    |
                                    ▼
                           +--------------------+
                           | CI Hook (GitHub   |
                           | Bot)               |
                           +--------------------+

Observability (Prometheus + Grafana) & Logging (Loki) tap into every component via side‑car exporters.
```

*Key architectural patterns*  

| Pattern | Why it satisfies a requirement |
|---------|--------------------------------|
| **Event‑driven workflow (Temporal)** | Guarantees **retries**, **state persistence**, and **visibility** → satisfies **FR‑3**, **NFR‑1**, **NFR‑3**. |
| **Plugin‑based language modules** | Enables **FR‑8** (add new language in ≤ 2 weeks). |
| **Docker sandbox per request** | Provides **NFR‑2** isolation and deterministic test execution. |
| **GitOps configuration** | Allows **FR‑9** style configurability without code changes. |
| **REST + gRPC internal** | REST for external (UI) simplicity; gRPC for low‑latency internal agent calls (e.g., Prompt Service). |
| **Side‑car Prometheus exporters** | Fulfill **NFR‑3** observability with minimal code intrusion. |

---  

## 6. Data Model  

All entities are stored in a **PostgreSQL** database (or CloudSQL). Primary keys are UUIDs.

| Table | Columns | Description |
|-------|---------|-------------|
| `requests` | `id PK`, `title`, `description`, `acceptance_criteria`, `status` (enum), `created_at`, `updated_at`, `owner_id` | Core request record. |
| `designs` | `id PK`, `request_id FK`, `markdown`, `confidence_score`, `created_at` | Output of Analysis Agent. |
| `code_artifacts` | `id PK`, `request_id FK`, `file_path`, `diff_blob` (BASE64), `language`, `created_at` | Files generated by Implementation Agent. |
| `test_artifacts` | `id PK`, `request_id FK`, `file_path`, `test_blob`, `coverage_pct`, `created_at` | Tests