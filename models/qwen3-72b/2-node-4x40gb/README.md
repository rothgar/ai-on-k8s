# Qwen3-72B — 2 Nodes × 4× 40 GB GPUs (TP=4, PP=2)

Serves [Qwen/Qwen3-72B](https://huggingface.co/Qwen/Qwen3-72B) via vLLM across **2 Kubernetes nodes**, each with 4× 40 GB GPUs, using tensor parallelism within each node (TP=4) and pipeline parallelism across nodes (PP=2). Total: 320 GB VRAM across 8 GPUs.

Uses [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) — the LWS controller must be installed before deploying.

See also: [`../2x80gb/`](../2x80gb/) · [`../4-node-2x40gb/`](../4-node-2x40gb/)

## Requirements

| | |
|---|---|
| **Nodes** | 2 Kubernetes nodes, each with 4× GPUs ≥ 40 GB VRAM |
| **Total VRAM** | 320 GB (2 × 4 × 40 GB) |
| **Storage** | 160 Gi, **ReadWriteMany** StorageClass |
| **StorageClass** | `local-path` (default) — must support RWX |
| **Secret** | `huggingface-token` in namespace `qwen3-72b` |
| **Controller** | LeaderWorkerSet — see [`infrastructure/lws/`](../../../infrastructure/lws/) |

> **Storage:** Multi-node deployments use a shared ReadWriteMany PVC so model weights are downloaded once and shared across all nodes. If your StorageClass only supports ReadWriteOnce, see the [prerequisites guide](../../../docs/prerequisites.md#multi-node-storage).

## Prerequisites

Install LeaderWorkerSet if not already present:

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/lws
```

Create the namespace and secret:

```bash
kubectl create namespace qwen3-72b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-72b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-72b/2-node-4x40gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-72b/2-node-4x40gb/
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
  path: ./models/qwen3-72b/2-node-4x40gb
  prune: true
  timeout: 30m
  patches:
    - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
      target:
        kind: PersistentVolumeClaim
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
    path: models/qwen3-72b/2-node-4x40gb
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
          target:
            kind: PersistentVolumeClaim
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
