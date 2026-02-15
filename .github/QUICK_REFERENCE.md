# GitHub Actions Quick Reference

## 🚀 What You Got

Three automated workflows (use **build.yml** - it's the best one!):

1. **build.yml** ⭐ **RECOMMENDED** - Simple, fast, reliable
2. **docker-security.yml** - Advanced with security scanning (optional)
3. **docker-publish.yml** - Original (use build.yml instead)

## 📦 Setup (3 Steps)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/jyotigpt-dashboard.git
git push -u origin main
```

### 2. Enable Workflows

Go to your repository → **Settings** → **Actions** → **General**

Set:
- ✅ **Read and write permissions**
- ✅ **Allow GitHub Actions to create and approve pull requests**

Click **Save**

### 3. Done! 

GitHub Actions will automatically:
- Build your Docker image
- Scan for vulnerabilities  
- Push to `ghcr.io/YOUR-USERNAME/jyotigpt-dashboard`

## 🎯 Using Your Image

### Pull and run:

```bash
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
docker run -d -p 5000:5000 --env-file .env \
  ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
```

### Update docker-compose.yml:

```yaml
services:
  dashboard:
    image: ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
    # ... rest of config
```

## 🏷️ Available Tags

Every push creates these tags:
- `latest` - Latest from main branch
- `main` - Main branch
- `sha-abc1234` - Specific commit

Every release (git tag v1.0.0):
- `v1.0.0` - Full version
- `1.0` - Major.minor
- `1` - Major only

## 🔄 Release New Version

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

GitHub Actions automatically builds and pushes with all version tags!

## 🔍 View Builds

1. Go to **Actions** tab in your repository
2. Click on a workflow run
3. View logs and download artifacts

## 🛡️ Security Features

✅ Vulnerability scanning (Trivy)
✅ Python security checks (Bandit)  
✅ Multi-platform builds (amd64, arm64)
✅ Build attestation for supply chain security

## 📊 Add Build Badge

Add to your README.md:

```markdown
![Docker Build](https://github.com/YOUR-USERNAME/jyotigpt-dashboard/actions/workflows/docker-publish.yml/badge.svg)
```

## 🔐 Make Package Public

By default, packages are private. To make public:

1. Go to repository → **Packages** (right sidebar)
2. Click your package
3. **Package settings** → Change visibility to **Public**

## 📚 Full Documentation

- **GITHUB_ACTIONS.md** - Complete guide
- **GHCR_USAGE.md** - Using published images
- **DEPLOYMENT.md** - Production deployment

## ⚡ Quick Commands

```bash
# Manual trigger (from GitHub UI)
Actions → Build and Push to GHCR → Run workflow

# View your published images
https://github.com/YOUR-USERNAME?tab=packages

# Pull latest
docker pull ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest

# Update running container
docker-compose pull && docker-compose up -d
```

## 🎉 That's It!

Push to GitHub and watch it build automatically. No Docker build time on deployment!

---

**Replace `YOUR-USERNAME`** with your actual GitHub username in all commands!
