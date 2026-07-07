# Qwen3-8B — AMD ROCm 1× 24 GB GPU

Serves [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) via vLLM on a **single AMD GPU** with 24 GB VRAM (e.g. RX 7900 XTX, Instinct MI50).

See also: [`../1x16gb/`](../1x16gb/) (NVIDIA) · [`../intel-2x16gb/`](../intel-2x16gb/) (Intel)

## Requirements

| | |
|---|---|
| **GPU** | 1× AMD GPU ≥ 24 GB VRAM |
| **Storage** | 25 Gi, any StorageClass |
| **Secret** | `huggingface-token` in namespace `qwen3-8b` |
| **Operator** | AMD GPU Operator — see [`infrastructure/rocm-operator/`](../../../infrastructure/rocm-operator/) |

## Prerequisites

```bash
kubectl create namespace qwen3-8b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-8b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-8b/rocm-1x24gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-8b/rocm-1x24gb/
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
  path: ./models/qwen3-8b/rocm-1x24gb
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
    path: models/qwen3-8b/rocm-1x24gb
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
