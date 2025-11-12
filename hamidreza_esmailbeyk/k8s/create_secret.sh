#!/bin/bash

username="hamidesmb"
password="hamidesmb2025"
email="hamid.esmb@yahoo.com"

kubectl create secret docker-registry todo-app-secret   --docker-server=https://index.docker.io/v1/   --docker-username=$username   --docker-password=$password   --docker-email=$email  --dry-run=client -o yaml > secret.yaml
