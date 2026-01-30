# Tasks — Phase IV: Local Kubernetes Deployment

**Project:** Cloud Native Todo Chatbot  
**Scope:** Docker → Helm → Kubernetes → AI Ops  
**Prerequisites:** Phase III backend + frontend completed

---

## Format

`[ID] [P?] [Scope] Description`

- **[P]** = can be done in parallel  
- **[Scope]** = INFRA, DOCKER, HELM, K8S, AI, TEST, OPS  

---

## Phase 1 — Environment & Tooling (Foundation)

> **CRITICAL:** All DevOps tooling must be ready before containerization.

- [T001] [P] [INFRA] Install Docker Desktop 4.53+
- [T002] [P] [INFRA] Enable Kubernetes in Docker Desktop
- [T003] [P] [INFRA] Install Minikube and verify `minikube start`
- [T004] [P] [INFRA] Enable metrics server in Minikube
- [T005] [P] [INFRA] Install Helm CLI
- [T006] [P] [AI] Install kubectl-ai via krew
- [T007] [P] [AI] Configure OpenAI API key for kubectl-ai
- [T008] [P] [AI] Install Kagent
- [T009] [P] [AI] Validate kubectl-ai and Kagent connectivity

**Checkpoint:** Local Kubernetes + AI DevOps ready ✔️

---

## Phase 2 — Docker AI Containerization

> **Goal:** All services must exist as production-grade Docker images.

### Frontend

- [T010] [DOCKER] Generate Next.js Dockerfile using Gordon
- [T011] [DOCKER] Build image `todo-frontend:latest`
- [T012] [DOCKER] Run and validate frontend container

### Backend

- [T013] [DOCKER] Generate FastAPI Dockerfile using Gordon
- [T014] [DOCKER] Add ENV support (DATABASE_URL, OPENAI_API_KEY, AI_AGENT_URL)
- [T015] [DOCKER] Build image `todo-backend:v6`

### AI Agent

- [T016] [DOCKER] Generate AI Agent Dockerfile
- [T017] [DOCKER] Build image `ai-agent:v6`

**Checkpoint:** All images exist locally ✔️

---

## Phase 3 — Load Images into Minikube

- [T018] [K8S] Point Docker to Minikube daemon
- [T019] [K8S] Rebuild frontend image inside Minikube
- [T020] [K8S] Rebuild backend image inside Minikube
- [T021] [K8S] Rebuild AI-agent image inside Minikube
- [T022] [K8S] Verify images via `minikube ssh docker images`

**Checkpoint:** Kubernetes can pull all images locally ✔️

---

## Phase 4 — Helm Chart Creation

> **CRITICAL:** No deployment allowed before Helm is valid.

- [T023] [HELM] Create Helm chart (`todo-chart`)
- [T024] [HELM] Configure Chart.yaml metadata
- [T025] [HELM] Create secrets template (API keys + DB URL)
- [T026] [HELM] Create frontend Deployment + Service
- [T027] [HELM] Create backend Deployment + Service
- [T028] [HELM] Create AI agent Deployment + Service
- [T029] [HELM] Lint Helm chart
- [T030] [HELM] Render Helm templates for validation

**Checkpoint:** Helm chart is valid ✔️

---

## Phase 5 — Kubernetes Deployment

- [T031] [K8S] Verify Minikube health
- [T032] [K8S] Deploy Helm release
- [T033] [K8S] Verify all pods running
- [T034] [K8S] Verify all services created
- [T035] [K8S] Validate service endpoints

**Checkpoint:** Application running in cluster ✔️

---

## Phase 6 — Networking & Access

- [T036] [K8S] Port-forward frontend to `localhost:3000`
- [T037] [K8S] Port-forward backend to `localhost:8000`
- [T038] [K8S] Port-forward AI agent to `localhost:8001`
- [T039] [K8S] Validate browser + API + AI endpoints

---

## Phase 7 — System Testing

- [T040] [TEST] Verify frontend loads
- [T041] [TEST] Verify backend API `/docs`
- [T042] [TEST] Verify AI agent responses
- [T043] [TEST] Run full UI → API → DB → AI flow

**Checkpoint:** Full system operational ✔️

---

## Phase 8 — Scaling & Rollouts

- [T044] [OPS] Scale frontend using kubectl-ai
- [T045] [OPS] Scale backend
- [T046] [OPS] Perform rolling update
- [T047] [OPS] Validate rollout status
- [T048] [OPS] Test rollback

---

## Phase 9 — Monitoring & Debugging

- [T049] [OPS] Enable Minikube dashboard
- [T050] [AI] Use kubectl-ai for pod health
- [T051] [AI] Use Kagent for performance analysis
- [T052] [OPS] Validate logs, events, networking

---

## Phase 10 — Documentation & Cleanup

- [T053] [INFRA] Write deployment README
- [T054] [INFRA] Document port-forwarding
- [T055] [INFRA] Document troubleshooting
- [T056] [OPS] Helm uninstall
- [T057] [OPS] Stop or delete Minikube

---

## Final Success Criteria

- [ ] All three services running in Kubernetes
- [ ] Helm chart deploys cleanly
- [ ] UI → API → AI works
- [ ] kubectl-ai + Kagent used
- [ ] Docs completed
