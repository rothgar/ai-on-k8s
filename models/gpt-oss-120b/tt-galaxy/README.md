# GPT-OSS 120B — Tenstorrent Galaxy (T3K, TP=8)

Serves [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) via the Tenstorrent vLLM backend on a **Galaxy server** (T3K topology: 8× N300 modules, 16× Wormhole B0 dies) using tensor parallelism (TP=8).

See also: [`../1x128gb/`](../1x128gb/) (NVIDIA GB200) · [`../2-node-8x80gb/`](../2-node-8x80gb/) (NVIDIA DGX)

## Requirements

| | |
|---|---|
| **Device** | 1× Tenstorrent Galaxy (T3K, 8× N300) |
| **Storage** | 200 Gi, any StorageClass |
| **Hugepages** | 256 Gi of 1 Gi hugepages on the node |
| **Memory** | 512 Gi system RAM |
| **CPU** | 16 cores |
| **Secret** | `huggingface-token` in namespace `gpt-oss-120b` |
| **Operator** | tt-operator — see [`infrastructure/tt-operator/`](../../../infrastructure/tt-operator/) |

> **First run:** Tenstorrent hardware compiles model kernels on first startup. Expect up to 60–90 minutes before the endpoint becomes ready for a model this size.

## Prerequisites

```bash
kubectl create namespace gpt-oss-120b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n gpt-oss-120b
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//models/gpt-oss-120b/tt-galaxy
```

Or from a local clone:

```bash
kubectl apply -k models/gpt-oss-120b/tt-galaxy/
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
  path: ./models/gpt-oss-120b/tt-galaxy
  prune: true
  timeout: 120m
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
    path: models/gpt-oss-120b/tt-galaxy
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
