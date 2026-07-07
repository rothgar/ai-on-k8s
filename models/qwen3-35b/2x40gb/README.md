# Qwen3-35B (Qwen3.6-35B-A3B) — 2× 40 GB GPUs (TP=2)

Serves [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) via vLLM across 2 GPUs on a single node using tensor parallelism (TP=2). Suited for nodes with two 40 GB A100s or similar (2× A100 40GB, 2× RTX 6000 Ada).

See also: [`../1x128gb/`](../1x128gb/) · [`../4x24gb/`](../4x24gb/) for other GPU topologies.

## Requirements

| | |
|---|---|
| **GPUs** | 2× GPUs with ≥ 40 GB VRAM each, on the **same node** |
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
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-35b/2x40gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-35b/2x40gb/
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
  path: ./models/qwen3-35b/2x40gb
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
    path: models/qwen3-35b/2x40gb
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
