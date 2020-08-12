FROM cebulany-manager-frontend as frontend
FROM cebulany-manager-backend as backend

RUN mkdir -p /app/spa
COPY --from=frontend /app/dist /app/spa/dist
