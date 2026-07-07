# Qwen3-35B (Qwen3.6-35B-A3B) — 4× 24 GB GPUs (TP=4)

Serves [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) via vLLM across 4 GPUs using tensor parallelism (TP=4). All 4 GPUs must be on the **same node** (e.g. a node with 4× RTX 3090 or 4× RTX 4090).

> A single GB10 node (128 GB unified memory) can also run this model — see [`../1x128gb/`](../1x128gb/) for a simpler single-GPU config with larger context.

See also: [`../1x128gb/`](../1x128gb/) · [`../2x40gb/`](../2x40gb/)

## Requirements

| | |
|---|---|
| **GPUs** | 4× GPUs with ≥ 24 GB VRAM each, on the **same node** |
| **Storage** | 80 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `qwen3-35b` |

## Prerequisites

```bash
kubectl create namespace qwen3-35b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-35b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-35b/4x24gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-35b/4x24gb/
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
  name: qwen3-35b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-35b/4x24gb
  prune: true
  timeout: 20m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-35b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-35b/4x24gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-35b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-35b.svc.cluster.local:8000/v1
```

Models served: `qwen3-35b`, `qwen3.6-35b-a3b`
