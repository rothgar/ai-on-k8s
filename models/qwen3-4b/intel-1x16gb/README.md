# Qwen3-4B — Intel Arc 1× 16 GB GPU

Serves [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) via vLLM on a **single Intel Arc GPU** with 16 GB VRAM (e.g. Arc A770, Arc B770).

See also: [`../1x8gb/`](../1x8gb/) (NVIDIA)

## Requirements

| | |
|---|---|
| **GPU** | 1× Intel Arc GPU ≥ 16 GB VRAM |
| **Storage** | 15 Gi, any StorageClass |
| **Secret** | `huggingface-token` in namespace `qwen3-4b` |
| **Plugin** | Intel GPU Device Plugin — see [`infrastructure/intel-gpu-plugin/`](../../../infrastructure/intel-gpu-plugin/) |

## Prerequisites

```bash
kubectl create namespace qwen3-4b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-4b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-4b/intel-1x16gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-4b/intel-1x16gb/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: qwen3-4b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-4b/intel-1x16gb
  prune: true
  timeout: 15m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-4b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-4b/intel-1x16gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-4b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-4b.svc.cluster.local:8000/v1
```

Models served: `qwen3-4b`
