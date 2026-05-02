# LiteLLM AI Gateway Integration Guide

This guide explains how to configure and use LiteLLM AI Gateway with the Docling Factory application to access remote LLMs from various providers.

## Table of Contents

- [Overview](#overview)
- [What is LiteLLM?](#what-is-litellm)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Supported Providers](#supported-providers)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## Overview

LiteLLM AI Gateway provides a unified interface to access LLMs from multiple providers including:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Azure OpenAI
- Google Vertex AI
- AWS Bedrock
- Local Ollama models
- And 100+ other providers

The Docling Factory application now supports both:
1. **Ollama** - For local LLM deployment
2. **LiteLLM** - For accessing remote LLMs through a unified gateway

## What is LiteLLM?

[LiteLLM](https://github.com/BerriAI/litellm) is an open-source proxy server that:
- Provides a unified API interface for 100+ LLM providers
- Handles authentication, rate limiting, and load balancing
- Supports fallback models and retry logic
- Includes cost tracking and observability
- Enables easy switching between providers without code changes

## Architecture

```
┌─────────────────────┐
│  Docling Factory    │
│  (app_enhanced.py)  │
└──────────┬──────────┘
           │
           ├─────────────────┐
           │                 │
    ┌──────▼──────┐   ┌─────▼──────┐
    │   Ollama    │   │  LiteLLM   │
    │   (Local)   │   │  Gateway   │
    └─────────────┘   └─────┬──────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
         ┌──────▼────┐ ┌───▼────┐ ┌───▼────┐
         │  OpenAI   │ │ Claude │ │ Azure  │
         └───────────┘ └────────┘ └────────┘
```

## Quick Start

### 1. Using Docker Compose

The easiest way to get started is using Docker Compose:

```bash
# Start all services including LiteLLM
docker-compose up -d

# Check LiteLLM logs
docker-compose logs -f litellm

# Access the application
open http://localhost:7860
```

### 2. Configure LiteLLM

Edit `litellm_config.yaml` to add your API keys:

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY  # NEVER hardcode keys
```

Or set environment variables:

```bash
export OPENAI_API_KEY="sk-****-your-actual-key"
export ANTHROPIC_API_KEY="sk-ant-****-your-actual-key"
```

### 3. Use in Application

1. Open the application at http://localhost:7860
2. Go to "Chat with Documents" tab
3. Check "Use LiteLLM AI Gateway"
4. Configure:
   - **LiteLLM API Base URL**: `http://localhost:4000` (or `http://litellm:4000` in Docker)
   - **LLM Model**: `gpt-4` or `claude-3-sonnet`
   - **Embedding Model**: `text-embedding-ada-002`
5. Click "Initialize RAG Engine"
6. Start chatting!

## Configuration

### LiteLLM Configuration File

The `litellm_config.yaml` file controls which models are available:

```yaml
model_list:
  # OpenAI Models
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY  # Never hardcode API keys
  
  # Anthropic Claude
  - model_name: claude-3-sonnet
    litellm_params:
      model: claude-3-sonnet-20240229
      api_key: os.environ/ANTHROPIC_API_KEY  # Never hardcode API keys
  
  # Local Ollama (via LiteLLM)
  - model_name: ollama/llama3.2
    litellm_params:
      model: ollama/llama3.2:latest
      api_base: http://host.docker.internal:11434

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

router_settings:
  routing_strategy: simple-shuffle
  num_retries: 2
  timeout: 600
  fallbacks:
    - gpt-4: ["gpt-3.5-turbo"]
```

### Environment Variables

Set these environment variables for the application:

```bash
# LiteLLM Configuration
LITELLM_API_BASE=http://localhost:4000
LITELLM_API_KEY=sk-****-change-this  # Master key from litellm_config.yaml

# Provider API Keys (for LiteLLM) - NEVER commit real keys
OPENAI_API_KEY=sk-****-your-actual-key
ANTHROPIC_API_KEY=sk-ant-****-your-actual-key
AZURE_API_KEY=****-your-actual-key
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_API_VERSION=2023-05-15
```

## Docker Deployment

### Using Docker Compose

The `docker-compose.yml` includes LiteLLM services:

```yaml
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./litellm_config.yaml:/app/config.yaml
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY:-sk-****-change-this}
      - DATABASE_URL=postgresql://llmproxy:dbpassword9090@litellm-db:5432/litellm
    depends_on:
      - litellm-db

  litellm-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=litellm
      - POSTGRES_USER=llmproxy
      - POSTGRES_PASSWORD=dbpassword9090
```

### Start Services

```bash
# Start all services
docker-compose up -d

# Start only specific services
docker-compose up -d opensearch litellm litellm-db docling-factory-cpu

# View logs
docker-compose logs -f litellm

# Stop services
docker-compose down
```

## Kubernetes Deployment

### Deploy LiteLLM

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy LiteLLM configuration
kubectl apply -f k8s/configmap.yaml

# Deploy LiteLLM services
kubectl apply -f k8s/litellm-deployment.yaml

# Deploy main application
kubectl apply -f k8s/deployment-cpu.yaml
kubectl apply -f k8s/service.yaml
```

### Configure Secrets

Update the secrets in `k8s/litellm-deployment.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: litellm-secrets
  namespace: docling-factory
type: Opaque
stringData:
  master-key: "your-secure-master-key"
  db-password: "your-secure-db-password"
  openai-api-key: "sk-your-openai-key"
  anthropic-api-key: "sk-ant-your-anthropic-key"
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n docling-factory

# Check services
kubectl get svc -n docling-factory

# View logs
kubectl logs -n docling-factory -l app=litellm -f

# Test LiteLLM health
kubectl port-forward -n docling-factory svc/litellm-service 4000:4000
curl http://localhost:4000/health
```

## Supported Providers

### OpenAI

```yaml
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY  # Never hardcode API keys

- model_name: text-embedding-ada-002
  litellm_params:
    model: text-embedding-ada-002
    api_key: os.environ/OPENAI_API_KEY  # Never hardcode API keys
```

### Anthropic Claude

```yaml
- model_name: claude-3-opus
  litellm_params:
    model: claude-3-opus-20240229
    api_key: os.environ/ANTHROPIC_API_KEY  # Never hardcode API keys
```

### Azure OpenAI

```yaml
- model_name: azure-gpt-4
  litellm_params:
    model: azure/gpt-4
    api_key: os.environ/AZURE_API_KEY  # Never hardcode API keys
    api_base: os.environ/AZURE_API_BASE
    api_version: os.environ/AZURE_API_VERSION
```

### Google Vertex AI

```yaml
- model_name: gemini-pro
  litellm_params:
    model: vertex_ai/gemini-pro
    vertex_project: os.environ/VERTEX_PROJECT
    vertex_location: os.environ/VERTEX_LOCATION
```

### AWS Bedrock

```yaml
- model_name: bedrock-claude
  litellm_params:
    model: bedrock/anthropic.claude-v2
    aws_region_name: us-east-1
```

### Local Ollama (via LiteLLM)

```yaml
- model_name: ollama/llama3.2
  litellm_params:
    model: ollama/llama3.2:latest
    api_base: http://host.docker.internal:11434
```

## Usage Examples

### Example 1: Using OpenAI GPT-4

1. Configure in UI:
   - Check "Use LiteLLM AI Gateway"
   - LiteLLM API Base: `http://localhost:4000`
   - LLM Model: `gpt-4`
   - Embedding Model: `text-embedding-ada-002`

2. Initialize RAG Engine

3. Upload and parse documents with "Index for RAG" enabled

4. Ask questions about your documents

### Example 2: Using Claude with Fallback to GPT-3.5

Configure in `litellm_config.yaml`:

```yaml
router_settings:
  fallbacks:
    - claude-3-opus: ["gpt-3.5-turbo"]
```

If Claude fails, requests automatically fall back to GPT-3.5.

### Example 3: Load Balancing Between Providers

```yaml
router_settings:
  routing_strategy: simple-shuffle
  model_group_alias:
    gpt-4-group:
      - gpt-4
      - azure-gpt-4
```

Requests to `gpt-4-group` are distributed between OpenAI and Azure.

## Troubleshooting

### LiteLLM Service Not Starting

```bash
# Check logs
docker-compose logs litellm

# Common issues:
# 1. Invalid config file
# 2. Missing environment variables
# 3. Database connection issues
```

### Authentication Errors

```bash
# Verify API keys are set
docker-compose exec litellm env | grep API_KEY

# Test LiteLLM directly
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Connection Refused

```bash
# Check if LiteLLM is running
docker-compose ps litellm

# Check port mapping
docker-compose port litellm 4000

# Test connectivity
curl http://localhost:4000/health
```

### Model Not Found

```bash
# List available models
curl http://localhost:4000/models \
  -H "Authorization: Bearer sk-1234"

# Verify model is in config
cat litellm_config.yaml | grep model_name
```

### Database Issues

```bash
# Check database logs
docker-compose logs litellm-db

# Connect to database
docker-compose exec litellm-db psql -U llmproxy -d litellm

# Reset database
docker-compose down -v
docker-compose up -d
```

## Advanced Features

### Cost Tracking

LiteLLM automatically tracks costs for all requests:

```bash
# View cost dashboard
open http://localhost:4000/ui
```

### Rate Limiting

Configure in `litellm_config.yaml`:

```yaml
general_settings:
  max_parallel_requests: 100
  max_budget: 100  # USD per month
```

### Caching

Enable caching to reduce costs:

```yaml
general_settings:
  cache: true
  cache_params:
    type: "redis"
    host: "redis"
    port: 6379
```

### Observability

Integrate with Langfuse for detailed observability:

```yaml
general_settings:
  success_callback: ["langfuse"]
```

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
- [Configuration Guide](https://docs.litellm.ai/docs/proxy/configs)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review LiteLLM logs: `docker-compose logs litellm`
3. Consult [LiteLLM documentation](https://docs.litellm.ai/)
4. Open an issue on GitHub

---

**Made with Bob**