# 🚀 Cloud Run Deployment Guide

This guide will help you deploy your Video Summarizer AI app to Google Cloud Run.

## 📋 Prerequisites

### Required Tools

- **Google Cloud CLI** (gcloud)
- **Docker** (for local testing)
- **Node.js** (v18+)

### Required Accounts

- **Google Cloud Account** with billing enabled
- **Google AI Studio Account** for Gemini API access

## 🔧 Setup Steps

### 1. Install Google Cloud CLI

#### macOS

```bash
# Using Homebrew
brew install google-cloud-sdk

# Or download from Google Cloud
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### Windows

```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install#windows
```

#### Linux

```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install#linux
```

### 2. Initialize Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Configure Docker for Google Cloud

```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker
```

## 🏗️ Build and Deploy

### Option 1: Deploy with Cloud Build (Recommended)

```bash
# Build and deploy in one command
gcloud run deploy video-summarizer \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900 \
  --max-instances 10
```

### Option 2: Build Locally and Deploy

```bash
# Build the Docker image locally
docker build -t gcr.io/YOUR_PROJECT_ID/video-summarizer .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/video-summarizer

# Deploy to Cloud Run
gcloud run deploy video-summarizer \
  --image gcr.io/YOUR_PROJECT_ID/video-summarizer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900 \
  --max-instances 10
```

## ⚙️ Configuration Options

### Environment Variables

| Variable         | Description           | Required | Default    |
| ---------------- | --------------------- | -------- | ---------- |
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes   | None       |
| `PORT`           | Server port           | ❌ No    | 8080       |
| `NODE_ENV`       | Environment mode      | ❌ No    | production |

### Resource Configuration

| Resource          | Recommended  | Minimum |
| ----------------- | ------------ | ------- |
| **Memory**        | 2Gi          | 512Mi   |
| **CPU**           | 2            | 1       |
| **Timeout**       | 900s (15min) | 300s    |
| **Max Instances** | 10           | 1       |

### Security Settings

```bash
# Deploy with authentication required
gcloud run deploy video-summarizer \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

## 🔐 Secure API Key Management

### Option 1: Environment Variable (Development)

```bash
gcloud run deploy video-summarizer \
  --source . \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

### Option 2: Secret Manager (Production - Recommended)

```bash
# Create a secret
echo -n "your_api_key_here" | gcloud secrets create gemini-api-key --data-file=-

# Deploy with secret reference
gcloud run deploy video-summarizer \
  --source . \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

### Option 3: Cloud Build with Secret

```bash
# Create a secret
echo -n "your_api_key_here" | gcloud secrets create gemini-api-key --data-file=-

# Grant Cloud Build access to the secret
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy video-summarizer \
  --source . \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

## 🌐 Custom Domain Setup

### 1. Map Custom Domain

```bash
gcloud run domain-mappings create \
  --service video-summarizer \
  --domain your-domain.com \
  --region us-central1
```

### 2. Update DNS Records

Add the provided CNAME record to your domain's DNS settings.

## 📊 Monitoring and Logging

### View Logs

```bash
# View real-time logs
gcloud logs tail --service=video-summarizer

# View specific log entries
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=video-summarizer"
```

### Set Up Monitoring

```bash
# Create alerting policy for errors
gcloud alpha monitoring policies create \
  --policy-from-file=monitoring-policy.yaml
```

## 🔄 Continuous Deployment

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Google Cloud CLI
        uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy video-summarizer \
            --source . \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

## 🧪 Testing Deployment

### Health Check

```bash
# Test health endpoint
curl https://your-service-url/health
```

### API Test

```bash
# Test video summarization
curl -X POST https://your-service-url/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "videoURL": "https://example.com/video.mp4",
    "prompt": "Summarize this video"
  }'
```

## 🚨 Troubleshooting

### Common Issues

#### Build Failures

```bash
# Check build logs
gcloud builds log BUILD_ID

# Rebuild with verbose output
gcloud run deploy video-summarizer --source . --verbosity=debug
```

#### Runtime Errors

```bash
# Check service logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=video-summarizer" --limit=50
```

#### Memory Issues

```bash
# Increase memory allocation
gcloud run deploy video-summarizer \
  --source . \
  --memory 4Gi \
  --cpu 2
```

#### Timeout Issues

```bash
# Increase timeout
gcloud run deploy video-summarizer \
  --source . \
  --timeout 1800
```

### Performance Optimization

#### Enable Autoscaling

```bash
gcloud run deploy video-summarizer \
  --source . \
  --min-instances 0 \
  --max-instances 10 \
  --cpu-throttling
```

#### Optimize Cold Starts

```bash
# Keep at least one instance warm
gcloud run deploy video-summarizer \
  --source . \
  --min-instances 1
```

## 💰 Cost Optimization

### Resource Recommendations

- **Development**: 512Mi memory, 1 CPU
- **Production**: 2Gi memory, 2 CPU
- **High Traffic**: 4Gi memory, 4 CPU

### Cost Monitoring

```bash
# View cost breakdown
gcloud billing budgets list

# Set up billing alerts
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --budget-amount=100USD \
  --budget-filter-projects=YOUR_PROJECT_ID
```

## 🔄 Updates and Rollbacks

### Update Service

```bash
# Deploy new version
gcloud run deploy video-summarizer --source .

# Rollback to previous version
gcloud run revisions list --service=video-summarizer
gcloud run services update-traffic video-summarizer --to-revisions=REVISION_NAME=100
```

### Blue-Green Deployment

```bash
# Deploy new version with traffic splitting
gcloud run deploy video-summarizer-v2 --source .
gcloud run services update-traffic video-summarizer \
  --to-revisions=video-summarizer-v2=50,REVISION_NAME=50
```

---

**Your Video Summarizer AI is now deployed and ready to use!** 🎥✨

For more information, visit:

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Genkit Cloud Run Guide](https://genkit.dev/docs/cloud-run/)
- [Google Cloud Pricing](https://cloud.google.com/run/pricing)
