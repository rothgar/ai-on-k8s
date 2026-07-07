# Tenstorrent Operator (tt-operator)

Installs the [tt-operator](https://docs.tenstorrent.com/tt-operator/latest/), the umbrella Helm chart that brings Tenstorrent devices (Wormhole and Blackhole families) under Kubernetes management. Handles driver installation, firmware updates, device discovery, and resource allocation.

If your cluster already has tt-operator installed, skip this and deploy models directly.

## What this installs

- tt-operator via HelmRelease (requires Flux helm-controller)
- Node Feature Discovery for Tenstorrent device labeling
- Driver manager — installs `tt-kmd` kernel module on device nodes
- Firmware manager — handles device firmware updates
- DRA driver — allocates devices to pods via `hugepages-1Gi` resources
- Telemetry — Prometheus metrics for device health and utilization
- Operator namespace: `tenstorrent-system`

> **Note:** This uses a HelmRelease CRD and requires [Flux](https://fluxcd.io) with the helm-controller installed. To install without Flux, consult the [tt-operator documentation](https://docs.tenstorrent.com/tt-operator/latest/) for the current Helm repo URL and chart values.

> **Helm repo URL:** The `helmrepository.yaml` in this directory uses `https://tenstorrent.github.io/helm-charts`. Verify this matches the [official docs](https://docs.tenstorrent.com/tt-operator/latest/) for your tt-operator version — Tenstorrent may update the chart location.

## Talos Prerequisites

Tenstorrent devices require the `tenstorrent` system extension, which provides the `tt-kmd` kernel module. This must be present on device nodes before tt-operator can manage them.

**Schematic ID** (extension: `tenstorrent`):
```
f173de223f7284159923ab96cbb8b1ae1d1d08fa9e24d8dec1768b2dd6890516
```

**Install or upgrade device nodes:**

```bash
talosctl upgrade --image factory.talos.dev/installer/f173de223f7284159923ab96cbb8b1ae1d1d08fa9e24d8dec1768b2dd6890516:v1.13.5 \
  -n <device-node-ip>
```

**Machine config patch for device nodes (`tt-patch.yaml`):**

```yaml
machine:
  kernel:
    modules:
      - name: tenstorrent
  sysctls:
    # 32 × 1Gi hugepages — required for DMA access to Tenstorrent devices.
    # Adjust if deploying multiple devices per node (multiply by device count).
    vm.nr_hugepages: "32"
```

Apply with: `talosctl patch mc --patch @tt-patch.yaml -n <device-node-ip>`

> Verify device files are present after the node reboots:
> `talosctl read /proc/modules | grep tenstorrent`
> `talosctl ls /dev/tenstorrent`

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/tt-operator
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/tt-operator/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: tt-operator
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/tt-operator
  prune: true
  timeout: 15m
```

## Verify

```bash
kubectl get pods -n tenstorrent-system
kubectl get nodes --show-labels | grep tenstorrent
```

## Models using this operator

Any model variant directory prefixed with `tt-` (e.g., `tt-t3k`, `tt-galaxy`) uses Tenstorrent hardware. These deployments request `hugepages-1Gi` rather than a GPU resource count, and use the `ghcr.io/tenstorrent/tt-inference-server` image with `VLLM_TARGET_DEVICE=tt`.

### Supported devices

| Device | ARCH_NAME | MESH_DEVICE |
|---|---|---|
| n150 | `wormhole_b0` | `N150` |
| n300 | `wormhole_b0` | `N300` |
| t3k (8× n300) | `wormhole_b0` | `T3K` |
| Galaxy | `wormhole_b0` | `TG` |
| p150 | `blackhole` | `P150` |
| p300 | `blackhole` | `P300` |
