# Qwen3-8B — Intel Arc 2× 16 GB GPUs (TP=2)

Serves [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) via vLLM across **2 Intel Arc GPUs** with 16 GB VRAM each (e.g. 2× Arc A770 or 2× Arc B770), using tensor parallelism (TP=2). Total: 32 GB VRAM.

See also: [`../1x16gb/`](../1x16gb/) (NVIDIA) · [`../rocm-1x24gb/`](../rocm-1x24gb/) (AMD)

## Requirements

| | |
|---|---|
| **GPUs** | 2× Intel Arc GPUs ≥ 16 GB VRAM, on the same node |
| **Storage** | 25 Gi, any StorageClass |
| **Secret** | `huggingface-token` in namespace `qwen3-8b` |
| **Plugin** | Intel GPU Device Plugin — see [`infrastructure/intel-gpu-plugin/`](../../../infrastructure/intel-gpu-plugin/) |

## Prerequisites

```bash
kubectl create namespace qwen3-8b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-8b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-8b/intel-2x16gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-8b/intel-2x16gb/
```

## Flux

```yaml
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
  path: ./models/qwen3-8b/intel-2x16gb
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
    path: models/qwen3-8b/intel-2x16gb
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
