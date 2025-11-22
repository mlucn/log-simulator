# CI/CD Setup Guide - Cloud Build for Cloud Run

This guide explains how to set up automated deployment to Cloud Run using **Cloud Build Triggers**. This approach is secure and uses Workload Identity instead of service account keys.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)

## Overview

### Why Cloud Build Triggers?

✅ **Secure**: Uses Workload Identity - no service account keys needed
✅ **Native Integration**: Built into GCP, seamless with Cloud Run
✅ **Free Tier**: 120 build-minutes per day
✅ **Simple Setup**: Minimal configuration required
✅ **Automated**: Triggers on every push to main branch

### Architecture

```
GitHub Push (main) → Cloud Build Trigger → Build Docker Image →
Push to GCR → Deploy to Cloud Run → Health Check
```

## Prerequisites

Before setting up CI/CD, ensure you have:

1. **GCP Project** with billing enabled
2. **GitHub Repository** with your code
3. **Required APIs** enabled:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```
4. **gcloud CLI** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

## Setup Instructions

### Step 1: Connect GitHub to Cloud Build

1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click **"Connect Repository"**
3. Select **GitHub** as the source
4. Authenticate with GitHub and authorize Cloud Build
5. Select your repository: `mlucn/log-simulator`
6. Click **"Connect"**

### Step 2: Create Build Trigger

**Option A: Using gcloud CLI (Recommended)**

```bash
# Set your project ID
export PROJECT_ID="your-gcp-project-id"

# Create the trigger
gcloud builds triggers create github \
  --name="deploy-log-simulator" \
  --repo-name=log-simulator \
  --repo-owner=mlucn \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --description="Deploy log-simulator to Cloud Run on push to main"
```

**Option B: Using Console**

1. In [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers), click **"Create Trigger"**
2. Configure:
   - **Name**: `deploy-log-simulator`
   - **Event**: Push to a branch
   - **Source**: `mlucn/log-simulator` (select your connected repo)
   - **Branch**: `^main$`
   - **Build Configuration**: Cloud Build configuration file (YAML or JSON)
   - **Location**: `cloudbuild.yaml`
3. Click **"Create"**

### Step 3: Grant Cloud Build Permissions

Cloud Build needs permissions to deploy to Cloud Run:

```bash
# Get the Cloud Build service account
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export CLOUD_BUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/run.admin"

# Grant Service Account User role (to deploy as Cloud Run runtime SA)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/iam.serviceAccountUser"

# Grant Storage Admin role (for Container Registry)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/storage.admin"
```

### Step 4: Verify Setup

Check that your trigger is configured correctly:

```bash
# List all triggers
gcloud builds triggers list

# Describe specific trigger
gcloud builds triggers describe deploy-log-simulator
```

You should see:
- **Trigger Name**: deploy-log-simulator
- **Branch Pattern**: ^main$
- **Build Config**: cloudbuild.yaml
- **Status**: Active

## Configuration

### cloudbuild.yaml Explained

The `cloudbuild.yaml` file defines the build and deployment process:

```yaml
steps:
  # 1. Build Docker image with two tags (commit SHA and latest)
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA', ...]

  # 2. Push commit-specific image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA']

  # 3. Push latest tag
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/log-simulator:latest']

  # 4. Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args: ['run', 'deploy', 'log-simulator', ...]
```

### Default Deployment Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| **Service Name** | `log-simulator` | Cloud Run service name |
| **Region** | `us-central1` | Deployment region |
| **Memory** | `512Mi` | Memory allocation |
| **CPU** | `1` | CPU allocation |
| **Min Instances** | `0` | Scale to zero when idle |
| **Max Instances** | `10` | Maximum concurrent instances |
| **Timeout** | `300s` | Request timeout |
| **Authentication** | Unauthenticated | Public access allowed |
| **Environment Variables** | See below | Runtime configuration |

**Environment Variables:**
- `LOG_SIM_RATE_LIMIT_ENABLED=true` - Enable rate limiting
- `LOG_SIM_MAX_LOG_COUNT=10000` - Maximum logs per request

## Testing

### Test the CI/CD Pipeline

1. **Make a change and push to main**:
   ```bash
   git checkout main
   echo "# Test change" >> README.md
   git add README.md
   git commit -m "test: Trigger CI/CD pipeline"
   git push origin main
   ```

2. **Monitor the build**:
   ```bash
   # Watch builds in real-time
   gcloud builds list --ongoing

   # View specific build logs
   gcloud builds log <BUILD_ID> --stream
   ```

   Or visit [Cloud Build History](https://console.cloud.google.com/cloud-build/builds)

3. **Verify deployment**:
   ```bash
   # Get service URL
   SERVICE_URL=$(gcloud run services describe log-simulator \
     --region us-central1 \
     --format 'value(status.url)')

   echo "Service URL: $SERVICE_URL"

   # Test health endpoint
   curl $SERVICE_URL/api/v1/health

   # Test log generation
   curl $SERVICE_URL/api/v1/generate/google_workspace/admin?count=5
   ```

### Manual Build Trigger

You can manually trigger a build without pushing to GitHub:

```bash
gcloud builds triggers run deploy-log-simulator --branch=main
```

## Monitoring

### Build Status

**Console**: [Cloud Build History](https://console.cloud.google.com/cloud-build/builds)

**CLI**:
```bash
# List recent builds
gcloud builds list --limit=10

