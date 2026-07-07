# Models

Each model directory contains one or more variant subdirectories named `{count}x{vram}gb` for single-node configs or `{nodes}-node-{count}x{vram}gb` for multi-node LeaderWorkerSet configs. The name tells you exactly what GPU hardware each configuration requires.

## Single-Node Models

| Directory | Variant | VRAM Required | Topology |
|---|---|---|---|
| `qwen3-4b/` | `1x8gb` | 8 GB | 1 GPU |
| `qwen3-8b/` | `1x16gb` | 16 GB | 1 GPU |
| `qwen3-14b/` | `1x40gb` | 28 GB | 1 GPU, FP8 |
| `qwen3-14b/` | `2x16gb` | 32 GB | 2 GPUs, TP=2 |
| `qwen3-30b/` | `1x24gb` | 22 GB | 1 GPU, MoE FP8 |
| `qwen3-30b/` | `1x80gb` | 60 GB | 1 GPU, MoE FP16 |
| `gemma-4-2b-it/` | `1x8gb` | 8 GB | 1 GPU |
| `gemma-4-9b-it/` | `1x24gb` | 18 GB | 1 GPU |
| `gemma-4-27b-it/` | `1x80gb` | 54 GB | 1 GPU, FP8 |
| `gemma-4-27b-it/` | `2x40gb` | 80 GB | 2 GPUs, TP=2 |
| `gpt-oss-120b/` | `1x128gb` | 120 GB | 1 GPU, mxfp4 (GB10/GB200) |

## Multi-Node Models (require LeaderWorkerSet)

| Directory | Variant | VRAM Required | Topology |
|---|---|---|---|
| `qwen3-72b/` | `2x80gb` | 144 GB | 2 GPUs, TP=2 |
| `qwen3-72b/` | `2-node-4x40gb` | 320 GB | 2 nodes × 4 GPUs |
| `qwen3-72b/` | `4-node-2x40gb` | 320 GB | 4 nodes × 2 GPUs |
| `gpt-oss-120b/` | `2-node-2x80gb` | 320 GB | 2 nodes × 2 GPUs |
| `gpt-oss-120b/` | `2-node-8x80gb` | 1280 GB | 2 nodes × 8 GPUs |
| `deepseek-v3/` | `2-node-8x80gb` | 1280 GB | 2 nodes × 8 GPUs |
| `deepseek-v3/` | `4-node-4x80gb` | 1280 GB | 4 nodes × 4 GPUs |
| `deepseek-r1/` | `2-node-8x80gb` | 1280 GB | 2 nodes × 8 GPUs |
| `deepseek-r1/` | `4-node-4x80gb` | 1280 GB | 4 nodes × 4 GPUs |
| `kimi-k2/` | `2-node-4x80gb` | 640 GB | 2 nodes × 4 GPUs |
| `kimi-k2/` | `4-node-2x80gb` | 640 GB | 4 nodes × 2 GPUs |

## All Models use vLLM

All deployments use [vLLM](https://github.com/vllm-project/vllm) serving an OpenAI-compatible API on port 8000. Connect any OpenAI-compatible client to `http://<service>.<namespace>.svc.cluster.local:8000/v1`.

## Common Patches

Override StorageClass:
```bash
kubectl apply -k models/qwen3-4b/1x8gb/ \
  --patch='[{"op":"replace","path":"/spec/storageClassName","value":"my-sc"}]'
```

Or use Flux/ArgoCD source patches — see [../docs/flux-usage.md](../docs/flux-usage.md).
