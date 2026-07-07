# ArgoCD Usage

## Single Model

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
    path: models/qwen3-35b/4x24gb
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

## Overriding StorageClass

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
    path: models/qwen3-35b/4x24gb
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
          target:
            kind: PersistentVolumeClaim
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

## All Apps via ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ai-apps
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - app: open-webui
          - app: litellm
          - app: substrate
  template:
    metadata:
      name: "{{app}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/siderolabs/ai-on-k8s
        targetRevision: main
        path: "apps/{{app}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{app}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

## Multiple Models via ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ai-models
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - model: qwen3-4b
            variant: 1x8gb
          - model: gemma-4-9b-it
            variant: 1x24gb
          - model: litellm
            variant: ""
  template:
    metadata:
      name: "{{model}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/siderolabs/ai-on-k8s
        targetRevision: main
        path: "models/{{model}}/{{variant}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{model}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```
