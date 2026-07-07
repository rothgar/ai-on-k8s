# Qwen3-35B (Qwen3.6-35B-A3B) — 1× 128 GB GPU

Serves [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) via vLLM with an OpenAI-compatible API on port 8000. This is a Mixture-of-Experts model with 35B total parameters and ~3.6B active per token, served in FP8 on a single high-VRAM GPU.

Ideal for: **NVIDIA GB10 (DGX Spark)**, GB200, or any GPU with ≥ 128 GB unified/HBM memory. Supports up to 131K token context.

See also: [`../2x40gb/`](../2x40gb/) · [`../4x24gb/`](../4x24gb/) for multi-GPU topologies.

## Requirements

| | |
|---|---|
| **GPU** | 1× GPU with ≥ 128 GB VRAM (e.g. GB10, GB200, H200 NVL) |
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
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-35b/1x128gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-35b/1x128gb/
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
  path: ./models/qwen3-35b/1x128gb
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
    path: models/qwen3-35b/1x128gb
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
