# Qwen3-8B — 1× 16 GB GPU

Serves [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) via vLLM with an OpenAI-compatible API on port 8000.

## Requirements

| | |
|---|---|
| **GPU** | 1× GPU with ≥ 16 GB VRAM |
| **Storage** | 25 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `qwen3-8b` |

## Prerequisites

```bash
kubectl create namespace qwen3-8b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-8b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-8b/1x16gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-8b/1x16gb/
```

## Flux

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: ai-on-k8s
  namespace: flux-system
spec:
  interval: 1h
  url: https://github.com/siderolabs/ai-on-k8s
  ref:
    branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: qwen3-8b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-8b/1x16gb
  prune: true
  timeout: 15m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-8b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-8b/1x16gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-8b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-8b.svc.cluster.local:8000/v1
```

Models served: `qwen3-8b`
