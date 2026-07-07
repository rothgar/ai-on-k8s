# Qwen3-72B — AMD ROCm 1× 192 GB GPU

Serves [Qwen/Qwen3-72B](https://huggingface.co/Qwen/Qwen3-72B) via vLLM on a **single AMD Instinct MI300X** (192 GB HBM3). The full 72B model in BF16 fits comfortably on one MI300X card, eliminating the need for tensor parallelism.

See also: [`../2x80gb/`](../2x80gb/) (NVIDIA 2× H100)

## Requirements

| | |
|---|---|
| **GPU** | 1× AMD Instinct MI300X (192 GB HBM3) |
| **Storage** | 160 Gi, any StorageClass |
| **Secret** | `huggingface-token` in namespace `qwen3-72b` |
| **Operator** | AMD GPU Operator — see [`infrastructure/rocm-operator/`](../../../infrastructure/rocm-operator/) |

## Prerequisites

```bash
kubectl create namespace qwen3-72b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-72b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-72b/rocm-1x192gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-72b/rocm-1x192gb/
```

## Flux

```yaml
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
  path: ./models/qwen3-72b/rocm-1x192gb
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
    path: models/qwen3-72b/rocm-1x192gb
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
