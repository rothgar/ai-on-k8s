# Qwen3-8B — Tenstorrent N150 (Wormhole)

Serves [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) via the Tenstorrent vLLM backend on a **single N150** Wormhole card using the `tt` device target.

See also: [`../tt-n300/`](../tt-n300/) · [`../1x16gb/`](../1x16gb/) (NVIDIA)

## Requirements

| | |
|---|---|
| **Device** | 1× Tenstorrent N150 (Wormhole B0) |
| **Storage** | 25 Gi, any StorageClass |
| **Hugepages** | 32 Gi of 1 Gi hugepages on the node |
| **Secret** | `huggingface-token` in namespace `qwen3-8b` |
| **Operator** | tt-operator — see [`infrastructure/tt-operator/`](../../../infrastructure/tt-operator/) |

> **First run:** Tenstorrent hardware compiles model kernels on first startup. Expect 30–60 minutes before the endpoint becomes ready.

## Prerequisites

```bash
kubectl create namespace qwen3-8b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-8b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-8b/tt-n150
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-8b/tt-n150/
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
  path: ./models/qwen3-8b/tt-n150
  prune: true
  timeout: 90m
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
    path: models/qwen3-8b/tt-n150
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
