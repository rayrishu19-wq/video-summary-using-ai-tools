#!/bin/bash

# Video Summarizer AI - Cloud Run Deployment Script
# This script automates the deployment process to Google Cloud Run

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${PROJECT_ID:-""}
SERVICE_NAME=${SERVICE_NAME:-"video-summarizer"}
REGION=${REGION:-"us-central1"}
API_KEY=${GEMINI_API_KEY:-""}

echo -e "${BLUE}🚀 Video Summarizer AI - Cloud Run Deployment${NC}"
echo "=================================================="

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud CLI (gcloud) is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not authenticated with Google Cloud.${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Get project ID if not set
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ No project ID set.${NC}"
        echo "Please set PROJECT_ID environment variable or run: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Project ID: $PROJECT_ID${NC}"

# Check if API key is provided
if [ -z "$API_KEY" ]; then
    echo -e "${YELLOW}⚠️  No GEMINI_API_KEY provided.${NC}"
    echo "You can set it as an environment variable or it will be prompted during deployment."
    echo "To set it: export GEMINI_API_KEY=your_api_key_here"
fi

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
gcloud services enable containerregistry.googleapis.com --project=$PROJECT_ID

# Build and deploy
echo -e "${YELLOW}🏗️  Building and deploying to Cloud Run...${NC}"

# Prepare deployment command
DEPLOY_CMD="gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900 \
  --max-instances 10 \
  --project $PROJECT_ID"

# Add API key if provided
if [ ! -z "$API_KEY" ]; then
    DEPLOY_CMD="$DEPLOY_CMD --set-env-vars GEMINI_API_KEY=$API_KEY"
fi

# Execute deployment
echo -e "${BLUE}Executing: $DEPLOY_CMD${NC}"
eval $DEPLOY_CMD

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo -e "${GREEN}🎉 Deployment successful!${NC}"
echo "=================================================="
echo -e "${GREEN}🌐 Service URL: $SERVICE_URL${NC}"
echo -e "${GREEN}📝 API Endpoint: $SERVICE_URL/api/summarize${NC}"
echo -e "${GREEN}🏥 Health Check: $SERVICE_URL/health${NC}"
echo ""
echo -e "${YELLOW}📊 View logs:${NC}"
echo "gcloud logs tail --service=$SERVICE_NAME --project=$PROJECT_ID"
echo ""
echo -e "${YELLOW}🔧 Update service:${NC}"
echo "gcloud run deploy $SERVICE_NAME --source . --region=$REGION"
echo ""
echo -e "${GREEN}Your Video Summarizer AI is now live! 🎥✨${NC}" 