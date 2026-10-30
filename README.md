# 🐳 Docker – Cheat Sheet

Containerised applications and images I build and ship to **Amazon ECR** and run on **ECS Fargate**.

## What's in this repo
| Path | Purpose |
|---|---|
| `app-name/Dockerfile` | Multi-stage build for each app |
| `app-name/.dockerignore` | Keeps images small and secrets out |
| `docker-compose.yml` | Local multi-container development |

## Everyday commands
```bash
docker build -t app:1.0.0 .                 # build an image
docker run -d -p 8080:8080 --name app app:1.0.0
docker logs -f app                          # follow logs
docker exec -it app sh                      # shell into a container
docker ps -a / docker images                # list containers / images
docker system prune -f                      # clean unused data
docker compose up -d --build                # start local stack
```

## Push to Amazon ECR
```bash
aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker tag app:1.0.0 <account-id>.dkr.ecr.<region>.amazonaws.com/app:1.0.0
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/app:1.0.0
```

## Best practices
- Use **multi-stage builds** so build tools never reach the final image
- Pin base image versions (never `latest`) and prefer slim or alpine variants
- Run as a **non-root user**
- Maintain a `.dockerignore` (`.git`, `node_modules`, `.env`, etc.)
- Order layers from least to most frequently changing to use the build cache
- Never bake secrets into images; use AWS Secrets Manager or environment injection
- Add a `HEALTHCHECK` and one process per container
- Tag images with version or commit SHA; scan before pushing (`trivy image app:1.0.0`)

## Example: multi-stage Dockerfile (Node)
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
USER node
EXPOSE 8080
HEALTHCHECK CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["node", "dist/index.js"]
```
