#!/bin/bash

kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml -n django-todo-app
kubectl apply -f secret.yaml -n django-todo-app
kubectl apply -f deployment.yaml -n django-todo-app
kubectl apply -f service.yaml -n django-todo-app
kubectl apply -f ingress.yaml -n django-todo-app
echo "✅ All Kubernetes resources have been created successfully."