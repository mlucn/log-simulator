# CI/CD Setup for Cloud Run Auto-Deployment

This guide shows you how to set up automatic deployment to Google Cloud Run whenever you push to the `main` branch.

## Choose Your Approach

### Option 1: Cloud Build Triggers (Recommended ⭐)

**Pros:**
- Native GCP integration
- Simpler setup (no GitHub secrets needed)
- Free tier: 120 build-minutes/day
- Automatic access to your GCP project

**Setup Steps:**

#### 1. Connect GitHub to Cloud Build

```bash
# Open Cloud Build in GCP Console
open https://console.cloud.google.com/cloud-build/triggers

# Or via CLI
gcloud builds triggers create github \
  --repo-name=log-simulator \
  --repo-owner=mlucn \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml \
  --description="Auto-deploy log-simulator on push to main"
```

**Via Console:**
1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click **"Connect Repository"**
3. Select **GitHub** → Authenticate
4. Choose **mlucn/log-simulator**
5. Create trigger:
   - **Name**: `deploy-log-simulator`
   - **Event**: Push to branch
   - **Branch**: `^main$`
   - **Configuration**: Cloud Build configuration file
   - **Location**: `/cloudbuild.yaml`
6. Click **"Create"**

#### 2. Grant Cloud Build Permissions

```bash
# Get Cloud Build service account
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/run.admin"

# Grant Service Account User role (needed to deploy as service account)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/iam.serviceAccountUser"
```

#### 3. Test It!

```bash
# Make a change and push to main
git checkout main
echo "# CI/CD Test" >> README.md
git add README.md
git commit -m "test: Trigger Cloud Build deployment"
git push origin main

# Watch the build
gcloud builds list --limit 1
gcloud builds log $(gcloud builds list --limit 1 --format="value(id)")
```

✅ **Done!** Every push to `main` will now auto-deploy to Cloud Run.

---

### Option 2: GitHub Actions

**Pros:**
- More familiar if you use GitHub Actions
- More control and flexibility
- Can add additional steps (tests, notifications, etc.)
- Runs alongside your existing test workflow

**Setup Steps:**

#### 1. Create GCP Service Account

```bash
# Set your project
PROJECT_ID=$(gcloud config get-value project)

# Create service account for GitHub Actions
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployment"

# Grant necessary roles
SERVICE_ACCOUNT="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create github-actions-key.json \
  --iam-account=${SERVICE_ACCOUNT}

echo "✅ Key created: github-actions-key.json"
echo "⚠️  Keep this file secure! You'll need it in the next step."
```

#### 2. Add GitHub Secrets

Go to your GitHub repository:

```
https://github.com/mlucn/log-simulator/settings/secrets/actions
```

Add these secrets:

1. **`GCP_PROJECT_ID`**
   - Value: Your GCP project ID (e.g., `my-project-123`)
   - Get it: `gcloud config get-value project`

2. **`GCP_SA_KEY`**
   - Value: Contents of `github-actions-key.json`
   - Get it: `cat github-actions-key.json`
   - Copy the **entire JSON** (including `{` and `}`)

**Security:** After adding to GitHub, delete the local key file:
```bash
rm github-actions-key.json
```

#### 3. Test It!

```bash
# Push to main branch
git checkout main
git pull
git push origin main

# Or manually trigger via GitHub UI:
# Go to Actions → Deploy to Cloud Run → Run workflow
```

✅ **Done!** Every push to `main` will now:
1. Run all tests
2. If tests pass → Deploy to Cloud Run
3. Run health check to verify deployment

---

## Verify Deployment

After setup, verify it's working:

### Check Build Logs

**Cloud Build:**
```bash
gcloud builds list --limit 5
gcloud builds log <BUILD_ID>
```

**GitHub Actions:**
```
https://github.com/mlucn/log-simulator/actions
```

### Check Deployment

