#!/bin/bash
docker build . -f Dockerfile.backend -t cebulany-manager-backend
docker build . -f Dockerfile.frontend -t cebulany-manager-frontend
docker build . -t cebulany-manager
