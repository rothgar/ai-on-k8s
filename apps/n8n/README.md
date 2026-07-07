# n8n

A self-hosted workflow automation platform with native AI agent support. Connect to any OpenAI-compatible LLM endpoint — point it at [litellm](../litellm/) or directly at a vLLM service.

- **Image**: `docker.n8n.io/n8nio/n8n`
- **Port**: 5678
- **Storage**: 5 Gi PVC for workflows, credentials, and execution history

## Requirements

| | |
|---|---|
| **Storage** | 5 Gi, any StorageClass |
| **LLM backend** | litellm or a vLLM service in the cluster |

## Prerequisites

```bash
kubectl create namespace n8n
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//apps/n8n
```

Or from a local clone:

```bash
kubectl apply -k apps/n8n/
```

By default n8n's AI nodes point at litellm at `http://litellm.litellm.svc.cluster.local:4000/v1`. To connect directly to a vLLM service, patch `OPENAI_API_BASE_URL`:

```yaml
patches:
  - patch: |
      - op: replace
        path: /spec/template/spec/containers/0/env/5/value
        value: http://vllm.qwen3-8b.svc.cluster.local:8000/v1
    target:
      kind: Deployment
      name: n8n
```

## Access

```bash
kubectl port-forward -n n8n svc/n8n 5678:80
```

Then open `http://localhost:5678`.

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: n8n
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./apps/n8n
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: n8n
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: apps/n8n
  destination:
    server: https://kubernetes.default.svc
    namespace: n8n
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
