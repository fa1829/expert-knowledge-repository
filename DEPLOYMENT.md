# Cloud Deployment Guide

This guide provides instructions for deploying the Expert Knowledge Repository to various cloud platforms.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Google Cloud Platform](#google-cloud-platform)
5. [Azure Deployment](#azure-deployment)
6. [DigitalOcean Deployment](#digitalocean-deployment)

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed (optional)

### Using Docker Compose (Recommended)

1. **Clone the repository**:
```bash
git clone https://github.com/fa1829/expert-knowledge-repository.git
cd expert-knowledge-repository
```

2. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

3. **Build and run**:
```bash
docker-compose up -d
```

4. **Access the application**:
```
http://localhost:5000
```

### Using Docker Only

1. **Build the image**:
```bash
docker build -t expert-knowledge-repo .
```

2. **Run the container**:
```bash
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/search_index:/app/search_index \
  --name knowledge-repo \
  expert-knowledge-repo
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Login to Heroku**:
```bash
heroku login
```

2. **Create a new Heroku app**:
```bash
heroku create your-app-name
```

3. **Add PostgreSQL addon** (recommended for production):
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set environment variables**:
```bash
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set FLASK_ENV=production
```

5. **Create Procfile**:
```bash
echo "web: gunicorn app:app" > Procfile
```

6. **Add gunicorn to requirements.txt**:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

7. **Deploy**:
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

8. **Initialize the database**:
```bash
heroku run python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

9. **Access your app**:
```bash
heroku open
```

---

## AWS Deployment

### Using AWS Elastic Beanstalk

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize EB application**:
```bash
eb init -p python-3.11 expert-knowledge-repo
```

3. **Create environment**:
```bash
eb create production-env
```

4. **Set environment variables**:
```bash
eb setenv SECRET_KEY="your-secret-key" FLASK_ENV=production
```

5. **Deploy**:
```bash
eb deploy
```

6. **Open the application**:
```bash
eb open
```

### Using AWS ECS (Docker)

1. **Build and tag the Docker image**:
```bash
docker build -t expert-knowledge-repo .
docker tag expert-knowledge-repo:latest <account-id>.dkr.ecr.<region>.amazonaws.com/expert-knowledge-repo:latest
```

2. **Push to ECR**:
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/expert-knowledge-repo:latest
```

3. **Create ECS task definition and service** (via AWS Console or CLI)

---

## Google Cloud Platform

### Using Google App Engine

1. **Create app.yaml**:
```yaml
runtime: python311

env_variables:
  SECRET_KEY: "your-secret-key"
  FLASK_ENV: "production"

handlers:
- url: /.*
  script: auto
```

2. **Deploy**:
```bash
gcloud app deploy
```

3. **Open the application**:
```bash
gcloud app browse
```

### Using Google Cloud Run (Docker)

1. **Build and push to Google Container Registry**:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/expert-knowledge-repo
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy expert-knowledge-repo \
  --image gcr.io/PROJECT-ID/expert-knowledge-repo \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY="your-secret-key"
```

---

## Azure Deployment

### Using Azure App Service

1. **Login to Azure**:
```bash
az login
```

2. **Create a resource group**:
```bash
az group create --name expert-knowledge-rg --location eastus
```

3. **Create an App Service plan**:
```bash
az appservice plan create --name expert-knowledge-plan --resource-group expert-knowledge-rg --sku B1 --is-linux
```

4. **Create a web app**:
```bash
az webapp create --resource-group expert-knowledge-rg --plan expert-knowledge-plan --name your-app-name --runtime "PYTHON|3.11"
```

5. **Configure deployment**:
```bash
az webapp deployment source config-local-git --name your-app-name --resource-group expert-knowledge-rg
```

6. **Set environment variables**:
```bash
az webapp config appsettings set --resource-group expert-knowledge-rg --name your-app-name --settings SECRET_KEY="your-secret-key" FLASK_ENV=production
```

7. **Deploy**:
```bash
git remote add azure <deployment-url>
git push azure main
```

---

## DigitalOcean Deployment

### Using DigitalOcean App Platform

1. **Connect your GitHub repository** via the DigitalOcean web interface

2. **Configure the app**:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn app:app`

3. **Set environment variables**:
   - `SECRET_KEY`: Your secret key
   - `FLASK_ENV`: production

4. **Deploy** (automatic on git push)

### Using DigitalOcean Droplet (Docker)

1. **Create a Droplet** with Docker pre-installed

2. **SSH into the droplet**:
```bash
ssh root@your-droplet-ip
```

3. **Clone the repository**:
```bash
git clone https://github.com/fa1829/expert-knowledge-repository.git
cd expert-knowledge-repository
```

4. **Run with Docker Compose**:
```bash
docker-compose up -d
```

---

## Production Considerations

### Database

For production, use a managed database service:

- **Heroku**: Heroku Postgres
- **AWS**: RDS (PostgreSQL/MySQL)
- **GCP**: Cloud SQL
- **Azure**: Azure Database for PostgreSQL
- **DigitalOcean**: Managed Databases

Update `DATABASE_URL` environment variable accordingly.

### File Storage

For production file uploads, use object storage:

- **AWS**: S3
- **GCP**: Cloud Storage
- **Azure**: Blob Storage
- **DigitalOcean**: Spaces

### Security

1. **Generate a strong SECRET_KEY**:
```python
import secrets
print(secrets.token_hex(32))
```

2. **Use HTTPS**: Enable SSL/TLS certificates

3. **Environment variables**: Never commit secrets to version control

4. **Rate limiting**: Implement API rate limiting

5. **CORS**: Configure CORS for frontend applications

### Monitoring

Consider adding:
- Application monitoring (New Relic, Datadog)
- Error tracking (Sentry)
- Log aggregation (ELK Stack, CloudWatch)

### Backup

Set up regular backups for:
- Database
- Uploaded files
- Search index

### Scaling

For high traffic:
- Use a reverse proxy (Nginx)
- Enable caching (Redis)
- Use a CDN for static files
- Horizontal scaling with load balancer
- Database read replicas
