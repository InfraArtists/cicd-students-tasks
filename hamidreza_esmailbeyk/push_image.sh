#!/bin/bash

# ===============================
# Settings
# ===============================
USERNAME="hamidesmb"       # Dockerhub Username
REPO="todo_app"          # Repo Name
TAG="latest"               # Image Tag
IMAGE="$USERNAME/$REPO:$TAG"
PASSWORD="hamidesmb2025"   # Dockerhub Password


docker image tag $REPO $USERNAME/$REPO:$TAG
echo ""
TOKEN=$(curl -s -H "Content-Type: application/json" \
  -X POST -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ Login failed! Check your username/password."
  exit 1
fi

REPO_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: JWT $TOKEN" \
  https://hub.docker.com/v2/repositories/$USERNAME/$REPO/)

if [ "$REPO_EXISTS" -eq 200 ]; then
  echo "✅ Repository '$USERNAME/$REPO' already exists."
else
  echo "⚙️  Repository not found. Creating it as PRIVATE..."
  CREATE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: JWT $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$REPO\", \"is_private\": true}" \
    https://hub.docker.com/v2/repositories/$USERNAME/)

  if [ "$CREATE_STATUS" -eq 201 ]; then
    echo "✅ Repository '$USERNAME/$REPO' created as private."
  else
    echo "❌ Failed to create repository. HTTP $CREATE_STATUS"
    exit 1
  fi
fi

echo "📦 Pushing image: $IMAGE ..."
echo $PASSWORD | docker login -u $USERNAME --password-stdin
docker push $IMAGE

if [ $? -eq 0 ]; then
  echo "✅ Image pushed successfully!"
else
  echo "❌ Failed to push image."
fi
