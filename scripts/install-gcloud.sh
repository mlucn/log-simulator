#!/bin/bash
# Install Google Cloud SDK on Ubuntu/Debian

set -e

echo "Installing Google Cloud SDK..."

# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install the Cloud SDK
sudo apt-get update && sudo apt-get install -y google-cloud-cli

# Verify installation
gcloud version

echo ""
echo "✅ Google Cloud SDK installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: gcloud init"
echo "2. Or run: ./scripts/deploy-cloudrun.sh"
