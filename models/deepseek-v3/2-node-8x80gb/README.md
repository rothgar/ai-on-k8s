# DeepSeek-V3 — 2 Nodes × 8× 80 GB GPUs (TP=8, PP=2)

Serves [deepseek-ai/DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3) via vLLM with FP8 quantization across **2 Kubernetes nodes**, each with 8× 80 GB GPUs (full DGX H100 nodes). Uses tensor parallelism within each node (TP=8) and pipeline parallelism across nodes (PP=2). Total: 1280 GB VRAM.

DeepSeek-V3 is a 671B parameter Mixture-of-Experts model. Uses `--enable-expert-parallel` for efficient MoE routing.

Uses [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) — the LWS controller must be installed before deploying.

See also: [`../4-node-4x80gb/`](../4-node-4x80gb/)

## Requirements

| | |
|---|---|
| **Nodes** | 2 Kubernetes nodes, each with 8× GPUs ≥ 80 GB VRAM (e.g. DGX H100) |
| **Total VRAM** | 1280 GB (2 × 8 × 80 GB) |
| **Storage** | 750 Gi, **ReadWriteMany** StorageClass |
| **Secret** | `huggingface-token` in namespace `deepseek-v3` |
| **Controller** | LeaderWorkerSet — see [`infrastructure/lws/`](../../../infrastructure/lws/) |

> **Storage:** Multi-node deployments use a shared ReadWriteMany PVC so model weights are downloaded once and shared across all nodes. If your StorageClass only supports ReadWriteOnce, see the [prerequisites guide](../../../docs/prerequisites.md#multi-node-storage).

## Prerequisites

Install LeaderWorkerSet if not already present:

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/lws
```

Create the namespace and secret:

```bash
kubectl create namespace deepseek-v3
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n deepseek-v3
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/deepseek-v3/2-node-8x80gb
```

Or from a local clone:

```bash
kubectl apply -k models/deepseek-v3/2-node-8x80gb/
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
  name: deepseek-v3
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/deepseek-v3/2-node-8x80gb
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
  name: deepseek-v3
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/deepseek-v3/2-node-8x80gb
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
          target:
            kind: PersistentVolumeClaim
  destination:
    server: https://kubernetes.default.svc
    namespace: deepseek-v3
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.deepseek-v3.svc.cluster.local:8000/v1
```

Models served: `deepseek-v3`
