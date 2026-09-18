---
name: devops-cloud-suite
description: |
  DevOps Cloud Master Suite providing end-to-end infrastructure-as-code automation. Includes multi-stage non-root distroless containerization, production Kubernetes manifests & Helm charts, 3-stage GitHub Actions CI/CD workflows, WireGuard / Zero-Trust network topologies, and autonomous diagnostic loops with build-error-resolver.
triggers:
  - "devops"
  - "devops suite"
  - "devops-cloud-suite"
  - "docker distroless"
  - "kubernetes helm"
  - "github actions ci cd"
  - "zero trust devops"
license: MIT
metadata:
  origin: ECC
---

# DevOps Cloud Master Suite

Automated cloud-native engineering blueprint standardizing container packaging, orchestrations, security scanning, and continuous delivery.

---

## 1. Cloud-Native Pipeline Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS CI/CD PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────┤
│  [ Stage 1: Security & Quality ]                                        │
│  ESLint ➔ TypeScript Check ➔ SafetyGuard Secret Scan ➔ Trivy Image Scan │
├─────────────────────────────────────────────────────────────────────────┤
│  [ Stage 2: Automated Tests ]                                           │
│  Postgres Service Container ➔ Redis Cache ➔ Vitest / Pytest Suite       │
├─────────────────────────────────────────────────────────────────────────┤
│  [ Stage 3: Build & Release ]                                           │
│  Multi-Stage Docker ➔ Distroless Image ➔ OCI Container Registry (GHCR)  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Helm Upgrade / GitOps (ArgoCD)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       KUBERNETES RUNTIME CLUSTER                        │
│  - Ingress with TLS Termination                                         │
│  - Read-Only Root Filesystem + Non-Root User (UID 10001)                │
│  - Pod Disruption Budgets + Liveness/Readiness Probes                   │
│  - WireGuard / mTLS Zero-Trust Service Mesh                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Stage Non-Root Docker Blueprint

```dockerfile
# syntax=docker/dockerfile:1.4
# Stage 1: Compilation Stage
FROM golang:1.24-alpine AS builder
WORKDIR /src
RUN apk add --no-cache git ca-certificates

COPY go.mod go.sum ./
RUN go mod download

COPY . .
# ponytail: Static CGO-disabled binary compilation with stripped debug symbols
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /bin/server ./cmd/server

# Stage 2: Distroless Minimal Runtime
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app
COPY --from=builder /bin/server /app/server

USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

---

## 3. Kubernetes Deployment & Service Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app.kubernetes.io/name: api-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: api-service
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      containers:
        - name: server
          image: ghcr.io/org/api-service:v1.0.0
          imagePullPolicy: IfNotPresent
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 2
            periodSeconds: 5
```

---

## 4. 3-Stage GitHub Actions CI/CD Blueprint

```yaml
name: Continuous Integration & Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: corepack enable && pnpm install --frozen-lockfile
      - run: pnpm tsc --noEmit
      - name: Pre-push Secret Scan
        run: python scripts/safety_guard.py --scan-file .

  test:
    needs: lint-and-scan
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - run: corepack enable && pnpm install --frozen-lockfile
      - run: pnpm test

  build-and-push:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 5. Subagent Delegation Matrix

| Subagent | Role | Responsibility |
|----------|------|----------------|
| `architect` | Cloud Architect | Infrastructure topology, Helm chart templating, PDB and probe design |
| `security-reviewer` | Container Security | Distroless verification, non-root checks, secret scanning, Trivy CVE scan |
| `build-error-resolver` | CI Diagnostics | Diagnose and patch Docker compilation and dependency installation failures |

---

## 6. Verification Checklist

```bash
# 1. Build and test container locally
docker build -t app-test:local .

# 2. Dry-run Kubernetes manifests
kubectl apply --dry-run=client -f k8s/

# 3. Secret scan
python scripts/safety_guard.py --scan-file .
```
