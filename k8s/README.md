# Kubernetes Deployment Guide for Docling Factory

This directory contains Kubernetes manifests for deploying Docling Factory on Kubernetes clusters.

## 📋 Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured to access your cluster
- For GPU deployment: NVIDIA GPU Operator installed
- For ingress: NGINX Ingress Controller
- For TLS: cert-manager (optional)
- Persistent storage provisioner

## 📦 Manifests Overview

| File | Description |
|------|-------------|
| `namespace.yaml` | Creates the docling-factory namespace |
| `configmap.yaml` | Application configuration with RAG settings |
| `pvc.yaml` | Persistent Volume Claims for input, output, and logs |
| `deployment-cpu.yaml` | CPU-based deployment (2 replicas) with RAG support |
| `deployment-gpu.yaml` | GPU-based deployment (1 replica with GPU) with RAG support |
| `opensearch-deployment.yaml` | OpenSearch deployment for RAG vector database |
| `service.yaml` | Services for CPU, GPU, and LoadBalancer |
| `ingress.yaml` | Ingress configuration for external access |
| `hpa.yaml` | Horizontal Pod Autoscaler for CPU deployment |

## 🚀 Quick Deployment

### Deploy with RAG Support (Recommended)

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Apply configuration
kubectl apply -f k8s/configmap.yaml

# 3. Deploy OpenSearch for RAG
kubectl apply -f k8s/opensearch-deployment.yaml

# 4. Wait for OpenSearch to be ready
kubectl wait --for=condition=ready pod -l app=opensearch -n docling-factory --timeout=300s

# 5. Deploy storage
kubectl apply -f k8s/pvc.yaml

# 6. Deploy application (CPU version)
kubectl apply -f k8s/deployment-cpu.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# 7. Optional: Apply ingress
kubectl apply -f k8s/ingress.yaml
```

### Deploy CPU Version Only (No RAG)

```bash
# Apply core manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment-cpu.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

### Deploy GPU Version

```bash
# Ensure GPU nodes are available
kubectl get nodes -l accelerator=nvidia-gpu

# Apply GPU deployment
kubectl apply -f k8s/deployment-gpu.yaml
```

### Deploy Everything

```bash
# Deploy all resources at once
kubectl apply -f k8s/
```

## 🔍 Verify Deployment

```bash
# Check namespace
kubectl get namespace docling-factory

# Check pods
kubectl get pods -n docling-factory

# Check services
kubectl get svc -n docling-factory

# Check persistent volumes
kubectl get pvc -n docling-factory

# Check HPA status
kubectl get hpa -n docling-factory

# View logs
kubectl logs -n docling-factory -l app=docling-factory --tail=100
```

## 🌐 Access the Application

### Via LoadBalancer

```bash
# Get external IP
kubectl get svc docling-factory -n docling-factory

# Access at http://<EXTERNAL-IP>
```

### Via Port Forward (Development)

```bash
# Forward port 7860
kubectl port-forward -n docling-factory svc/docling-factory 7860:80

# Access at http://localhost:7860
```

### Via Ingress

1. Update `ingress.yaml` with your domain
2. Apply the ingress manifest
3. Access at https://your-domain.com

## ⚙️ Configuration

### RAG Configuration

The application requires external services for full RAG functionality:

1. **OpenSearch** - Deployed via `opensearch-deployment.yaml`
2. **Ollama** - Must be deployed separately (see below)

#### Deploy Ollama (External)

Ollama should be deployed as a separate service. Update `configmap.yaml` with your Ollama endpoint:

```yaml
OLLAMA_BASE_URL: "http://ollama-service:11434"
```

