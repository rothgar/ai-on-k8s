# LeaderWorkerSet (LWS)

Installs the [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) controller, which is required for all multi-node model deployments in this repository. LWS manages groups of pods that work together as a single distributed inference unit.

If you only intend to deploy single-node models (e.g., `qwen3-35b/4x24gb`, `gemma-4-27b-it/1x80gb`), you do not need LWS.

## What this installs

- LeaderWorkerSet CRD
- LWS controller in the `lws-system` namespace

## Deploy

```bash
kubectl apply -k https://github.com/siderolabs/ai-on-k8s//infrastructure/lws
```

Or from a local clone:

```bash
kubectl apply -k infrastructure/lws/
```

## Flux

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: lws
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: ai-on-k8s
  path: ./infrastructure/lws
  prune: true
  timeout: 5m
```

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: lws
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/siderolabs/ai-on-k8s
    targetRevision: main
    path: infrastructure/lws
  destination:
    server: https://kubernetes.default.svc
    namespace: lws-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Verify

```bash
kubectl get crd leaderworkersets.leaderworkerset.x-k8s.io
kubectl get pods -n lws-system
```

## Models that require LWS

Any model variant directory prefixed with a node count (e.g., `2-node-8x80gb`, `4-node-4x80gb`) uses LWS. Single-node variants (e.g., `4x24gb`, `2x80gb`) do not.
