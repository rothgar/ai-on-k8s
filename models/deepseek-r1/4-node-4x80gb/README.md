# DeepSeek-R1 — 4 Nodes × 4× 80 GB GPUs (TP=4, PP=4)

Serves [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1) via vLLM with FP8 quantization across **4 Kubernetes nodes**, each with 4× 80 GB GPUs. Uses tensor parallelism within each node (TP=4) and pipeline parallelism across nodes (PP=4). Total: 1280 GB VRAM across 16 GPUs.

DeepSeek-R1 is a 671B parameter Mixture-of-Experts reasoning model. Uses `--enable-expert-parallel` and `--reasoning-parser deepseek_r1` for chain-of-thought output.

Uses [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) — the LWS controller must be installed before deploying.

See also: [`../2-node-8x80gb/`](../2-node-8x80gb/)

## Requirements

| | |
|---|---|
| **Nodes** | 4 Kubernetes nodes, each with 4× GPUs ≥ 80 GB VRAM |
| **Total VRAM** | 1280 GB (4 × 4 × 80 GB) |
| **Storage** | 750 Gi, **ReadWriteMany** StorageClass |
| **Secret** | `huggingface-token` in namespace `deepseek-r1` |
| **Controller** | LeaderWorkerSet — see [`infrastructure/lws/`](../../../infrastructure/lws/) |

> **Storage:** Multi-node deployments use a shared ReadWriteMany PVC so model weights are downloaded once and shared across all nodes. If your StorageClass only supports ReadWriteOnce, see the [prerequisites guide](../../../docs/prerequisites.md#multi-node-storage).

## Prerequisites

Install LeaderWorkerSet if not already present:

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/lws
```

Create the namespace and secret:

```bash
kubectl create namespace deepseek-r1
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n deepseek-r1
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/deepseek-r1/4-node-4x80gb
```

Or from a local clone:

```bash
kubectl apply -k models/deepseek-r1/4-node-4x80gb/
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
  name: deepseek-r1
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/deepseek-r1/4-node-4x80gb
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
  name: deepseek-r1
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/deepseek-r1/4-node-4x80gb
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
          target:
            kind: PersistentVolumeClaim
  destination:
    server: https://kubernetes.default.svc
    namespace: deepseek-r1
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.deepseek-r1.svc.cluster.local:8000/v1
```

Models served: `deepseek-r1`
