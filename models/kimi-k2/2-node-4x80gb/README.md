# Kimi-K2 — 2 Nodes × 4× 80 GB GPUs (TP=4, PP=2)

Serves [moonshotai/Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) via vLLM with FP8 quantization across **2 Kubernetes nodes**, each with 4× 80 GB GPUs. Uses tensor parallelism within each node (TP=4) and pipeline parallelism across nodes (PP=2). Total: 640 GB VRAM.

Kimi K2 is a Mixture-of-Experts model optimized for agentic tasks and tool use. Uses `--enable-expert-parallel` for efficient MoE routing.

Uses [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) — the LWS controller must be installed before deploying.

See also: [`../4-node-2x80gb/`](../4-node-2x80gb/)

## Requirements

| | |
|---|---|
| **Nodes** | 2 Kubernetes nodes, each with 4× GPUs ≥ 80 GB VRAM |
| **Total VRAM** | 640 GB (2 × 4 × 80 GB) |
| **Storage** | 400 Gi, **ReadWriteMany** StorageClass |
| **Secret** | `huggingface-token` in namespace `kimi-k2` |
| **Controller** | LeaderWorkerSet — see [`infrastructure/lws/`](../../../infrastructure/lws/) |

> **Storage:** Multi-node deployments use a shared ReadWriteMany PVC so model weights are downloaded once and shared across all nodes. If your StorageClass only supports ReadWriteOnce, see the [prerequisites guide](../../../docs/prerequisites.md#multi-node-storage).

## Prerequisites

Install LeaderWorkerSet if not already present:

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/lws
```

Create the namespace and secret:

```bash
kubectl create namespace kimi-k2
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n kimi-k2
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/kimi-k2/2-node-4x80gb
```

Or from a local clone:

```bash
kubectl apply -k models/kimi-k2/2-node-4x80gb/
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
  name: kimi-k2
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/kimi-k2/2-node-4x80gb
  prune: true
  timeout: 60m
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
  name: kimi-k2
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/kimi-k2/2-node-4x80gb
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
          target:
            kind: PersistentVolumeClaim
  destination:
    server: https://kubernetes.default.svc
    namespace: kimi-k2
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.kimi-k2.svc.cluster.local:8000/v1
```

Models served: `kimi-k2`
