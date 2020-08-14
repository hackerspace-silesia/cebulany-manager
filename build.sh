#!/bin/bash
docker build . -f Dockerfile.backend -t cebulany-manager-backend
docker build . -f Dockerfile.frontend -t cebulany-manager-frontend --build-arg URL_PREFIX=${URL_PREFIX:-}
docker build . -t cebulany-manager
