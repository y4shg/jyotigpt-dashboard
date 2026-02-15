# Using the Pre-built Docker Image from GHCR

Instead of building locally, you can pull the pre-built image from GitHub Container Registry.

## Quick Start with GHCR Image

### 1. Pull the image

```bash
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

### 2. Run with docker-compose (Recommended)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  dashboard:
    image: ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
    container_name: jyotigpt-dashboard
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - ADMIN_USERNAME=${ADMIN_USERNAME}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD}
      - OPENWEBUI_URL=${OPENWEBUI_URL}
      - OPENWEBUI_ADMIN_TOKEN=${OPENWEBUI_ADMIN_TOKEN}
      - HF_TOKEN=${HF_TOKEN}
      - HF_SPACE_IDS=${HF_SPACE_IDS}
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Create your `.env` file, then:

```bash
docker-compose up -d
```

### 3. Run with Docker CLI

```bash
docker run -d \
  --name jyotigpt-dashboard \
  -p 5000:5000 \
  --env-file .env \
  --restart unless-stopped \
  ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## Available Tags

- `latest` - Latest stable release from main branch
- `main` - Latest commit on main branch
- `develop` - Latest commit on develop branch
- `v1.0.0` - Specific version (semantic versioning)
- `1.0` - Major.minor version
- `1` - Major version only
- `sha-abc1234` - Specific commit

## Examples

### Run a specific version

```bash
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:v1.0.0
docker run -d -p 5000:5000 --env-file .env \
  ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:v1.0.0
```

### Update to latest version

```bash
docker-compose pull
docker-compose up -d
```

Or with Docker CLI:

```bash
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
docker stop jyotigpt-dashboard
docker rm jyotigpt-dashboard
docker run -d --name jyotigpt-dashboard -p 5000:5000 --env-file .env \
  ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## Watchtower Auto-Updates

Use Watchtower to automatically update your container:

```yaml
version: '3.8'

services:
  dashboard:
    image: ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
    # ... other config ...

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 3600 jyotigpt-dashboard
```

## Multi-Architecture Support

The image supports both amd64 and arm64:

```bash
# Works on Intel/AMD servers
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest

# Also works on ARM (Raspberry Pi, Apple Silicon, AWS Graviton)
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## Checking Image Info

```bash
# View image labels
docker inspect ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest

# View image layers
docker history ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## Benefits of Using GHCR Image

✅ **No build time** - Ready to use immediately
✅ **Security scanned** - Automatically scanned for vulnerabilities
✅ **Multi-platform** - Works on amd64 and arm64
✅ **Cached** - Faster pulls with layer caching
✅ **Versioned** - Easy rollback to previous versions
✅ **Automated** - Built and pushed automatically on every commit

## Private Repository Access

If your repository/package is private:

```bash
# Create a Personal Access Token with read:packages scope
# https://github.com/settings/tokens

# Login to GHCR
echo YOUR_PAT | docker login ghcr.io -u YOUR-USERNAME --password-stdin

# Pull the image
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## Image Size

The optimized image is approximately **150-200MB** (compressed).

## Troubleshooting

### Cannot pull image

```bash
# Check if package exists and is public
# Visit: https://github.com/YOUR-USERNAME/jyotigpt-dashboard/pkgs/container/jyotigpt-dashboard

# If private, authenticate first
docker login ghcr.io
```

### Image not found

Make sure:
1. Repository name is correct (lowercase)
2. Package is public or you're authenticated
3. Image has been built (check Actions tab)

### Old version still running

```bash
# Force pull latest
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest --no-cache

# Recreate container
docker-compose up -d --force-recreate
```
