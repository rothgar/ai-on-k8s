# Qwen3-14B — 2× 16 GB GPUs (TP=2)

Serves [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) via vLLM across 2 GPUs on a single node using tensor parallelism (TP=2). Suited for nodes with two 16 GB GPUs (e.g. 2× RTX 4080, 2× Tesla T4).

## Requirements

| | |
|---|---|
| **GPUs** | 2× GPUs with ≥ 16 GB VRAM each, on the **same node** |
| **Storage** | 40 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `qwen3-14b` |

> Both GPUs must be on the same node — this uses tensor parallelism (single Deployment), not LeaderWorkerSet.

See also: [`../1x40gb/`](../1x40gb/) to run on a single 40 GB GPU.

## Prerequisites

```bash
kubectl create namespace qwen3-14b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-14b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-14b/2x16gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-14b/2x16gb/
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
  path: ./models/qwen3-14b/2x16gb
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
    path: models/qwen3-14b/2x16gb
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