Example Ollama deployment (create `ollama-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: docling-factory
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: docling-factory
spec:
  ports:
  - port: 11434
    targetPort: 11434
  selector:
    app: ollama
```

### Adjust Resources

Edit `deployment-cpu.yaml` or `deployment-gpu.yaml`:

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Adjust Replicas

```bash
# Scale CPU deployment
kubectl scale deployment docling-factory-cpu -n docling-factory --replicas=5

# Or edit deployment-cpu.yaml and reapply
```

### Update ConfigMap

Edit `configmap.yaml` and reapply:

```bash
kubectl apply -f k8s/configmap.yaml

# Restart pods to pick up changes
kubectl rollout restart deployment/docling-factory-cpu -n docling-factory
```

## 💾 Storage Configuration

### Adjust Storage Sizes

Edit `pvc.yaml`:

```yaml
resources:
  requests:
    storage: 50Gi  # Adjust as needed
```

### Use Different Storage Class

```yaml
storageClassName: fast-ssd  # Your storage class
```

## 🔐 Security

### Network Policies

Create network policies to restrict traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: docling-factory-netpol
  namespace: docling-factory
spec:
  podSelector:
    matchLabels:
      app: docling-factory
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 7860
```

### Resource Quotas

Set namespace resource quotas:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: docling-factory-quota
  namespace: docling-factory
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    persistentvolumeclaims: "10"
```

## 📊 Monitoring

### Check Pod Status

```bash
# Watch pods
kubectl get pods -n docling-factory -w

# Describe pod
kubectl describe pod <pod-name> -n docling-factory

# View events
kubectl get events -n docling-factory --sort-by='.lastTimestamp'
```

### View Metrics

```bash
# Pod metrics (requires metrics-server)
kubectl top pods -n docling-factory

# Node metrics
kubectl top nodes
```

## 🔄 Updates and Rollbacks

### Update Image

```bash
# Update CPU deployment
kubectl set image deployment/docling-factory-cpu \
  docling-factory=docling-factory:cpu-v2.0 \
  -n docling-factory

# Check rollout status
kubectl rollout status deployment/docling-factory-cpu -n docling-factory
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/docling-factory-cpu -n docling-factory

# Rollback to specific revision
kubectl rollout undo deployment/docling-factory-cpu --to-revision=2 -n docling-factory
```

## 🧹 Cleanup

### Remove All Resources

```bash
# Delete namespace (removes everything)
kubectl delete namespace docling-factory

# Or delete individual resources
kubectl delete -f k8s/
```

### Keep PVCs

```bash
# Delete everything except PVCs
kubectl delete deployment,service,ingress,hpa,configmap -n docling-factory --all
```

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n docling-factory

# Check logs
kubectl logs <pod-name> -n docling-factory

# Check previous logs if pod restarted
kubectl logs <pod-name> -n docling-factory --previous
```

### PVC Not Binding

```bash
# Check PVC status
kubectl get pvc -n docling-factory

# Describe PVC
kubectl describe pvc <pvc-name> -n docling-factory

# Check available storage classes
kubectl get storageclass
```

### GPU Not Available

```bash
# Check GPU nodes
kubectl get nodes -l accelerator=nvidia-gpu

# Check GPU operator
kubectl get pods -n gpu-operator-resources

# Describe GPU pod
kubectl describe pod <gpu-pod-name> -n docling-factory
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager](https://cert-manager.io/docs/)

## 🔗 Related Files

- [Main README](../README.md)
- [Docker Compose](../docker-compose.yml)
- [Dockerfile](../Dockerfile)
- [Dockerfile GPU](../Dockerfile.gpu)
- [RAG Usage Guide](../RAG_USAGE_GUIDE.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)

## 🆕 RAG Features

The Kubernetes deployment now includes full RAG (Retrieval-Augmented Generation) support:

- **OpenSearch** for vector storage and semantic search
- **Ollama** integration for local LLM and embeddings
- **OpenLLMetry** for observability and metrics
- **Chat with Documents** functionality
- **Real-time metrics dashboard**

### RAG Architecture in Kubernetes

```
┌─────────────────┐
│   Ingress       │
└────────┬────────┘
         │
┌────────▼────────┐
│  LoadBalancer   │
└────────┬────────┘
         │
    ┌────▼─────┬──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼───┐
│ Pod 1 │  │ Pod 2│  │ Pod N│  (Docling Factory)
└───┬───┘  └──┬───┘  └──┬───┘
    │         │         │
    └─────────┼─────────┘
              │
    ┌─────────▼──────────┐
    │                    │
┌───▼────────┐  ┌───────▼────┐
│ OpenSearch │  │   Ollama   │
│  Service   │  │  Service   │
└────────────┘  └────────────┘
```

### Environment Variables for RAG

The following environment variables are configured in `configmap.yaml`:

- `OPENSEARCH_HOST`: OpenSearch service hostname
- `OPENSEARCH_PORT`: OpenSearch port (default: 9200)
- `OLLAMA_BASE_URL`: Ollama service URL

### Scaling Considerations

- **OpenSearch**: Single replica for development, consider clustering for production
- **Ollama**: Resource-intensive, allocate sufficient CPU/memory
- **Docling Factory**: Can scale horizontally with HPA

# Made with Bob