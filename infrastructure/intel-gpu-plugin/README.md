# Intel GPU Device Plugin

Installs the [Intel Device Plugins Operator](https://github.com/intel/intel-device-plugins-for-kubernetes), which discovers Intel GPUs (Arc, Flex, Max series) and exposes them as `gpu.intel.com/i915` schedulable resources.

If your cluster already has the Intel GPU device plugin installed, skip this and deploy models directly.

## What this installs

- Intel Device Plugins Operator via HelmRelease (requires Flux helm-controller)
- `GpuDevicePlugin` CR that deploys the GPU device plugin DaemonSet
- Exposes `gpu.intel.com/i915` on nodes with Intel GPUs
- Operator namespace: `intel-device-plugins`

> **Note:** This uses a HelmRelease CRD and requires [Flux](https://fluxcd.io) with the helm-controller installed. To install without Flux:
> ```bash
> helm repo add intel https://intel.github.io/helm-charts
> helm install intel-device-plugins-operator intel/intel-device-plugins-operator \
>   --namespace intel-device-plugins --create-namespace
> ```

## Talos Prerequisites

Intel Arc and Intel Data Center GPU (Flex/Max) support on Talos requires a system extension for the GPU firmware and kernel driver. Use `i915` for Arc A-series (Alchemist) and older; use `xe` for Arc B-series (Battlemage) and newer Intel GPUs.

**Arc A-series — Schematic ID** (extension: `i915`):
```
dc8730aa8cc7bfa5ef7e2b3284248f2631135b2faf4ae11aa997a0c1987b0eee
```

```bash
talosctl upgrade --image factory.talos.dev/installer/dc8730aa8cc7bfa5ef7e2b3284248f2631135b2faf4ae11aa997a0c1987b0eee:v1.13.5 \
  -n <gpu-node-ip>
```

**Arc B-series and newer — Schematic ID** (extension: `xe`):
```
07d2e0789ba25df7b83db46fde66fad289da2fed89e1fb498e08215816c65d7a
```

```bash
talosctl upgrade --image factory.talos.dev/installer/07d2e0789ba25df7b83db46fde66fad289da2fed89e1fb498e08215816c65d7a:v1.13.5 \
  -n <gpu-node-ip>
```

**Machine config patch for i915 nodes (`gpu-patch.yaml`):**

```yaml
machine:
  kernel:
    modules:
      - name: i915
```

**Machine config patch for xe nodes (`gpu-patch.yaml`):**

```yaml
machine:
  kernel:
    modules:
      - name: xe
```

Apply with: `talosctl patch mc --patch @gpu-patch.yaml -n <gpu-node-ip>`

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/intel-gpu-plugin
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/intel-gpu-plugin/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: intel-gpu-plugin
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/intel-gpu-plugin
  prune: true
  timeout: 10m
```

## Verify

```bash
kubectl get nodes -o json | jq '.items[].status.allocatable | with_entries(select(.key | startswith("gpu.intel")))'
```

Intel GPU nodes should show `gpu.intel.com/i915` in their allocatable resources.

## Models using this plugin

Any model variant directory prefixed with `intel-` (e.g., `intel-2x16gb`) uses `gpu.intel.com/i915` resources and the Intel XPU vLLM image.
