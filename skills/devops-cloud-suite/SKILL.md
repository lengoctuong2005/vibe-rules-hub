---
name: devops-cloud-suite
description: |
  Comprehensive DevOps Cloud Master Suite for enterprise cloud engineering: Terraform / OpenTofu IaC, multi-stage distroless containers, Kubernetes orchestration, zero-downtime canary pipelines, GitHub Actions CI/CD automation, and OpenTelemetry / Prometheus SRE observability.
triggers:
  - "devops"
  - "devops-cloud-suite"
  - "terraform"
  - "kubernetes"
  - "docker"
  - "cicd"
  - "cloud architecture"
license: MIT
metadata:
  origin: ECC
---

# DevOps Cloud Master Suite

Enterprise-grade infrastructure, deployment, and reliability engineering framework integrating cloud automation, container security, and automated multi-agent operational pipelines.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                           DEVELOPER / GIT OPS                           |
|  Git Push · Pull Request · Branch Protection · Peer Review Sign-off     |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                      GITHUB ACTIONS CI/CD PIPELINE                      |
|  Stage 1: Safety Scan (Secret Guard) · Static Lint (tflint / ESLint)   |
|  Stage 2: Unit / Integration Tests (Ephemeral Testcontainers)          |
|  Stage 3: Distroless Docker Build · Trivy CVE Vulnerability Scan       |
|  Stage 4: OIDC Cloud Auth · Canary Deployment (Argo Rollouts / Flux)   |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ OIDC (Zero Static Keys)
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     KUBERNETES CLOUD RUNTIME (EKS/GKE)                  |
|  Ingress Gateway · NetworkPolicy Firewall · Namespace Isolation         |
|  PodDisruptionBudget (PDB) · Horizontal Pod Autoscaler (HPA)            |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|        DATABASE CLOUD TIER       |  |       OBSERVABILITY & APM         |
|  AWS RDS / Cloud SQL (PgBouncer) |  |  OpenTelemetry Collector Daemon   |
|  Encrypted at Rest (KMS)         |  |  Prometheus Metrics · Grafana SLO |
+──────────────────────────────────┘  +───────────────────────────────────+
```

---

## 2. Declarative Terraform / OpenTofu Blueprint

```hcl
# main.tf: Enterprise AWS VPC & EKS Infrastructure Module
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
  backend "s3" {
    bucket         = "company-tfstate-production"
    key            = "core/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "VanguardMasterSuite"
    }
  }
}

# ponytail: Direct VPC resource declaration - upgrade to complex transit gateway if multi-region
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}
```

---

## 3. GitHub Actions OIDC Multi-Stage CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Production CI/CD Pipeline

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  security-and-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Secret Scan
        run: python scripts/safety_guard.py --scan-file .
      - name: Run ESLint & TypeCheck
        run: |
          pnpm install --frozen-lockfile
          pnpm tsc --noEmit
          pnpm lint

  build-and-push:
    needs: [security-and-lint]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build Container Image
        uses: docker/build-push-action@v5
        with:
          context: .
          load: true
          tags: app:test
      - name: Scan Image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app:test'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

---

## 4. Kubernetes NetworkPolicy (Zero-Trust Pod Isolation)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-db-isolation
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgres-db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-service
      ports:
        - protocol: TCP
          port: 5432
```

---

## 5. OpenTelemetry Collector DaemonSet Configuration

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
        - name: otel-collector
          image: otel/opentelemetry-collector-contrib:0.95.0
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          ports:
            - containerPort: 4317 # OTLP gRPC
            - containerPort: 4318 # OTLP HTTP
            - containerPort: 8889 # Prometheus metrics exporter
```

---

## 6. Subagent Delegation Matrix

| Subagent | Role & Objective | Invocation Trigger |
|----------|------------------|--------------------|
| `cloud-architect` | Modular IaC design, Kubernetes topologies | Infrastructure change |
| `terraform-linter` | Trivy / tfsec scans, tagging compliance | Before Terraform apply |
| `container-security-reviewer` | Multi-stage Dockerfile audit, non-root user | Image build or base change |
| `ci-cd-runner` | GitHub Actions pipeline engineering | CI/CD automation task |
| `sre-observability-gate` | Prometheus rules, SLI/SLO dashboards | Release verification |
