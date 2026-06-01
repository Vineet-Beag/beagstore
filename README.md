# AI-Powered Kubernetes Observability Assistant

An AI-powered Retrieval-Augmented Generation (RAG) platform built for Kubernetes and SRE troubleshooting.

## Features

- Streamlit Chat Interface
- PDF Knowledge Upload
- FastAPI Backend
- PostgreSQL + pgvector Vector Database
- Ollama + Mistral LLM
- Semantic Search Retrieval
- Kubernetes Deployment
- Prometheus Metrics
- Grafana Monitoring


## Architecture

![Architecture](docs/architecture.png)

User
↓
Streamlit UI
↓
FastAPI
↓
Sentence Transformers
↓
PostgreSQL + pgvector
↓
Ollama (Mistral)

## Technology Stack

- Python
- FastAPI
- Streamlit
- PostgreSQL
- pgvector
- Kubernetes
- Docker
- Prometheus
- Grafana
- OCI
- Ollama
- Mistral

## Use Cases

- Kubernetes Troubleshooting
- SRE Knowledge Assistant
- Runbook Search
- Incident RCA Search
- Operational Documentation Assistant
