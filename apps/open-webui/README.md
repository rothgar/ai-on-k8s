# Open WebUI

A self-hosted chat interface for interacting with LLMs. Connects to any OpenAI-compatible API — point it at [litellm](../litellm/) for a unified gateway or directly at a vLLM service endpoint.

- **Image**: `ghcr.io/open-webui/open-webui`
- **Port**: 8080
- **Storage**: 10 Gi PVC for chat history and settings

## Requirements

| | |
|---|---|
| **Storage** | 10 Gi, any StorageClass |
| **LLM backend** | litellm or a vLLM service in the cluster |

## Prerequisites

```bash
kubectl create namespace open-webui
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//apps/open-webui
```

Or from a local clone:

```bash
kubectl apply -k apps/open-webui/
```

By default, Open WebUI connects to litellm at `http://litellm.litellm.svc.cluster.local:4000/v1`. To connect directly to a vLLM service instead, patch the `OPENAI_API_BASE_URL` environment variable:

```yaml
# In your Flux Kustomization or ArgoCD Application:
patches:
  - patch: |
      - op: replace
        path: /spec/template/spec/containers/0/env/0/value
        value: http://vllm.qwen3-35b.svc.cluster.local:8000/v1
    target:
      kind: Deployment
      name: open-webui
```

## Access

Expose the service with a LoadBalancer or Ingress:

```bash
kubectl port-forward -n open-webui svc/open-webui 8080:8080
```

Then open `http://localhost:8080`.

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: open-webui
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./apps/open-webui
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: open-webui
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: apps/open-webui
  destination:
    server: https://kubernetes.default.svc
    namespace: open-webui
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
