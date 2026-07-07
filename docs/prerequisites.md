# Prerequisites

Before deploying any model or application from this repository, ensure the following are in place.

## 1. NVIDIA GPU Operator

The GPU operator must be installed with the driver installer **disabled** (Talos Linux manages NVIDIA drivers via system extensions).

A ready-to-use manifest is provided at [`infrastructure/nvidia-operator/`](../infrastructure/nvidia-operator/). If you already have the operator installed, skip this step.

Verify the operator is healthy:
```bash
kubectl get pods -n nvidia-system
```

## 2. StorageClass

All PVCs default to `storageClassName: local-path`. You need either:

- **Rancher local-path-provisioner** (provided at [`infrastructure/local-path-provisioner/`](../infrastructure/local-path-provisioner/))
- **Any other StorageClass** in your cluster — override the name via a patch in your Flux/ArgoCD source definition (see below)

For multi-node models the PVC uses `accessModes: ReadWriteMany`. You need a StorageClass that supports RWX (e.g., CephFS, NFS, Longhorn with RWX enabled). If you only have `ReadWriteOnce` storage, see [Multi-Node Storage](#multi-node-storage) below.

### Overriding StorageClass

Add this patch to your Flux `Kustomization` or ArgoCD `Application` — no changes to this repo needed:

```yaml
# Flux
patches:
  - patch: '{"spec": {"storageClassName": "my-storageclass"}}'
    target:
      kind: PersistentVolumeClaim
```

```yaml
# ArgoCD Application
spec:
  source:
    kustomize:
      patches:
        - patch: '{"spec": {"storageClassName": "my-storageclass"}}'
          target:
            kind: PersistentVolumeClaim
```

## 3. HuggingFace Token Secret

All models pull weights from HuggingFace at startup. Create the secret in each model's namespace **before** deploying:

```bash
kubectl create namespace <model-namespace>
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n <model-namespace>
```

For example, to deploy `qwen3-35b/4x24gb`:
```bash
kubectl create namespace qwen3-35b
kubectl create secret generic huggingface-token \
  --from-literal=token=hf_yourtoken \
  -n qwen3-35b
```

The secret name `huggingface-token` and key `token` are fixed by convention across all models.

> Some models (e.g., `gpt-oss-120b`) require accepting a HuggingFace model license before the token grants access. Accept the license on the model's HuggingFace page before deploying.

## 4. LeaderWorkerSet Controller (multi-node models only)

Multi-node models use the [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) API. Install the controller before deploying any model under a `*-node-*` directory:

```bash
kubectl apply -k infrastructure/lws/
```

Or install directly from upstream:
```bash
kubectl apply --server-side -f https://github.com/kubernetes-sigs/lws/releases/latest/download/manifests.yaml
```

## Multi-Node Storage

Multi-node models (those in `*-node-*` variant directories) use a single `ReadWriteMany` PVC shared across all nodes so model weights are downloaded once. If your StorageClass only supports `ReadWriteOnce`, you have two options:

### Option A: Use a RWX-capable StorageClass
Patch the StorageClass name as shown above. Any RWX-capable provisioner (CephFS, NFS, Longhorn RWX mode) works.

### Option B: Per-node download with ReadWriteOnce
Patch the PVC to `ReadWriteOnce` and add an init container to each pod that downloads weights from HuggingFace independently:

```yaml
patches:
  - patch: |
      - op: replace
        path: /spec/accessModes/0
        value: ReadWriteOnce
    target:
      kind: PersistentVolumeClaim
```

Each pod will then download the full model independently — this uses more storage but works with any StorageClass.
