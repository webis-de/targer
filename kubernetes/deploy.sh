#!/bin/bash

# Go to project root.
cd ..

# Build Docker images.
docker-compose -p targer_kubernetes build

# Deploy to Kubernetes cluster.
kubectl apply -k kubernetes/
