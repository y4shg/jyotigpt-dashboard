# GitHub Actions - Docker Build & GHCR Publishing

This repository includes automated workflows to build Docker images and publish them to GitHub Container Registry (GHCR).

## 📦 Available Workflows

### 1. `docker-publish.yml` - Simple Build & Push
**Triggers:**
- Push to `main` or `develop` branches
- Git tags matching `v*.*.*` (e.g., v1.0.0)
- Pull requests to `main`
- Manual trigger via GitHub UI

**Features:**
- Multi-platform builds (amd64, arm64)
- Automatic tagging (latest, version, SHA)
- Build caching for faster builds
- Artifact attestation for supply chain security

### 2. `docker-security.yml` - Build with Security Scanning
**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly scheduled scans (Sundays at midnight)

**Features:**
- Python code linting (flake8)
- Security scanning (bandit, Trivy)
- Vulnerability detection
- SARIF reports uploaded to GitHub Security

## 🚀 Quick Setup

### Step 1: Enable GitHub Container Registry

Your repository automatically has access to GHCR. No additional setup needed!

### Step 2: Configure Repository Settings

1. Go to your repository **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
3. Click **Save**

### Step 3: Make Repository Package Public (Optional)

By default, packages are private. To make public:

1. Go to your repository page
2. Click **Packages** on the right sidebar
3. Click on your package name
4. Click **Package settings**
5. Scroll to **Danger Zone** → Change visibility to **Public**

## 📋 Image Tags

Your images will be tagged as:

```
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest          # Latest from main branch
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:main            # Main branch
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:develop         # Develop branch
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:v1.0.0          # Semantic version
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:1.0             # Major.minor
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:1               # Major only
ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:sha-abc1234     # Git commit SHA
```

## 🔄 Triggering Builds

### Automatic (on push)
```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

### Release with version tag
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Manual trigger
1. Go to **Actions** tab in your repository
2. Select **"Build and Push to GHCR"** workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

## 📥 Using Your Published Image

### Pull from GHCR

```bash
# Pull the latest image
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest

# Pull a specific version
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:v1.0.0
```

### Run with Docker

```bash
docker run -d \
  --name jyotigpt-dashboard \
  -p 5000:5000 \
  --env-file .env \
  ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

### Update docker-compose.yml

Replace the `build: .` line with your image:

```yaml
version: '3.8'

services:
  dashboard:
    image: ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
    container_name: jyotigpt-dashboard
    restart: unless-stopped
    ports:
      - "5000:5000"
    env_file:
      - .env
```

Then run:
```bash
docker-compose pull
docker-compose up -d
```

## 🔐 Accessing Private Images

If your package is private, authenticate first:

```bash
# Create a Personal Access Token (PAT) with read:packages scope
# Go to: Settings → Developer settings → Personal access tokens → Tokens (classic)

# Login to GHCR
echo YOUR_PAT | docker login ghcr.io -u YOUR-USERNAME --password-stdin

# Now you can pull
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

## 🛡️ Security Features

### Vulnerability Scanning (Trivy)
- Scans for CVEs in base images and dependencies
- Results uploaded to GitHub Security tab
- Runs on every build and weekly

### Code Security (Bandit)
- Scans Python code for security issues
- Detects common security problems
- Reports available in Actions artifacts

### Supply Chain Security
- Build provenance attestation
- Signed artifacts with cosign
- Verifiable build process

## 📊 Monitoring Builds

### View Build Status

1. Go to **Actions** tab
2. Click on a workflow run
3. View logs and artifacts

### Build Badges

Add to your README.md:

```markdown
![Docker Build](https://github.com/YOUR-USERNAME/jyotigpt-dashboard/actions/workflows/docker-publish.yml/badge.svg)
```

## 🔧 Customization

### Change Build Triggers

Edit `.github/workflows/docker-publish.yml`:

```yaml
on:
  push:
    branches:
      - main
      - staging     # Add more branches
    paths-ignore:   # Ignore certain files
      - '**.md'
      - 'docs/**'
```

### Add Build Arguments

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    build-args: |
      CUSTOM_VAR=value
      ANOTHER_VAR=value
```

### Multi-stage Builds

Your Dockerfile already supports multi-stage builds. To optimize:

```dockerfile
# Add to Dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🐛 Troubleshooting

### Build Fails with Permission Error

Make sure you've enabled **read and write permissions** in repository settings.

### Can't Pull Private Image

```bash
# Generate PAT with read:packages scope
# Login before pulling
docker login ghcr.io
```

### Workflow Doesn't Trigger

Check:
- Workflow file is in `.github/workflows/`
- File has `.yml` extension
- Syntax is correct (use YAML validator)
- Branch matches trigger conditions

### Image Too Large

Optimize your Dockerfile:
- Use slim base images
- Remove unnecessary files
- Use `.dockerignore`
- Multi-stage builds

## 📝 Best Practices

1. **Tag releases properly**: Use semantic versioning (v1.0.0)
2. **Keep main stable**: Only merge tested code to main
3. **Use develop branch**: For active development
4. **Monitor security scans**: Review and fix vulnerabilities
5. **Update base images**: Regularly rebuild to get security patches
6. **Cache dependencies**: Let GitHub Actions cache your builds
7. **Document changes**: Use meaningful commit messages

## 🔄 Auto-Update Strategy

### Dependabot for Base Images

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## 📚 Additional Resources

- [GitHub Packages Documentation](https://docs.github.com/en/packages)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Container Registry Best Practices](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## 🎯 Example: Complete Release Workflow

```bash
# 1. Make changes
git checkout -b feature/new-dashboard
# ... make changes ...
git commit -m "Add new dashboard feature"
git push origin feature/new-dashboard

# 2. Create PR (triggers test workflow)
# Review and merge to main

# 3. Tag release
git checkout main
git pull
git tag -a v1.2.0 -m "Release v1.2.0: New dashboard feature"
git push origin v1.2.0

# 4. GitHub Actions automatically:
# - Builds image
# - Scans for vulnerabilities
# - Pushes to GHCR with tags: v1.2.0, 1.2, 1, latest

# 5. Deploy
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:v1.2.0
docker-compose up -d
```

---

**Need help?** Open an issue in the repository!
