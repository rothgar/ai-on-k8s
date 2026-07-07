# LiteLLM

An LLM gateway that provides a unified OpenAI-compatible API across multiple model backends. Add your deployed vLLM services to its ConfigMap and expose a single endpoint to clients like [Open WebUI](../open-webui/).

- **Image**: `ghcr.io/berriai/litellm`
- **Port**: 4000
- **Config**: `litellm-config` ConfigMap — `model_list` is empty by default; patch in your models

## Requirements

| | |
|---|---|
| **Dependencies** | One or more vLLM services in the cluster |

## Prerequisites

```bash
kubectl create namespace litellm
```

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//apps/litellm
```

Or from a local clone:

```bash
kubectl apply -k apps/litellm/
```

## Add Models

The default `model_list` in the ConfigMap is empty. Add your deployed models by patching the ConfigMap in your Flux or ArgoCD configuration:

```yaml
patches:
  - patch: |
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: litellm-config
        namespace: litellm
      data:
        config.yaml: |
          model_list:
            - model_name: qwen3-35b
              litellm_params:
                model: openai/qwen3-35b
                api_base: http://vllm.qwen3-35b.svc.cluster.local:8000/v1
                api_key: none
            - model_name: deepseek-v3
              litellm_params:
                model: openai/deepseek-v3
                api_base: http://vllm.deepseek-v3.svc.cluster.local:8000/v1
                api_key: none
    target:
      kind: ConfigMap
      name: litellm-config
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: litellm
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./apps/litellm
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: litellm
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: apps/litellm
  destination:
    server: https://kubernetes.default.svc
    namespace: litellm
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## API Endpoint

```
http://litellm.litellm.svc.cluster.local:4000/v1
```
