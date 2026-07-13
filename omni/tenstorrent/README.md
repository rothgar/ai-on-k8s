# Tenstorrent — Omni Cluster Templates

Single-node Talos Linux cluster templates for Tenstorrent hardware, provisioned via [Siderolabs Omni](https://omni.siderolabs.com/).

## Templates

| Directory | Card | Architecture | Chips | VRAM | Model |
|---|---|---|---|---|---|
| `n150/` | Wormhole N150 | Wormhole | 1 | 12 GB | google/gemma-4-12B-it |
| `n300/` | Wormhole N300 | Wormhole | 2 | 24 GB | google/gemma-4-12B-it (TP=2) |
| `p150/` | Blackhole P150 | Blackhole | 1 | 32 GB | Qwen/Qwen3-14B |
| `2xp150/` | 2× Blackhole P150 | Blackhole | 2 | 64 GB | Qwen/Qwen3-32B (TP=2) |
| `quietboxv2/` | TT-QuietBox v2 (4× P150) | Blackhole | 4 | 128 GB | Qwen/Qwen3.6-35B-A3B (TP=4) |

> **Multi-card templates** (`2xp150/`, `quietboxv2/`) require the inter-chip Ethernet links to be configured before deploying. On the TT-QuietBox this is done via the baseboard; on custom builds use `tt-topology -l mesh` after driver installation.

## What Every Template Deploys

| Component | Namespace | Description |
|---|---|---|
| tt-operator (NFD) | `tt-operator-system` | Node Feature Discovery — detects the card and labels the node |
| tt-k8s-driver-manager | `tt-operator-system` | Firmware upgrade controller (see Firmware Upgrades below) |
| tt-telemetry | `tt-operator-system` | Per-device metrics collector; NodePort 30080 |
| vLLM inference server | `<model-name>` | TT Metal backend; model weights at `/var/mnt/llm-models` |
| Open WebUI | `open-webui` | Chat interface connecting to the vLLM service |

## Requirements

- Siderolabs Omni account with the machine enrolled
- [`omnictl`](https://omni.siderolabs.com/docs/how-to-guides/how-to-install-and-configure-omnictl/) installed and authenticated
- [`envsubst`](https://www.gnu.org/software/gettext/) (`gettext` package on most systems)
- HuggingFace token with access to the model in the chosen template

## Deploy

```bash
cd /path/to/ai-on-k8s   # must run from repo root

export MACHINE_UUID=<uuid>    # from Omni UI or: omnictl get machines
export HF_TOKEN=hf_xxx
export CLUSTER_NAME=<name>

envsubst '${MACHINE_UUID} ${HF_TOKEN} ${CLUSTER_NAME}' \
  < omni/tenstorrent/<variant>/cluster.yaml > /tmp/tt-cluster.yaml
omnictl cluster template sync --verbose -f /tmp/tt-cluster.yaml
```

## Talos Configuration (all templates)

| Setting | Value |
|---|---|
| Talos version | v1.13.6 |
| Kubernetes version | v1.36.2 |
| System extension | `siderolabs/tenstorrent` (provides `tt-kmd` kernel driver) |
| Kernel args | `hugepagesz=1G hugepages=32` (32 GiB reserved for TT Metal DMA) |
| Control plane scheduling | Enabled (single-node) |
| Install disk | `/dev/nvme0n1` |
| LLM storage | 50–200 GiB NVMe partition mounted at `/var/mnt/llm-models` |

## Access Open WebUI

```bash
kubectl port-forward -n open-webui svc/open-webui 8080:80
```

Then open [http://localhost:8080](http://localhost:8080).

> **Note:** The first time vLLM starts, TT Metal compiles kernels for the model. This takes **30–60+ minutes**. The pod shows `Running` but not `Ready` until compilation finishes. Monitor progress with:
>
> ```bash
> kubectl logs -n <model-namespace> deploy/vllm -f
> ```

## Firmware Upgrades

`tt-k8s-driver-manager` is included in every deployment for on-demand firmware flashing. It does not flash automatically — apply a `TenstorrentFirmwarePolicy` CR when you want to upgrade.

Check the current firmware version:

```bash
kubectl exec -n tt-operator-system ds/tt-telemetry-daemonset -- tt-smi
```

Apply a firmware policy to flash a specific version:

```bash
kubectl apply -f - <<EOF
apiVersion: firmware.tenstorrent.com/v1alpha1
kind: TenstorrentFirmwarePolicy
metadata:
  name: flash-19-11-0
  namespace: tt-operator-system
spec:
  version: "19.11.0"
  nodeAffinity:
    matchLabels:
      feature.node.kubernetes.io/pci-1200_1e52.present: "true"
EOF
```

Watch the flash job, then delete the CR when done:

```bash
kubectl get jobs -n tt-operator-system
kubectl delete tenstorrentfirmwarepolicy -n tt-operator-system flash-19-11-0
```

> The controller cordons the node during the flash. If the CR is deleted mid-flight, uncordon manually: `kubectl uncordon <node-name>`

## Teardown

```bash
omnictl cluster delete ${CLUSTER_NAME}
```
