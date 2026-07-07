# Gemma 4 27B IT — 2× 40 GB GPUs (TP=2)

Serves [google/gemma-4-27b-it](https://huggingface.co/google/gemma-4-27b-it) via vLLM across 2 GPUs on a single node using tensor parallelism (TP=2). Suited for nodes with 2× A100 40GB, 2× RTX 6000 Ada, or similar.

> **Note:** Gemma models require accepting Google's model license on HuggingFace before your token grants access.

See also: [`../1x80gb/`](../1x80gb/) to run on a single 80 GB GPU.

## Requirements

| | |
|---|---|
| **GPUs** | 2× GPUs with ≥ 40 GB VRAM each, on the **same node** |
| **Storage** | 70 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `gemma-4-27b-it` |

## Prerequisites

Accept the [Gemma model license](https://huggingface.co/google/gemma-4-27b-it) on HuggingFace, then:

```bash
kubectl create namespace gemma-4-27b-it
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n gemma-4-27b-it
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/gemma-4-27b-it/2x40gb
```

Or from a local clone:

```bash
kubectl apply -k models/gemma-4-27b-it/2x40gb/
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
  name: gemma-4-27b-it
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/gemma-4-27b-it/2x40gb
  prune: true
  timeout: 20m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gemma-4-27b-it
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/gemma-4-27b-it/2x40gb
  destination:
    server: https://kubernetes.default.svc
    namespace: gemma-4-27b-it
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.gemma-4-27b-it.svc.cluster.local:8000/v1
```

Models served: `gemma-4-27b-it`
