#!/bin/bash
# Deploy Log Simulator to Google Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Log Simulator to Google Cloud Run${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed${NC}"
    echo "Please run: ./scripts/install-gcloud.sh"
    exit 1
fi

# Configuration
SERVICE_NAME="log-simulator"
REGION="${CLOUD_RUN_REGION:-us-central1}"
MEMORY="${CLOUD_RUN_MEMORY:-512Mi}"
CPU="${CLOUD_RUN_CPU:-1}"
MIN_INSTANCES="${CLOUD_RUN_MIN_INSTANCES:-0}"
MAX_INSTANCES="${CLOUD_RUN_MAX_INSTANCES:-10}"
TIMEOUT="${CLOUD_RUN_TIMEOUT:-300}"

echo "Configuration:"
echo "  Service:       ${SERVICE_NAME}"
echo "  Region:        ${REGION}"
echo "  Memory:        ${MEMORY}"
echo "  CPU:           ${CPU}"
echo "  Min Instances: ${MIN_INSTANCES}"
echo "  Max Instances: ${MAX_INSTANCES}"
echo "  Timeout:       ${TIMEOUT}s"
echo ""

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No GCP project set${NC}"
    echo "Please run: gcloud init"
    exit 1
fi

echo -e "${GREEN}📦 GCP Project: ${PROJECT_ID}${NC}"
echo ""

# Confirm deployment
read -p "Deploy to Cloud Run? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo -e "${YELLOW}⚙️  Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable artifactregistry.googleapis.com --quiet

echo ""
echo -e "${YELLOW}🔨 Building and deploying to Cloud Run...${NC}"
echo "This will take a few minutes..."
echo ""

# Deploy to Cloud Run from source
gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8080 \
  --memory ${MEMORY} \
  --cpu ${CPU} \
  --min-instances ${MIN_INSTANCES} \
  --max-instances ${MAX_INSTANCES} \
  --timeout ${TIMEOUT} \
  --set-env-vars LOG_SIM_RATE_LIMIT_ENABLED=true \
  --set-env-vars LOG_SIM_MAX_LOG_COUNT=10000 \
  --quiet

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --region ${REGION} \
  --format 'value(status.url)' 2>/dev/null)

if [ -n "$SERVICE_URL" ]; then
    echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
    echo ""
    echo "Test endpoints:"
    echo "  Health:  ${SERVICE_URL}/api/v1/health"
    echo "  Docs:    ${SERVICE_URL}/api/v1/docs"
    echo "  Schemas: ${SERVICE_URL}/api/v1/schemas"
    echo ""
    echo "Test with curl:"
    echo "  curl ${SERVICE_URL}/api/v1/health"
fi

echo ""
echo -e "${GREEN}🎉 Deployment successful!${NC}"
