# GPT-OSS 120B — 1× 128 GB GPU

Serves [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) via vLLM with mxfp4 quantization and fp8 KV cache on a single high-VRAM GPU. Uses the NVIDIA vLLM container image for optimized CUTLASS MoE kernels.

> **Note:** Requires accepting the model license on HuggingFace.

Ideal for: **NVIDIA GB10 (DGX Spark)**, GB200, or any GPU with ≥ 128 GB memory.

See also: [`../2-node-2x80gb/`](../2-node-2x80gb/) · [`../2-node-8x80gb/`](../2-node-8x80gb/) for multi-node deployments.

## Requirements

| | |
|---|---|
| **GPU** | 1× GPU with ≥ 128 GB VRAM (e.g. GB10, GB200) |
| **Storage** | 150 Gi for model weights |
| **StorageClass** | `local-path` (default) |
| **Secret** | `huggingface-token` in namespace `gpt-oss-120b` |
| **vLLM Image** | `nvcr.io/nvidia/vllm` (NVIDIA-optimized, includes mxfp4 support) |

## Prerequisites

Accept the [model license](https://huggingface.co/openai/gpt-oss-120b) on HuggingFace, then:

```bash
kubectl create namespace gpt-oss-120b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n gpt-oss-120b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/gpt-oss-120b/1x128gb
```

Or from a local clone:

```bash
kubectl apply -k models/gpt-oss-120b/1x128gb/
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
  name: gpt-oss-120b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/gpt-oss-120b/1x128gb
  prune: true
  timeout: 30m
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
    path: models/gpt-oss-120b/1x128gb
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