# View build details
gcloud builds describe <BUILD_ID>

# Stream build logs
gcloud builds log <BUILD_ID> --stream
```

### Cloud Run Metrics

**Console**: [Cloud Run Services](https://console.cloud.google.com/run)

**CLI**:
```bash
# Get service details
gcloud run services describe log-simulator --region us-central1

# View recent revisions
gcloud run revisions list --service log-simulator --region us-central1

# View logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=log-simulator" \
  --limit 50 \
  --format "table(timestamp,textPayload)"
```

### Set Up Alerts

Create alerts for deployment failures:

```bash
# Create notification channel (email)
gcloud alpha monitoring channels create \
  --display-name="DevOps Team" \
  --type=email \
  --channel-labels=email_address=your-email@example.com

# Create alert policy for failed builds
gcloud alpha monitoring policies create \
  --notification-channels=<CHANNEL_ID> \
  --display-name="Cloud Build Failures" \
  --condition-display-name="Build Failed" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=0s \
  --condition-filter='resource.type="cloud_build" AND metric.type="cloudbuild.googleapis.com/build/count" AND metric.labels.status="FAILURE"'
```

## Troubleshooting

### Common Issues

#### 1. Build Fails with Permission Denied

**Error**: `ERROR: (gcloud.run.deploy) PERMISSION_DENIED`

**Solution**: Ensure Cloud Build service account has required roles:
```bash
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export CLOUD_BUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/iam.serviceAccountUser"
```

#### 2. Trigger Doesn't Fire

**Possible Causes**:
- Branch pattern mismatch (check `^main$` vs `main`)
- Trigger is disabled
- GitHub webhook not configured

**Solution**:
```bash
# Check trigger configuration
gcloud builds triggers describe deploy-log-simulator

# Re-create webhook
gcloud builds triggers update deploy-log-simulator --update-webhooks
```

#### 3. Build Times Out

**Error**: `ERROR: build timeout exceeded`

**Solution**: Increase timeout in `cloudbuild.yaml`:
```yaml
timeout: '2400s'  # Increase from 1200s to 2400s (40 minutes)
```

#### 4. Docker Image Push Fails

**Error**: `denied: Token exchange failed for project`

**Solution**: Grant Storage Admin role:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/storage.admin"
```

#### 5. Cloud Run Deployment Fails

**Error**: `The user-provided container failed to start`

**Debug**:
```bash
# Check Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision" \
  --limit 100 \
  --format "table(timestamp,textPayload)"

# Test Docker image locally
docker pull gcr.io/$PROJECT_ID/log-simulator:latest
docker run -p 8080:8080 gcr.io/$PROJECT_ID/log-simulator:latest
```

### View Build Logs

```bash
# Find recent build ID
BUILD_ID=$(gcloud builds list --limit=1 --format="value(id)")

# View full logs
gcloud builds log $BUILD_ID

# Filter for errors
gcloud builds log $BUILD_ID | grep -i error
```

## Customization

### Change Deployment Region

Edit `cloudbuild.yaml`:
```yaml
args:
  - 'run'
  - 'deploy'
  - 'log-simulator'
  - '--region'
  - 'europe-west1'  # Change from us-central1
```

### Adjust Resource Limits

Edit `cloudbuild.yaml`:
```yaml
args:
  - '--memory'
  - '1Gi'  # Increase memory
  - '--cpu'
  - '2'    # Increase CPU
  - '--max-instances'
  - '50'   # Increase max instances
```

### Add Environment Variables

