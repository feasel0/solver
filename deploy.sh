#!/bin/bash
set -euo pipefail

# run from repo root
cd "$(dirname "$0")"

echo "==> Pulling latest code from GitHub..."
git fetch origin main
git reset --hard origin/main

echo "==> Pulling base images (security updates)..."
docker compose pull || true

echo "==> Rebuilding containers (fresh layers)..."
docker compose build --pull

echo "==> Restarting containers..."
docker compose up -d --remove-orphans

echo "==> Pruning unused Docker images/containers/build cache..."
docker system prune -af

echo "==> Pruning UNUSED Docker volumes..."
# only removes volumes not attached to any container
docker volume prune -f

echo "==> Docker disk usage after prune:"
docker system df

echo "==> Deployment complete!"
