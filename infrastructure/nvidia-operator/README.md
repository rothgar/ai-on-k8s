# NVIDIA GPU Operator

Installs the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/overview.html) with `driver.enabled: false`. This configuration is required for **Talos Linux** clusters, where NVIDIA drivers are managed via Talos system extensions rather than by the operator.

If your cluster already has the GPU Operator installed (with or without the driver component), you can skip this and go directly to deploying models.

## What this installs

- GPU Operator via HelmRelease (requires Flux helm-controller)
- Operator namespace: `gpu-operator`
- Driver installer: **disabled** (Talos manages NVIDIA drivers)
- All other operator components: enabled (device plugin, container toolkit, DCGM exporter, etc.)

> **Note:** This uses a HelmRelease CRD and requires [Flux](https://fluxcd.io) with the helm-controller installed. If you are not using Flux, install the GPU Operator using Helm directly:
> ```bash
> helm install gpu-operator nvidia/gpu-operator \
>   --namespace gpu-operator --create-namespace \
>   --set driver.enabled=false
> ```

## Talos Prerequisites

NVIDIA drivers on Talos are managed via system extensions, not the GPU Operator's driver container. GPU nodes must be running a Talos image built with the NVIDIA extensions before deploying this operator.

**Schematic ID** (extensions: `nonfree-kmod-nvidia-production` + `nvidia-container-toolkit-production`):
```
26124abcbd408be693df9fe852c80ef1e6cc178e34d7d7d8430a28d1130b4227
```

**Install or upgrade GPU nodes:**

```bash
talosctl upgrade --image factory.talos.dev/installer/26124abcbd408be693df9fe852c80ef1e6cc178e34d7d7d8430a28d1130b4227:v1.13.5 \
  -n <gpu-node-ip>
```

**Machine config patch for GPU nodes (`gpu-patch.yaml`):**

```yaml
machine:
  kernel:
    modules:
      - name: nvidia
      - name: nvidia_uvm
      - name: nvidia_drm
      - name: nvidia_modeset
```

Apply with: `talosctl patch mc --patch @gpu-patch.yaml -n <gpu-node-ip>`

## Prerequisites

Flux must be installed with the helm-controller and source-controller components. GPU nodes must have the NVIDIA system extensions loaded (see above) before deploying this operator.

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/nvidia-operator
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/nvidia-operator/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: nvidia-operator
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/nvidia-operator
  prune: true
  timeout: 10m
```

## Verify

Once the operator is running, verify GPUs are available:

```bash
kubectl get nodes -o json | jq '.items[].status.allocatable | with_entries(select(.key | startswith("nvidia")))'
```

GPU nodes should show `nvidia.com/gpu` in their allocatable resources.
