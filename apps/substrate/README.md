# Substrate

An actor-based agent orchestration system for running AI workloads on Kubernetes. Substrate manages the lifecycle of agent pods, jobs, and services — creating, monitoring, and cleaning up resources on behalf of running agents.

Requires a ClusterRole with permissions to manage pods, jobs, services, and configmaps across namespaces.

## Requirements

| | |
|---|---|
| **RBAC** | ClusterRole — grants pod/job/service/configmap create, get, list, watch, delete |
| **LLM backend** | Any OpenAI-compatible API (litellm or vLLM directly) |

## Prerequisites

```bash
kubectl create namespace substrate
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//apps/substrate
```

Or from a local clone:

```bash
kubectl apply -k apps/substrate/
```

The kustomization creates a ServiceAccount, ClusterRole, and ClusterRoleBinding in addition to the Deployment and Service.

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: substrate
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./apps/substrate
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: substrate
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: apps/substrate
  destination:
    server: https://kubernetes.default.svc
    namespace: substrate
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
