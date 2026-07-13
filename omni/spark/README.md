# NVIDIA DGX Spark (GB10) — Omni Cluster Template

Single-node cluster template for a DGX Spark (GB10, 128 GB unified memory). Provisions Talos Linux via [Siderolabs Omni](https://omni.siderolabs.com/) and deploys:

- **vLLM** serving `Qwen/Qwen3.6-35B-A3B-FP8` with model weights on NVMe
- **Open WebUI** — chat interface connected to the model

## Requirements

- Siderolabs Omni account with the machine enrolled
- [`omnictl`](https://omni.siderolabs.com/docs/how-to-guides/how-to-install-and-configure-omnictl/) installed and authenticated
- [`envsubst`](https://www.gnu.org/software/gettext/) (`gettext` package on most systems)
- HuggingFace token with access to [`Qwen/Qwen3.6-35B-A3B-FP8`](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8)

## Deploy

```bash
export MACHINE_UUID=<uuid>    # from Omni UI or: omnictl get machines
export HF_TOKEN=hf_xxx
export CLUSTER_NAME=spark

envsubst '${MACHINE_UUID} ${HF_TOKEN} ${CLUSTER_NAME}' \
  < omni/spark/cluster.yaml > /tmp/spark-cluster.yaml
omnictl cluster template sync --verbose -f /tmp/spark-cluster.yaml
```

The machine UUID is visible in the Omni UI under **Machines**, or via:

```bash
omnictl get machines
```

## Post-Deploy: Install Infrastructure

After the cluster is up, install the NVIDIA GPU Operator and local-path-provisioner:

```bash
# NVIDIA GPU Operator — device plugin, RuntimeClass, feature discovery
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/nvidia-operator

# local-path-provisioner — StorageClass for Open WebUI data
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/local-path-provisioner
```

## Access Open WebUI

```bash
kubectl port-forward -n open-webui svc/open-webui 8080:80
```

Then open [http://localhost:8080](http://localhost:8080).

> **Note:** On first start, vLLM downloads the model weights (~20 GB) to the NVMe partition. The startup probe allows up to 30 minutes for this. Monitor progress with:
>
> ```bash
> kubectl logs -n qwen3-35b deploy/vllm -f
> ```

## What Gets Deployed

| Component | Namespace | Notes |
|---|---|---|
| vLLM | `qwen3-35b` | Model weights on `/var/mnt/vllm-models` (NVMe partition, up to 2 TiB) |
| Open WebUI | `open-webui` | 10 Gi PVC via local-path |

## Talos Configuration

| Setting | Value |
|---|---|
| Talos version | v1.13.6 |
| Kubernetes version | v1.36.2 |
| System extensions | `siderolabs/nonfree-kmod-nvidia`, `siderolabs/nvidia-container-toolkit` |
| Kernel args | `nvidia_drm.modeset=1 iommu=pt arm64.nobti` |
| Control plane scheduling | Enabled (single-node) |
| Install disk | `/dev/nvme0n1` |
| NVMe ephemeral partition | up to 100 GiB |
| NVMe model weight partition | 1–2 TiB (mounted at `/var/mnt/vllm-models`) |

## Re-syncing After Changes

The template uses `mode: one-shot` for all manifests — Omni applies them once at cluster creation and does not reconcile changes. To re-apply after modifying the template, re-sync:

```bash
envsubst '${MACHINE_UUID} ${HF_TOKEN} ${CLUSTER_NAME}' \
  < omni/spark/cluster.yaml > /tmp/spark-cluster.yaml
omnictl cluster template sync --verbose -f /tmp/spark-cluster.yaml
```

## Teardown

```bash
omnictl cluster delete ${CLUSTER_NAME}
```
