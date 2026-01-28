## Phase 4: Kubernetes Orchestration & AIOps (v1.0.0)

### 1. Build & Versioning (Strict v1.0.0)
- [x] **Frontend**: Build Docker image `todo-frontend:v1.0.0`. (Current: latest)
- [x] **Backend**: Build Docker image `todo-backend:v1.0.0`. (Current: latest)
- [x] **AI-Agent**: Build Docker image `todo-ai-agent:v1.0.0`. (Current: latest)
- [x] **Minikube Sync**: Load all `:v1.0.0` images into Minikube using `minikube image load`.

### 2. Helm Chart Updates (`todo-chart/`)
- [x] **Values.yaml**: Update all image tags from `latest` to `v1.0.0`.
- [x] **Pull Policy**: Set `imagePullPolicy: Never` in all templates to force use of local v1.0.0 images.
- [x] **Internal Routing**: 
    - Verify Frontend uses `http://backend-service:80`.
    - Verify Backend uses `http://ai-agent-service:8080`.

### 3. Restore "Real AI" Logic
- [x] **Assistant.py**: Remove the mock "Sadaf/Samia" if/else block.
- [x] **SDK Integration**: Restore the `process_message` function to use the **OpenAI Agents SDK** and `agent.run()`.
- [x] **Secrets**: Ensure `todo-secrets` (OPENAI_API_KEY) is properly injected into the `ai_agent` deployment.

### 4. Deployment & Verification
- [x] **Cluster Start**: `minikube start --driver=docker`.
- [x] **Helm Install**: `helm install my-todo-stack ./todo-chart`.
- [x] **Health Check**: Run `kubectl get pods` and confirm all are `1/1 Running`.
- [x] **Service Check**: Run `kubectl get service` to verify NodePort access.