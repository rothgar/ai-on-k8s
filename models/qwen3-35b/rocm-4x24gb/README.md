# Qwen3-35B — AMD ROCm 4× 24 GB GPUs (TP=4)

Serves [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) via vLLM across **4 AMD GPUs** with 24 GB VRAM each (e.g. 4× RX 7900 XTX), using tensor parallelism (TP=4). Total: 96 GB VRAM.

See also: [`../4x24gb/`](../4x24gb/) (NVIDIA) · [`../2x40gb/`](../2x40gb/) (NVIDIA)

## Requirements

| | |
|---|---|
| **GPUs** | 4× AMD GPUs ≥ 24 GB VRAM, on the same node |
| **Storage** | 80 Gi, any StorageClass |
| **Secret** | `huggingface-token` in namespace `qwen3-35b` |
| **Operator** | AMD GPU Operator — see [`infrastructure/rocm-operator/`](../../../infrastructure/rocm-operator/) |

> **FP8:** This config uses the FP8-quantized model. AMD Instinct MI300-series GPUs support native FP8; RDNA3 consumer GPUs (RX 7900 XTX) will run the model in BF16 fallback mode via vLLM's automatic quantization handling.

## Prerequisites

```bash
kubectl create namespace qwen3-35b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-35b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/qwen3-35b/rocm-4x24gb
```

Or from a local clone:

```bash
kubectl apply -k models/qwen3-35b/rocm-4x24gb/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: qwen3-35b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-35b/rocm-4x24gb
  prune: true
  timeout: 15m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qwen3-35b
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: models/qwen3-35b/rocm-4x24gb
  destination:
    server: https://kubernetes.default.svc
    namespace: qwen3-35b
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://vllm.qwen3-35b.svc.cluster.local:8000/v1
```

Models served: `qwen3-35b`, `qwen3.6-35b-a3b`
