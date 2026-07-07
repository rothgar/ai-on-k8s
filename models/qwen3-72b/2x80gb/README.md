# Qwen3-72B — 2× 80 GB GPUs (TP=2)

Serves [Qwen/Qwen3-72B](https://huggingface.co/Qwen/Qwen3-72B) via vLLM across 2 GPUs on a **single node** using tensor parallelism (TP=2). Suited for nodes with 2× H100 80GB or 2× A100 80GB.

See also: [`../2-node-4x40gb/`](../2-node-4x40gb/) · [`../4-node-2x40gb/`](../4-node-2x40gb/) for multi-node configurations.

## Requirements

| | |
|---|---|
| **GPUs** | 2× GPUs with ≥ 80 GB VRAM each, on the **same node** |
| **Storage** | 160 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `qwen3-72b` |

## Prerequisites

```bash
kubectl create namespace qwen3-72b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-72b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-72b/2x80gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-72b/2x80gb/
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
  name: qwen3-72b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-72b/2x80gb
  prune: true
  timeout: 30m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-72b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-72b/2x80gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-72b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-72b.svc.cluster.local:8000/v1
```

Models served: `qwen3-72b`
