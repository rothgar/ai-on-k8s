# Qwen3-14B — 1× 40 GB GPU

Serves [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) via vLLM with an OpenAI-compatible API on port 8000. Runs in FP8 on a single 40 GB GPU (A100 40 GB, RTX A6000, etc.).

## Requirements

| | |
|---|---|
| **GPU** | 1× GPU with ≥ 40 GB VRAM (e.g. A100 40GB, RTX A6000) |
| **Storage** | 40 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `qwen3-14b` |

See also: [`../2x16gb/`](../2x16gb/) to run this model across 2× 16 GB GPUs.

## Prerequisites

```bash
kubectl create namespace qwen3-14b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-14b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-14b/1x40gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-14b/1x40gb/
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
  name: qwen3-14b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-14b/1x40gb
  prune: true
  timeout: 15m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-14b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-14b/1x40gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-14b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-14b.svc.cluster.local:8000/v1
```

Models served: `qwen3-14b`
