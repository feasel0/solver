#!/bin/bash
set -e

echo "Pulling latest code from GitHub..."
git fetch origin main
git reset --hard origin/main

echo "Rebuilding containers..."
docker compose build --no-cache

echo "Restarting containers..."
docker compose up -d

echo "Deployment complete!"
