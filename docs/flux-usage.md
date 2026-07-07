# Flux Usage

## Single Model

Create a `GitRepository` pointing at this repo, then a `Kustomization` for the specific model variant you want:

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
  name: qwen3-35b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/qwen3-35b/4x24gb
  prune: true
  timeout: 15m
```

## Overriding StorageClass

Pass a patch inline — no changes to this repo needed:

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
  path: ./models/qwen3-35b/4x24gb
  prune: true
  timeout: 15m
  patches:
    - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
      target:
        kind: PersistentVolumeClaim
```

## All Apps

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: ai-apps
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./apps
  prune: true
  timeout: 5m
```

## Multiple Models

Create one `Kustomization` per model, all referencing the same `GitRepository`:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: gemma-4-9b
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./models/gemma-4-9b-it/1x24gb
  prune: true
  timeout: 15m
---
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

## Infrastructure (nvidia-operator, lws)

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: ai-infrastructure
  namespace: flux-system
spec:
  interval: 1h
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure
  prune: true
  timeout: 10m
```

> Infrastructure components use `HelmRelease` CRDs and require Flux's `helm-controller`. The model and app directories do not.
