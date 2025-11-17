# Docker Deployment Guide

This guide covers running Log Simulator in Docker containers for local development, production deployment, and cloud environments.

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop the service
docker-compose down
```

The API will be available at http://localhost:8080

### Using Docker CLI

```bash
# Build the image
docker build -t log-simulator:latest .

# Run the container
docker run -d \
  --name log-simulator \
  -p 8080:8080 \
  log-simulator:latest

# View logs
docker logs -f log-simulator

# Stop and remove
docker stop log-simulator
docker rm log-simulator
```

## Docker Compose Profiles

### Production Mode (Default)

```bash
docker-compose up -d
```

Features:
- Rate limiting enabled
- No auto-reload
- Optimized for performance
- Port: 8080

### Development Mode

```bash
docker-compose --profile dev up api-dev
```

Features:
- Rate limiting disabled
- Auto-reload on code changes
- Debug mode enabled
- Port: 8081

## Configuration

### Environment Variables

Configure the API using environment variables:

```yaml
environment:
  # Server Settings
  - LOG_SIM_HOST=0.0.0.0
  - LOG_SIM_PORT=8080
  - LOG_SIM_DEBUG=false

  # Rate Limiting
  - LOG_SIM_RATE_LIMIT_ENABLED=true
  - LOG_SIM_RATE_LIMIT_DEFAULT=10/minute
  - LOG_SIM_RATE_LIMIT_GENERATE=5/minute

  # Generation Limits
  - LOG_SIM_MAX_LOG_COUNT=10000
  - LOG_SIM_MAX_TIME_SPREAD=86400

  # CORS
  - LOG_SIM_CORS_ORIGINS=["*"]
```

### Using .env File

Create a `.env` file in the project root:

```bash
# .env
LOG_SIM_DEBUG=false
LOG_SIM_RATE_LIMIT_ENABLED=true
LOG_SIM_MAX_LOG_COUNT=50000
```

Then reference it in docker-compose.yml:

```yaml
services:
  api:
    env_file:
      - .env
```

## Volume Mounts

### Data Persistence

The container creates a `/app/data` directory for persistence:

```yaml
volumes:
  - ./data:/app/data
```

### Schema Updates (Development)

Mount schemas directory for live updates:

```yaml
volumes:
  - ./src/log_simulator/schemas:/app/src/log_simulator/schemas:ro
```

### Source Code (Development)

Mount entire source for hot reload:

```yaml
volumes:
  - ./src:/app/src
```

## Health Checks

The container includes a built-in health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1
```

Check health status:

```bash
docker inspect --format='{{.State.Health.Status}}' log-simulator
```

## Building for Production

### Optimized Build

```bash
# Build with specific version tag
docker build -t log-simulator:v0.1.0 .

# Tag for registry
docker tag log-simulator:v0.1.0 your-registry/log-simulator:v0.1.0

# Push to registry
docker push your-registry/log-simulator:v0.1.0
```

### Multi-platform Build

```bash
# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t log-simulator:latest \
  --push \
  .
```

## Cloud Deployment

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/log-simulator

# Deploy to Cloud Run
gcloud run deploy log-simulator \
  --image gcr.io/PROJECT-ID/log-simulator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars LOG_SIM_RATE_LIMIT_ENABLED=true
```

See [cloudrun/README.md](../deployment/cloudrun/README.md) for detailed Cloud Run deployment.

### AWS ECS/Fargate

```bash
# Tag for ECR
docker tag log-simulator:latest AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/log-simulator:latest

# Push to ECR
docker push AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/log-simulator:latest

# Create ECS task definition and service
aws ecs create-service \
  --cluster log-simulator-cluster \
  --service-name log-simulator \
  --task-definition log-simulator:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

### Azure Container Instances

```bash
# Login to Azure Container Registry
az acr login --name yourregistry

# Tag and push
docker tag log-simulator:latest yourregistry.azurecr.io/log-simulator:latest
docker push yourregistry.azurecr.io/log-simulator:latest

# Deploy to ACI
az container create \
  --resource-group log-simulator-rg \
  --name log-simulator \
  --image yourregistry.azurecr.io/log-simulator:latest \
  --dns-name-label log-simulator \
  --ports 8080 \
  --environment-variables \
    LOG_SIM_RATE_LIMIT_ENABLED=true
```

## Docker Compose Examples

### With Custom Port

```yaml
services:
  api:
    ports:
      - "3000:8080"  # External:Internal
```

### With Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### With Restart Policy

```yaml
services:
  api:
    restart: always  # always, unless-stopped, on-failure
```

### Multiple Instances (Load Balancing)

```yaml
services:
  api:
    deploy:
      replicas: 3
    ports:
      - "8080-8082:8080"
```

## Testing the Container

### Verify Health

```bash
# Wait for container to be healthy
docker-compose up -d
sleep 10
curl http://localhost:8080/api/v1/health
```

### Run Tests Inside Container

```bash
# Execute tests in running container
docker exec log-simulator pytest

# Or start a new container for testing
docker run --rm log-simulator:latest pytest
```

### Interactive Shell

```bash
# Access container shell
docker exec -it log-simulator /bin/bash

# Or start with shell
docker run -it --rm log-simulator:latest /bin/bash
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Check container status
docker ps -a

# Inspect container
docker inspect log-simulator
```

### Port Already in Use

```bash
# Find process using port
lsof -ti:8080 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8081:8080"
```

### Permission Denied

```bash
# Ensure data directory is writable
mkdir -p data
chmod 777 data

# Or run as root (not recommended for production)
docker run --user root ...
```

### Memory Issues

```bash
# Increase memory limit
docker run -m 1g log-simulator:latest

# Or in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
```

### Image Size Too Large

```bash
# Check image size
docker images log-simulator

# Analyze image layers
docker history log-simulator:latest

# Use dive for detailed analysis
dive log-simulator:latest
```

## Performance Optimization

### Image Size

Current image: ~200MB (Python 3.12 slim base)

Optimization tips:
- Use `.dockerignore` to exclude unnecessary files
- Multi-stage builds (prepared for frontend)
- Minimize layers
- Use specific base image tags

### Runtime Performance

```yaml
# Use production WSGI server for high load
command: ["gunicorn", "log_simulator.api.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
```

### Caching

```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker build .

# Cache from registry
docker build --cache-from your-registry/log-simulator:latest .
```

## Security Best Practices

✅ **Implemented:**
- Non-root user (logsim:logsim)
- Read-only filesystem for schemas
- No unnecessary packages
- Health checks
- Minimal base image

🔒 **Additional Recommendations:**

```dockerfile
# Run as read-only
docker run --read-only --tmpfs /tmp log-simulator:latest

# Drop capabilities
docker run --cap-drop=ALL log-simulator:latest

# Use security scanning
docker scan log-simulator:latest
```

## Monitoring

### View Logs

```bash
# Follow logs
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api

# Since timestamp
docker-compose logs --since 2025-11-16T10:00:00 api
```

### Resource Usage

```bash
# Real-time stats
docker stats log-simulator

# Export metrics
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

## Next Steps

- See [API Documentation](../docs/API.md) for endpoint reference
- See [Cloud Run Guide](../deployment/cloudrun/README.md) for cloud deployment
- See [Kubernetes Guide](../deployment/kubernetes/README.md) for K8s deployment

## Support

- GitHub Issues: https://github.com/mlucn/log-simulator/issues
- Docker Hub: (coming soon)
