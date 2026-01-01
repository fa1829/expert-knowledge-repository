# DEPLOYMENT (AWS outline)

Fast path:
- EC2 + Docker Compose
- Caddy/Nginx for HTTPS + domain

Scale path:
- S3 for files + CloudFront CDN
- App handles metadata + access control + index
- Cognito for auth