```bash
# Get service URL
gcloud run services describe log-simulator \
  --region us-central1 \
  --format='value(status.url)'

# Test health endpoint
SERVICE_URL=$(gcloud run services describe log-simulator --region us-central1 --format='value(status.url)')
curl $SERVICE_URL/api/v1/health

# Test new Google Workspace schemas
curl $SERVICE_URL/api/v1/schemas | jq '.schemas.cloud_identity[] | select(contains("google_workspace"))'
```

---

## Customization

### Change Deployment Region

**Cloud Build (`cloudbuild.yaml`):**
```yaml
# Line 41: Change region
- '--region'
- 'us-east1'  # Change this
```

**GitHub Actions (`.github/workflows/deploy-cloudrun.yml`):**
```yaml
# Line 12: Change region
env:
  REGION: us-east1  # Change this
```

### Increase Memory/CPU

**Cloud Build (`cloudbuild.yaml`):**
```yaml
# Lines 46-49
- '--memory'
- '1Gi'  # Increase from 512Mi
- '--cpu'
- '2'    # Increase from 1
```

**GitHub Actions (`.github/workflows/deploy-cloudrun.yml`):**
```yaml
# Lines 87-88
--memory=1Gi
--cpu=2
```

### Add Staging Environment

Create a separate trigger/workflow for a `staging` branch:

**Cloud Build:** Create another trigger with:
- Branch: `^staging$`
- Service name: `log-simulator-staging`

**GitHub Actions:** Duplicate workflow and modify:
```yaml
on:
  push:
    branches: [ staging ]
# ...
  SERVICE_NAME: log-simulator-staging
```

---

## Monitoring

### View Deployment History

**Cloud Build:**
```bash
gcloud builds list --limit 10
```

**GitHub Actions:**
```bash
gh run list --workflow="Deploy to Cloud Run" --limit 10
```

### View Service Logs

```bash
# Real-time logs
gcloud run services logs tail log-simulator --region us-central1

# Recent logs
gcloud run services logs read log-simulator --region us-central1 --limit 100
```

### Setup Alerts

```bash
# Alert on failed deployments
gcloud alpha monitoring policies create \
  --notification-channels=<CHANNEL_ID> \
  --display-name="Failed Cloud Run Deployments" \
  --condition-display-name="Build Failed" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=60s
```

---

## Rollback

If a deployment fails:

**Quick rollback to previous version:**
```bash
# List revisions
gcloud run revisions list --service log-simulator --region us-central1

# Rollback to specific revision
gcloud run services update-traffic log-simulator \
  --region us-central1 \
  --to-revisions=<REVISION_NAME>=100
```

**Via Console:**
1. Go to [Cloud Run](https://console.cloud.google.com/run)
2. Click **log-simulator**
3. Go to **"Revisions"** tab
4. Click **"Manage Traffic"**
5. Route 100% traffic to previous working revision

---

## Cost Optimization

Both options use similar resources:

**Cloud Build:**
- Free: 120 build-minutes/day
- After: $0.003/build-minute
- Typical build: 3-5 minutes = $0.01-0.015

**GitHub Actions:**
- Free: 2,000 minutes/month (public repos)
- Free: 500 MB storage
- Typical workflow: 5 minutes

**Cloud Run:**
- Same cost regardless of deployment method
- Free tier: 2M requests/month
- Estimated: $0-5/month for light usage

---

## Troubleshooting

### Cloud Build: Permission Denied

```bash
# Re-grant permissions
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/run.admin"
```

### GitHub Actions: Invalid Credentials

1. Regenerate service account key:
   ```bash
   gcloud iam service-accounts keys create new-key.json \
     --iam-account=github-actions@${PROJECT_ID}.iam.gserviceaccount.com
   ```

2. Update `GCP_SA_KEY` secret in GitHub

### Build Succeeds but Deployment Fails

Check logs:
```bash
gcloud run services logs read log-simulator --region us-central1 --limit 50
```

Common issues:
- Port not exposed (should be 8080)
- Health check failing
- Environment variables missing

---

## Next Steps

After setup:

1. ✅ Test a deployment
2. ✅ Set up staging environment (optional)
3. ✅ Configure monitoring/alerts
4. ✅ Document your team's workflow

## Support

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
