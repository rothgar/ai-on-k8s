# Gemma 4 2B IT — 1× 8 GB GPU

Serves [google/gemma-4-2b-it](https://huggingface.co/google/gemma-4-2b-it) via vLLM with an OpenAI-compatible API on port 8000.

> **Note:** Gemma models require accepting Google's model license on HuggingFace before your token grants access.

## Requirements

| | |
|---|---|
| **GPU** | 1× GPU with ≥ 8 GB VRAM |
| **Storage** | 10 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `gemma-4-2b-it` |

## Prerequisites

Accept the [Gemma model license](https://huggingface.co/google/gemma-4-2b-it) on HuggingFace, then:

```bash
kubectl create namespace gemma-4-2b-it
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n gemma-4-2b-it
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/gemma-4-2b-it/1x8gb
```

Or from a local clone:

```bash
kubectl apply -k models/gemma-4-2b-it/1x8gb/
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
  name: gemma-4-2b-it
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/gemma-4-2b-it/1x8gb
  prune: true
  timeout: 15m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gemma-4-2b-it
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/gemma-4-2b-it/1x8gb
  destination:
    server: https://kubernetes.default.svc
    namespace: gemma-4-2b-it
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.gemma-4-2b-it.svc.cluster.local:8000/v1
```

Models served: `gemma-4-2b-it`
