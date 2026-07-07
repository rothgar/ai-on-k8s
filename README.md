# AI on K8s

Kubernetes manifests for deploying AI workloads — LLM model runners and example applications — using [vLLM](https://github.com/vllm-project/vllm). Designed to be used as a remote source for [Flux](https://fluxcd.io) or [ArgoCD](https://argoproj.github.io/cd/) without modification.

Targets [Talos Linux](https://www.talos.dev/) clusters. Supports NVIDIA, AMD ROCm, Intel Arc, and Tenstorrent accelerators.

## Requirements

- Kubernetes cluster (Talos Linux recommended)
- A hardware accelerator with the appropriate operator or device plugin installed (see [`infrastructure/`](infrastructure/))
- A StorageClass available in the cluster (default assumed: `local-path`)
- A `huggingface-token` Secret in each model's namespace (see [prerequisites](docs/prerequisites.md))

For multi-node models, [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) must also be installed. See [`infrastructure/lws/`](infrastructure/lws/).

## Structure

```
models/          # vLLM model deployments, organized by model then hardware config
apps/            # Example applications (open-webui, litellm, substrate)
infrastructure/  # Hardware operators and cluster prerequisites
docs/            # Setup guides
```

### Hardware prefixes

Model variant directories are named to indicate the hardware they target:

| Prefix | Hardware | Example |
|---|---|---|
| *(none)* | NVIDIA (CUDA) | `4x24gb`, `2-node-8x80gb` |
| `rocm-` | AMD ROCm | `rocm-4x24gb` |
| `intel-` | Intel Arc / Data Center GPU | `intel-2x16gb` |
| `tt-` | Tenstorrent (Wormhole / Blackhole) | `tt-t3k`, `tt-galaxy` |

## Quick Start

Point Flux or ArgoCD at any subdirectory. Every leaf directory is independently deployable:

```bash
# Deploy a single model directly
kubectl apply -k models/qwen3-35b/4x24gb/

# Deploy all example apps
kubectl apply -k apps/
```

See [docs/flux-usage.md](docs/flux-usage.md) and [docs/argocd-usage.md](docs/argocd-usage.md) for GitOps integration examples.

## Model Hardware Requirements

Each model directory contains subdirectories named by hardware topology. Pick the config that matches your available hardware.

### NVIDIA (CUDA)

| Model | Config | Total VRAM | Topology | Notes |
|---|---|---|---|---|
| [Qwen3-4B](models/qwen3-4b/) | `1x8gb` | 8 GB | 1× 8GB+ GPU | |
| [Qwen3-8B](models/qwen3-8b/) | `1x16gb` | 16 GB | 1× 16GB+ GPU | |
| [Qwen3-14B](models/qwen3-14b/) | `1x40gb` | 28 GB | 1× 40GB GPU | FP8 |
| [Qwen3-14B](models/qwen3-14b/) | `2x16gb` | 32 GB | 2× 16GB GPUs | TP=2 |
| [Qwen3-30B-A3B](models/qwen3-30b/) | `1x24gb` | 22 GB | 1× 24GB GPU | MoE, FP8 |
| [Qwen3-30B-A3B](models/qwen3-30b/) | `1x80gb` | 60 GB | 1× 80GB GPU | MoE, FP16 |
| [Qwen3-72B](models/qwen3-72b/) | `2x80gb` | 144 GB | 2× 80GB GPUs | TP=2 |
| [Qwen3-72B](models/qwen3-72b/) | `2-node-4x40gb` | 320 GB | 2 nodes × 4× 40GB | LWS, TP=4 PP=2 |
| [Qwen3-72B](models/qwen3-72b/) | `4-node-2x40gb` | 320 GB | 4 nodes × 2× 40GB | LWS, TP=2 PP=4 |
| [Gemma-4-2B-IT](models/gemma-4-2b-it/) | `1x8gb` | 8 GB | 1× 8GB+ GPU | |
| [Gemma-4-9B-IT](models/gemma-4-9b-it/) | `1x24gb` | 18 GB | 1× 24GB GPU | |
| [Gemma-4-27B-IT](models/gemma-4-27b-it/) | `1x80gb` | 54 GB | 1× 80GB GPU | FP8 |
| [Gemma-4-27B-IT](models/gemma-4-27b-it/) | `2x40gb` | 80 GB | 2× 40GB GPUs | TP=2 |
| [GPT-OSS-120B](models/gpt-oss-120b/) | `1x128gb` | 120 GB | 1× 128GB GPU | mxfp4, GB10/GB200 |
| [GPT-OSS-120B](models/gpt-oss-120b/) | `2-node-2x80gb` | 320 GB | 2 nodes × 2× 80GB | LWS |
| [GPT-OSS-120B](models/gpt-oss-120b/) | `2-node-8x80gb` | 1280 GB | 2 nodes × 8× 80GB | LWS, reference |
| [DeepSeek-V3](models/deepseek-v3/) | `2-node-8x80gb` | 1280 GB | 2 nodes × 8× 80GB | LWS, MoE FP8 |
| [DeepSeek-V3](models/deepseek-v3/) | `4-node-4x80gb` | 1280 GB | 4 nodes × 4× 80GB | LWS, MoE FP8 |
| [DeepSeek-R1](models/deepseek-r1/) | `2-node-8x80gb` | 1280 GB | 2 nodes × 8× 80GB | LWS, MoE FP8 |
| [DeepSeek-R1](models/deepseek-r1/) | `4-node-4x80gb` | 1280 GB | 4 nodes × 4× 80GB | LWS, MoE FP8 |
| [Kimi-K2](models/kimi-k2/) | `2-node-4x80gb` | 640 GB | 2 nodes × 4× 80GB | LWS, MoE |
| [Kimi-K2](models/kimi-k2/) | `4-node-2x80gb` | 640 GB | 4 nodes × 2× 80GB | LWS, MoE |

### AMD ROCm

| Model | Config | Total VRAM | Topology | Notes |
|---|---|---|---|---|
| [Qwen3-8B](models/qwen3-8b/) | `rocm-1x24gb` | 24 GB | 1× 24GB GPU | RX 7900 XTX / MI250 |
| [Qwen3-14B](models/qwen3-14b/) | `rocm-2x24gb` | 48 GB | 2× 24GB GPUs | TP=2 |
| [Qwen3-35B](models/qwen3-35b/) | `rocm-4x24gb` | 96 GB | 4× 24GB GPUs | TP=4, FP8 MoE |
| [Qwen3-72B](models/qwen3-72b/) | `rocm-1x192gb` | 192 GB | 1× 192GB GPU | MI300X |

### Intel Arc

| Model | Config | Total VRAM | Topology | Notes |
|---|---|---|---|---|
| [Qwen3-4B](models/qwen3-4b/) | `intel-1x16gb` | 16 GB | 1× 16GB GPU | Arc A770 / B580 |
| [Qwen3-8B](models/qwen3-8b/) | `intel-2x16gb` | 32 GB | 2× 16GB GPUs | TP=2 |
| [Qwen3-14B](models/qwen3-14b/) | `intel-2x16gb` | 32 GB | 2× 16GB GPUs | TP=2 |

### Tenstorrent

| Model | Config | Device | Topology | Notes |
|---|---|---|---|---|
| [Qwen3-8B](models/qwen3-8b/) | `tt-n150` | N150 | 1× Wormhole B0 | TP=1 |
| [Qwen3-8B](models/qwen3-8b/) | `tt-n300` | N300 | 2× Wormhole B0 | TP=2 |
| [GPT-OSS-120B](models/gpt-oss-120b/) | `tt-galaxy` | Galaxy (T3K) | 8× N300 modules | TP=8, 256 Gi hugepages |

## Infrastructure

| Component | Path | Required for |
|---|---|---|
| NVIDIA GPU Operator | [`infrastructure/nvidia-operator/`](infrastructure/nvidia-operator/) | NVIDIA configs |
| AMD GPU Operator | [`infrastructure/rocm-operator/`](infrastructure/rocm-operator/) | AMD ROCm configs |
| Intel GPU Device Plugin | [`infrastructure/intel-gpu-plugin/`](infrastructure/intel-gpu-plugin/) | Intel Arc configs |
| Tenstorrent Operator | [`infrastructure/tt-operator/`](infrastructure/tt-operator/) | Tenstorrent configs |
| LeaderWorkerSet | [`infrastructure/lws/`](infrastructure/lws/) | All multi-node configs |
| Local Path Provisioner | [`infrastructure/local-path-provisioner/`](infrastructure/local-path-provisioner/) | Optional local storage |

Each infrastructure README includes the Talos Image Factory schematic ID and machine config patch needed for that hardware.

## Example Applications

| App | Path | Description |
|---|---|---|
| Open WebUI | [`apps/open-webui/`](apps/open-webui/) | Chat UI, connects to LiteLLM or vLLM directly |
| LiteLLM | [`apps/litellm/`](apps/litellm/) | OpenAI-compatible LLM gateway and proxy |
| Substrate | [`apps/substrate/`](apps/substrate/) | Actor-based agent orchestration on Kubernetes |

## Overriding StorageClass

All PVCs default to `storageClassName: local-path`. Override without modifying this repo using a Flux/ArgoCD patch:

```yaml
# Flux Kustomization
patches:
  - patch: '{"spec": {"storageClassName": "ceph-filesystem"}}'
    target:
      kind: PersistentVolumeClaim
```
