# Deploy to Google Cloud Run

This guide will help you deploy the Log Simulator API to Google Cloud Run.

## Prerequisites

- Google Cloud Platform account
- A GCP project with billing enabled
- Permissions to deploy to Cloud Run

## Quick Start

### Step 1: Install gcloud CLI

```bash
./scripts/install-gcloud.sh
```

Or manually:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Step 2: Initialize gcloud

```bash
gcloud init
```

This will:
- Authenticate you with Google Cloud
- Let you select or create a project
- Set your default region

### Step 3: Deploy

```bash
./scripts/deploy-cloudrun.sh
```

This will:
- Enable required APIs (Cloud Build, Cloud Run, Artifact Registry)
- Build your Docker image using Cloud Build
- Deploy to Cloud Run
- Output the service URL

## Manual Deployment

If you prefer to deploy manually:

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Deploy from source
gcloud run deploy log-simulator \
  --source . \
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

## Configuration Options

Customize deployment with environment variables:

```bash
# Change region
export CLOUD_RUN_REGION=us-east1

# Increase memory
export CLOUD_RUN_MEMORY=1Gi

# Set min instances (keep warm)
export CLOUD_RUN_MIN_INSTANCES=1

# Then deploy
./scripts/deploy-cloudrun.sh
```

Available options:
- `CLOUD_RUN_REGION` - Deployment region (default: us-central1)
- `CLOUD_RUN_MEMORY` - Memory allocation (default: 512Mi)
- `CLOUD_RUN_CPU` - CPU allocation (default: 1)
- `CLOUD_RUN_MIN_INSTANCES` - Minimum instances (default: 0)
- `CLOUD_RUN_MAX_INSTANCES` - Maximum instances (default: 10)
- `CLOUD_RUN_TIMEOUT` - Request timeout in seconds (default: 300)

## Testing Your Deployment

Once deployed, you'll get a URL like: `https://log-simulator-xxxxx-uc.a.run.app`

### Test the health endpoint:
```bash
curl https://YOUR-SERVICE-URL/api/v1/health
```

### View API documentation:
```
https://YOUR-SERVICE-URL/api/v1/docs
```

### Generate logs:
```bash
curl -X POST https://YOUR-SERVICE-URL/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "cloud_identity/google_workspace",
    "count": 5,
    "scenario": "user_login_success"
  }'
```

## Managing Your Deployment

### View service details:
```bash
gcloud run services describe log-simulator --region us-central1
```

### View logs:
```bash
gcloud run services logs read log-simulator --region us-central1
```

### Update environment variables:
```bash
gcloud run services update log-simulator \
  --region us-central1 \
  --set-env-vars LOG_SIM_MAX_LOG_COUNT=50000
```

### Scale up/down:
```bash
# Set min instances to 1 (keep warm)
gcloud run services update log-simulator \
  --region us-central1 \
  --min-instances 1

# Set max instances
gcloud run services update log-simulator \
  --region us-central1 \
  --max-instances 20
```

### Delete service:
```bash
gcloud run services delete log-simulator --region us-central1
```

## Cost Optimization

Cloud Run pricing is based on:
- **CPU and Memory**: Billed per 100ms of usage
- **Requests**: First 2 million requests/month are free
- **Networking**: Egress charges may apply

### Free Tier
- 2 million requests/month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

### Tips to minimize costs:
1. Set `min-instances` to 0 (scales to zero when not in use)
2. Use the smallest memory that works (512Mi is fine for most cases)
3. Enable request timeout to prevent long-running requests
4. Use rate limiting to prevent abuse

## Continuous Deployment

### Option 1: GitHub Actions

Create `.github/workflows/deploy-cloudrun.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: log-simulator
          region: us-central1
          source: .
```

### Option 2: Cloud Build Triggers

Set up automatic deployments on git push:

```bash
gcloud builds triggers create github \
  --repo-name=log-simulator \
  --repo-owner=mlucn \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml
```

## Troubleshooting

### Build fails
- Check Cloud Build logs: `gcloud builds list --limit 5`
- Ensure Dockerfile is valid: `docker build -t test .`

### Service won't start
- Check logs: `gcloud run services logs read log-simulator --region us-central1`
- Verify port 8080 is exposed in Dockerfile
- Check health endpoint is accessible

### 502 Bad Gateway
- Service might be taking too long to start
- Increase timeout or memory allocation
- Check application logs for errors

### Permission denied
- Ensure billing is enabled on your project
- Check IAM permissions (need Cloud Run Admin role)
- Enable required APIs

## Security

The current deployment allows **unauthenticated** access. For production:

### Option 1: Require authentication
```bash
gcloud run services update log-simulator \
  --region us-central1 \
  --no-allow-unauthenticated
```

Then use:
```bash
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://YOUR-SERVICE-URL/api/v1/health
```

### Option 2: Use API Gateway
- Set up Cloud Endpoints or API Gateway
- Add API key authentication
- Implement rate limiting at the gateway level

## Support

- Cloud Run docs: https://cloud.google.com/run/docs
- Pricing: https://cloud.google.com/run/pricing
- Quotas: https://cloud.google.com/run/quotas
