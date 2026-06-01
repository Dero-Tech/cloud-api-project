#!/bin/bash
set -e

# Update system packages
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker

# Pull and run the app container from GitHub Container Registry
docker pull ghcr.io/${github_username}/cloud-api:latest

docker run -d \
  --name cloud-api \
  --restart always \
  -p 5000:5000 \
  -e APP_ENV=${app_env} \
  ghcr.io/${github_username}/cloud-api:latest
