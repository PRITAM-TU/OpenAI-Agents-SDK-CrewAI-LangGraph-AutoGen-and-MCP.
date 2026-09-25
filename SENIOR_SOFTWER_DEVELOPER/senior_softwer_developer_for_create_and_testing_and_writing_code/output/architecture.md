# Agentic Software Delivery Platform – Multi‑Agent Development Workflow  
**Version:** 1.0 – Design Document  
**Author:** Senior Software Architect  
**Date:** 2026‑09‑25  

---  

## Table of Contents
1. [Scope & Overview](#1-scope--overview)  
2. [Actors & User Flow](#2-actors--user-flow)  
3. [Functional Requirements & Acceptance Criteria](#3-functional-requirements--acceptance-criteria)  
4. [Non‑Functional Requirements](#4-non-functional-requirements)  
5. [System Architecture](#5-system-architecture)  
6. [Data Model & Persistence](#6-data-model--persistence)  
7. [Module & API Boundaries](#7-module--api-boundaries)  
8. [Technology Choices & Rationale](#8-technology-choices--rationale)  
9. [Implementation‑Ready Acceptance Criteria (Traceability)](#9-implementation-ready-acceptance-criteria-traceability)  
10. [Risks & Mitigations](#10-risks--mitigations)  
11. [Assumptions & Dependencies](#11-assumptions--dependencies)  

---  

## 1. Scope & Overview  

| In‑Scope | Out‑of‑Scope (Release 1) |
|----------|--------------------------|
| **REQ‑A** – Multi‑agent orchestration (Analyse, Design, Code‑Gen, Test‑Gen, Validator).  <br>**REQ‑B** – Natural‑language request UI (Web + API). <br>**REQ‑C** – Plug‑in architecture for custom agents. <br>**REQ‑D** – CI/CD integration (GitHub/GitLab). <br>**REQ‑E** – Test generation + execution + coverage/mutation reporting. <br>**REQ‑F** – Dashboard & immutable audit log. <br>**REQ‑G** – Role‑based access control. <br>**REQ‑H** – Containerised runtime with secret‑sanitisation. <br>**REQ‑I** – Documentation & developer guide. | Pair‑programming UI, automatic refactoring of existing code, non‑code artefacts (mock‑ups, diagrams), self‑learning agents, native integration with external ticketing tools. |

The platform’s **primary outcome** is a **Git Pull‑Request (PR)** that contains:  

* A **design specification** (Markdown).  
* **Source code** matching the spec.  
* **Focused unit/integration tests**.  
* **Verification summary** (coverage, mutation score, pass/fail).  

All artefacts are traceable to the originating request and immutable audit logs.

---  

## 2. Actors & User Flow  

### 2.1 Actors  

| Actor | Responsibilities | Primary UI / API |
|-------|-------------------|------------------|
| **Product Manager (PM)** | Submit high‑level feature/bug description. | Web UI – “New Request” form. |
| **Software Engineer (SE)** | Review design, edit generated code/tests, merge PR. | Web UI – Request Detail / GitHub PR. |
| **Team Lead / Engineering Manager (TL)** | Monitor pipeline health, approve/reject PRs, view audit. | Dashboard. |
| **QA Engineer (QA)** | Inspect generated tests, add manual tests if needed. | Dashboard – Test Explorer. |
| **DevOps / Platform Engineer (DO)** | Configure CI hooks, maintain agent registry, manage runtime. | Admin UI / CLI. |
| **Compliance / Security Officer (CS)** | Review audit logs, enforce RBAC, verify no secret leakage. | Dashboard – Audit Log. |
| **Agent Runtime (AR)** | Execute specialised agents in isolated containers. | Internal – orchestrated via Scheduler. |
| **External Git Service (GitHub/GitLab)** | Host source repository, receive PRs, run CI jobs. | Integrated via OAuth token. |

### 2.2 End‑to‑End User Flow  

1. **Login** – user authenticates via SSO (OIDC). RBAC evaluated (REQ‑G).  
2. **Submit Request** – PM/SE writes a natural‑language description → POST `/api/v1/requests`. System returns **Request ID** and status **QUEUED** (F‑001).  
3. **Analyse Stage** – Orchestrator launches **Analyse Agent** (container). Output: **DesignSpec** (markdown) → status **DESIGN_READY** (F‑002).  
4. **Design Review** – SE views spec in Dashboard, can add comments or request “Regenerate”.  
5. **Code Generation** – **CodeGen Agent** produces source files → new Git branch `ai/<request-id>` is created, PR opened → status **CODE_READY** (F‑003).  
6. **Test Generation** – **TestGen Agent** adds test files, runs coverage tool, stores report → status **TESTS_READY** (F‑004).  
7. **Validation** – **Validator Agent** triggers CI pipeline (GitHub Actions) that runs: unit tests, coverage, **Stryker** mutation testing → creates **AI‑Verified** check (PASS/FAIL) and comment with metrics → status **VALIDATED** (F‑005).  
8. **Human Review** – SE may edit code/tests, push commits → audit log records **USER_MODIFICATION** (F‑008).  
9. **Merge** – TL approves PR (must have **AI‑Verified PASS**). Merge triggers production deployment via existing CI/CD.  
10. **Dashboard & Auditing** – TL/CS view request timeline, artefact hash, RBAC‑controlled logs (F‑006).  
11. **Optional Export** – DO clicks **Export** → signed zip (F‑010).  

*All steps are event‑driven via a **Message Bus** (Redis Streams) ensuring decoupling and easy scaling.*

---  

## 3. Functional Requirements & Acceptance Criteria  

| ID | Title | Requirement | Acceptance Criteria (G/W/T) |
|----|-------|-------------|-----------------------------|
| **F‑001** | Submit a natural‑language request | **M** – Must allow authenticated user to create request via UI/API. | **Given** a logged‑in user with role *requester* **When** they POST `{description}` to `/api/v1/requests` **Then** a `Request` record is persisted, a UUID is returned, status = *QUEUED*, and an event `request.created` is emitted. |
| **F‑002** | Analyse request & produce design spec | **M** – Must turn description into a design document. | **Given** a queued request **When** the Analyse Agent finishes **Then** a markdown file `design.md` is stored, linked to the request, status → *DESIGN_READY*, and an event `design.completed` is emitted. |
| **F‑003** | Generate implementation code | **M** – Must create a PR with source files that follow the design. | **Given** a request with status *DESIGN_READY* **When** CodeGen Agent runs **Then** a new branch `ai/<id>` is pushed to the target repo, a PR titled “AI‑Generated – <summary>” is opened, status → *CODE_READY*, and `code.generated` event emitted. |
| **F‑004** | Generate focused verification tests | **M** – Must add unit & integration tests plus coverage report. | **Given** a PR in *CODE_READY* **When** TestGen Agent runs **Then** test files are added, `coverage.xml` and `mutation.json` are stored, PR status → *TESTS_READY*, and `tests.generated` event emitted. |
| **F‑005** | Execute tests & report validation | **M** – Must run CI, produce pass/fail, coverage ≥ 85 % and mutation ≥ 70 %. | **Given** a PR with tests **When** Validator Agent triggers CI **Then** the PR receives a status check “AI‑Verified” (PASS/FAIL) and a comment summarising metrics. If metrics meet thresholds, status = *VALIDATED*; else *FAILED*. |
| **F‑006** | Dashboard view & audit trail | **S** – Must expose searchable view of all requests and immutable logs. | **Given** a user with role *manager* **When** they open `/dashboard` **Then** they see a table (ID, owner, status, timestamps) and can drill into a request to see design, code diff, test report, and a SHA‑256 hash of the full artefact bundle. |
| **F‑007** | Role‑based access control | **S** – Must enforce RBAC for all actions. | **Given** any API call **When** RBAC middleware checks the caller’s role **Then** the request is allowed/denied, and the attempt is recorded in `audit_log`. |
| **F‑008** | Override / edit generated artefacts | **C** – Must preserve AI context when humans edit PR. | **Given** a PR opened by the platform **When** a user pushes a new commit **Then** the system records the diff as `user_modification` and does **not** auto‑re‑run agents unless the user explicitly requests regeneration. |
| **F‑009** | Plug‑in architecture for custom agents | **C** – Must allow registration of Docker‑based agents that implement the Agent SDK. | **Given** an admin uploads a Docker image tag `registry.mycorp.com/custom-analyse:1.0` via `/admin/agents` **When** the image passes health‑check **Then** it appears in the Agent Registry and can be selected for any step via request‑level config. |
| **F‑010** | Export artefacts for external CI | **W** – Must allow download of signed zip bundle. | **Given** a request in *VALIDATED* **When** the user clicks “Export” **Then** a PKCS#7‑signed zip containing `design.md`, source, tests, coverage, mutation report is streamed, and a download‑audit entry is created. |

*All functional stories reference the **MoSCoW** priority matrix in the PRD.*

---  

## 4. Non‑Functional Requirements  

| ID | Category | Requirement | Trace to PRD | Acceptance Metric |
|----|----------|-------------|--------------|-------------------|
| **NF‑001** | Performance | End‑to‑end ≤ 5 min for ≤ 200 LOC feature. | BG‑1, REQ‑A | 95 % of 100‑request load‑test meet ≤ 5 min latency. |
| **NF‑002** | Reliability | System availability 99.5 % (excl. maintenance). | BG‑3, REQ‑A | Monthly uptime ≥ 99.5 % (monitor via Prometheus). |
| **NF‑003** | Scalability | Up to 50 parallel agents; auto‑scale containers. | REQ‑A, REQ‑C | Load test with 50 concurrent requests shows ≤ 10 % latency increase. |
| **NF‑004** | Security | All artefacts encrypted at rest; no secret leakage in logs. | BG‑4, REQ‑H | Automated secret‑scan (GitGuardian) reports 0 leaks over 30 days; storage encrypted with AES‑256. |
| **NF‑005** | Maintainability | Agents conform to **Agent SDK v1.0**; each covered ≥ 80 % unit tests. | REQ‑C, REQ‑I | CI badge “Agent SDK compliance” passes; test coverage report ≥ 80 % per agent repo. |
| **NF‑006** | Observability | Structured logging, metrics (request latency, error rates), tracing (OpenTelemetry). | BG‑3, REQ‑A | Grafana dashboards show per‑stage latency, error count < 1 % of total requests. |
| **NF‑007** | Portability | Deployable on Kubernetes (v1.28+) and optionally on Docker‑Compose for dev. | REQ‑H | Helm chart installs successfully on GKE/EKS; dev mode runs via `docker-compose up`. |
| **NF‑008** | Cost Control | LLM token usage < 0.5 USD per request (average). | A‑1 | Billing dashboard shows avg cost ≤ 0.5 USD over 30‑day window. |

---  

## 5. System Architecture  

### 5.1 High‑Level Diagram  

```
+-------------------+          +-------------------+          +-------------------+
|   Front‑End (SPA) | <--HTTPS--> Auth Service   | <--JWT--> |   API Gateway    |
+-------------------+          +-------------------+          +-------------------+
          |                                 |                         |
          |                                 |                         |
          v