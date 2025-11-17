#!/bin/bash
# Set up budget alerts for Cloud Run

set -e

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
BUDGET_AMOUNT="${BUDGET_AMOUNT:-5}" # Default $5/month

echo "Setting up budget alert for project: ${PROJECT_ID}"
echo "Budget amount: \$${BUDGET_AMOUNT}/month"
echo ""

# Create budget with email alert
gcloud billing budgets create \
  --billing-account=$(gcloud billing projects describe ${PROJECT_ID} --format="value(billingAccountName)") \
  --display-name="Cloud Run Budget Alert" \
  --budget-amount=${BUDGET_AMOUNT} \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=75 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100

echo ""
echo "✅ Budget alerts configured!"
echo "You'll receive emails at 50%, 75%, 90%, and 100% of \$${BUDGET_AMOUNT}"
echo ""
echo "To change the budget amount, run:"
echo "  BUDGET_AMOUNT=10 ./scripts/setup-budget-alert.sh"
