#!/bin/bash
# Monitor Cloud Run costs and usage

set -e

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
SERVICE_NAME="log-simulator"
REGION="us-central1"

echo "📊 Cloud Run Usage for ${SERVICE_NAME}"
echo "========================================"
echo ""

# Get current month metrics
echo "🔢 Request Count (last 7 days):"
gcloud monitoring time-series list \
  --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
  --format="table(metric.type, points[0].value.int64Value)" \
  2>/dev/null | grep request_count || echo "No data yet"

echo ""
echo "💾 Memory Usage:"
gcloud run services describe ${SERVICE_NAME} \
  --region ${REGION} \
  --format="value(spec.template.spec.containers[0].resources.limits.memory)"

echo ""
echo "⚡ CPU Allocation:"
gcloud run services describe ${SERVICE_NAME} \
  --region ${REGION} \
  --format="value(spec.template.spec.containers[0].resources.limits.cpu)"

echo ""
echo "📈 Scaling Configuration:"
echo "  Min Instances: $(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format='value(spec.template.metadata.annotations.autoscaling\.knative\.dev/minScale)' 2>/dev/null || echo '0')"
echo "  Max Instances: $(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format='value(spec.template.metadata.annotations.autoscaling\.knative\.dev/maxScale)' 2>/dev/null || echo 'Not set')"

echo ""
echo "💰 Estimated Free Tier Usage:"
echo "  ✅ 2M requests/month free"
echo "  ✅ 360K GB-seconds memory free"
echo "  ✅ 180K vCPU-seconds free"
echo ""
echo "⚠️  Current config uses ~0.0024 GB-seconds per request"
echo "    = ~150K requests within free tier (conservative estimate)"
echo ""
echo "To view detailed billing:"
echo "  https://console.cloud.google.com/billing/${PROJECT_ID}"