Edit `cloudbuild.yaml`:
```yaml
args:
  - '--set-env-vars'
  - 'LOG_SIM_RATE_LIMIT_ENABLED=true,LOG_SIM_MAX_LOG_COUNT=50000,NEW_VAR=value'
```

### Deploy to Multiple Environments

Create separate triggers for dev/staging/prod:

```bash
# Development (deploys from 'develop' branch)
gcloud builds triggers create github \
  --name="deploy-log-simulator-dev" \
  --branch-pattern="^develop$" \
  --build-config=cloudbuild.yaml \
  --substitutions=_ENVIRONMENT=dev,_SERVICE_NAME=log-simulator-dev

# Production (deploys from 'main' branch)
gcloud builds triggers create github \
  --name="deploy-log-simulator-prod" \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --substitutions=_ENVIRONMENT=prod,_SERVICE_NAME=log-simulator
```

Then use substitutions in `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE_NAME}'  # Uses substitution variable
      - '--image'
      - 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA'
```

### Enable Approval Gates

For production deployments, add manual approval:

1. Split `cloudbuild.yaml` into build and deploy steps
2. Create separate triggers:
   - Build trigger (runs on all pushes)
   - Deploy trigger (manual only)

**cloudbuild-build.yaml**:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA']
images:
  - 'gcr.io/$PROJECT_ID/log-simulator:$COMMIT_SHA'
```

**cloudbuild-deploy.yaml**:
```yaml
steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args: ['run', 'deploy', 'log-simulator', '--image', 'gcr.io/$PROJECT_ID/log-simulator:${_IMAGE_TAG}']
```

### Rollback to Previous Version

```bash
# List recent revisions
gcloud run revisions list --service log-simulator --region us-central1

# Route all traffic to previous revision
gcloud run services update-traffic log-simulator \
  --region us-central1 \
  --to-revisions log-simulator-00002-xyz=100
```

## Cost Optimization

### Free Tier Limits

**Cloud Build**:
- First 120 build-minutes per day: Free
- After: $0.003 per build-minute

**Cloud Run**:
- 2 million requests per month: Free
- 360,000 GB-seconds memory: Free
- 180,000 vCPU-seconds: Free

### Reduce Build Time

1. **Use Docker layer caching**:
   ```yaml
   options:
     machineType: 'N1_HIGHCPU_8'
     logging: CLOUD_LOGGING_ONLY
     substitution_option: 'ALLOW_LOOSE'
   ```

2. **Optimize Dockerfile**:
   - Use multi-stage builds
   - Order layers from least to most frequently changing
   - Use `.dockerignore` to exclude unnecessary files

3. **Use Artifact Registry** (faster than Container Registry):
   ```bash
   gcloud services enable artifactregistry.googleapis.com

   gcloud artifacts repositories create log-simulator \
     --repository-format=docker \
     --location=us-central1
   ```

   Update `cloudbuild.yaml` to use Artifact Registry:
   ```yaml
   images:
     - 'us-central1-docker.pkg.dev/$PROJECT_ID/log-simulator/log-simulator:$COMMIT_SHA'
   ```

## Security Best Practices

1. **Use Workload Identity** (already configured with Cloud Build)
2. **Scan images for vulnerabilities**:
   ```bash
   gcloud container images scan gcr.io/$PROJECT_ID/log-simulator:latest
   gcloud container images describe gcr.io/$PROJECT_ID/log-simulator:latest --show-package-vulnerability
   ```

3. **Enable Binary Authorization** (require signed images):
   ```bash
   gcloud services enable binaryauthorization.googleapis.com
   ```

4. **Use Secret Manager for sensitive data**:
   ```yaml
   availableSecrets:
     secretManager:
       - versionName: projects/$PROJECT_ID/secrets/api-key/versions/latest
         env: 'API_KEY'
   ```

## Next Steps

1. ✅ Set up Cloud Build trigger
2. ✅ Grant necessary permissions
3. ✅ Test deployment pipeline
4. 🔄 Monitor first production deployment
5. 📊 Set up monitoring and alerts
6. 🔐 Review security settings
7. 💰 Monitor costs and optimize

## Resources

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Triggers](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
- [Cost Optimization](https://cloud.google.com/run/docs/tips/general#optimize-costs)

---

**Questions or Issues?**
- Check the [Troubleshooting](#troubleshooting) section
- Review [Cloud Build Logs](https://console.cloud.google.com/cloud-build/builds)
- Check [Cloud Run Logs](https://console.cloud.google.com/run)
