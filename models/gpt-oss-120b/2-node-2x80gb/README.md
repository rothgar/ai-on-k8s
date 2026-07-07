# GPT-OSS 120B — 2 Nodes × 2× 80 GB GPUs (TP=2, PP=2)

Serves [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) via vLLM with mxfp4 quantization across **2 Kubernetes nodes**, each with 2× 80 GB GPUs. Uses tensor parallelism within each node (TP=2) and pipeline parallelism across nodes (PP=2). Total: 320 GB VRAM.

Uses [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws). The LWS controller must be installed before deploying.

See also: [`../1x128gb/`](../1x128gb/) · [`../2-node-8x80gb/`](../2-node-8x80gb/)

## Requirements

| | |
|---|---|
| **Nodes** | 2 Kubernetes nodes, each with 2× GPUs ≥ 80 GB VRAM |
| **Total VRAM** | 320 GB (2 × 2 × 80 GB) |
| **Storage** | 200 Gi, **ReadWriteMany** StorageClass |
| **Secret** | `huggingface-token` in namespace `gpt-oss-120b` |
| **Controller** | LeaderWorkerSet — see [`infrastructure/lws/`](../../../infrastructure/lws/) |

## Prerequisites

Install LeaderWorkerSet, then:

```bash
kubectl create namespace gpt-oss-120b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n gpt-oss-120b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/gpt-oss-120b/2-node-2x80gb
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: gpt-oss-120b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/gpt-oss-120b/2-node-2x80gb
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
  name: gpt-oss-120b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/gpt-oss-120b/2-node-2x80gb
  destination:
    server: https://kubernetes.default.svc
    namespace: gpt-oss-120b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.gpt-oss-120b.svc.cluster.local:8000/v1
```

Models served: `gpt-oss-120b`
