# AMD GPU Operator

Installs the [AMD GPU Operator](https://github.com/ROCm/gpu-operator), which discovers AMD GPUs on Kubernetes nodes and exposes them as schedulable resources via the `amd.com/gpu` device plugin.

If your cluster already has the AMD GPU Operator or ROCm device plugin installed, skip this and deploy models directly.

## What this installs

- AMD GPU Operator via HelmRelease (requires Flux helm-controller)
- Node Feature Discovery for AMD GPU node labeling
- Device plugin exposing `amd.com/gpu` on GPU nodes
- Operator namespace: `amd-gpu-operator`

> **Note:** This uses a HelmRelease CRD and requires [Flux](https://fluxcd.io) with the helm-controller installed. To install without Flux:
> ```bash
> helm repo add rocm https://rocm.github.io/gpu-operator
> helm install amd-gpu-operator rocm/gpu-operator \
>   --namespace amd-gpu-operator --create-namespace
> ```

## Talos Prerequisites

AMD GPU support on Talos requires the `amdgpu` system extension, which provides AMD GPU firmware and kernel modules.

**Schematic ID** (extension: `amdgpu`):
```
74b14c6bce8dbecd928887731c64ceef5c0ecf9205059d44dbe92f66277edcff
```

**Install or upgrade GPU nodes:**

```bash
talosctl upgrade --image factory.talos.dev/installer/74b14c6bce8dbecd928887731c64ceef5c0ecf9205059d44dbe92f66277edcff:v1.13.5 \
  -n <gpu-node-ip>
```

**Machine config patch for GPU nodes (`gpu-patch.yaml`):**

```yaml
machine:
  kernel:
    modules:
      - name: amdgpu
```

Apply with: `talosctl patch mc --patch @gpu-patch.yaml -n <gpu-node-ip>`

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/rocm-operator
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/rocm-operator/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: rocm-operator
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/rocm-operator
  prune: true
  timeout: 10m
```

## Verify

```bash
kubectl get nodes -o json | jq '.items[].status.allocatable | with_entries(select(.key | startswith("amd")))'
```

AMD GPU nodes should show `amd.com/gpu` in their allocatable resources.

## Models using this operator

Any model variant directory prefixed with `rocm-` (e.g., `rocm-4x24gb`) uses `amd.com/gpu` resources and the ROCm vLLM image. The `/dev/kfd` and `/dev/dri` device paths must be present on the node.
