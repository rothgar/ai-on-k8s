# Local Path Provisioner

Installs [Rancher's local-path-provisioner](https://github.com/rancher/local-path-provisioner), which creates a `local-path` StorageClass backed by node-local storage. This is the default StorageClass assumed by all model PVCs in this repository.

**This component is optional.** If your cluster already has a StorageClass (e.g., Ceph, Longhorn, NFS), skip this and patch the StorageClass name in your Flux or ArgoCD configuration instead. See [docs/prerequisites.md](../../docs/prerequisites.md) for details.

> **Single-node models** work with ReadWriteOnce StorageClasses including `local-path`. **Multi-node models** require a ReadWriteMany StorageClass — `local-path` does not support RWX and is not suitable for multi-node deployments.

## What this installs

- `local-path-provisioner` Deployment in `local-path-storage` namespace
- `local-path` StorageClass (set as default)
- Storage backed by `/opt/local-path-provisioner` on each node

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/local-path-provisioner
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/local-path-provisioner/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: local-path-provisioner
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/local-path-provisioner
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: local-path-provisioner
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: infrastructure/local-path-provisioner
  destination:
    server: https://kubernetes.default.svc
    namespace: local-path-storage
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Verify

```bash
kubectl get storageclass local-path
```
