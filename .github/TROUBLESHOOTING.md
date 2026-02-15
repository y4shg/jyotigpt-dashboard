# GitHub Actions Troubleshooting

## Common Issues and Solutions

### ❌ Error: "docker exporter does not support exporting manifest lists"

**Problem:** Trying to build multi-platform images and save to a tar file at the same time.

**Solution:** Use the simpler `build.yml` workflow which pushes directly to GHCR without intermediate tar files.

**Quick Fix:**
```bash
# Use the main build.yml workflow (recommended)
# It's simpler and more reliable
```

---

### ❌ Error: "permission denied while trying to connect to the Docker daemon"

**Problem:** GitHub Actions doesn't have permission to write to GHCR.

**Solution:**
1. Go to **Settings** → **Actions** → **General**
2. Scroll to "Workflow permissions"
3. Select **"Read and write permissions"**
4. Click **Save**

---

### ❌ Error: "failed to solve: failed to push"

**Problem:** Image push failed (usually network or permissions).

**Solution:**
1. Verify your repository has packages permission
2. Check if GITHUB_TOKEN has write access
3. Try re-running the workflow

---

### ❌ Workflow doesn't trigger

**Problem:** Pushing code but workflow doesn't start.

**Solutions:**
1. **Check workflow is in correct location:** `.github/workflows/`
2. **Verify file extension:** Must be `.yml` or `.yaml`
3. **Check syntax:** Use a YAML validator
4. **Verify branch name:** Make sure it matches workflow triggers
5. **Check Actions are enabled:**
   - Go to **Settings** → **Actions** → **General**
   - Verify Actions are allowed

---

### ❌ Build succeeds but can't find image

**Problem:** Build completes but package not visible.

**Solutions:**
1. **Check package visibility:**
   - Go to your repository
   - Click **Packages** on right sidebar
   - Click your package
   - **Package settings** → Make it public if needed

2. **Wait a moment:** Packages can take a few seconds to appear

3. **Check correct registry:**
   ```bash
   # Correct format
   ghcr.io/USERNAME/REPO-NAME:latest
   
   # Wrong - Docker Hub (different registry)
   docker.io/USERNAME/REPO-NAME:latest
   ```

---

### ❌ Can't pull image: "unauthorized"

**Problem:** Private package or not authenticated.

**Solutions:**

1. **Make package public:**
   - Repository → **Packages** → Your package
   - **Package settings** → Change to **Public**

2. **Or authenticate:**
   ```bash
   # Create PAT with read:packages scope
   # https://github.com/settings/tokens
   
   echo YOUR_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin
   ```

---

### ❌ Build is very slow

**Problem:** Building takes a long time.

**Solutions:**
1. **Enable caching:** Already enabled in workflows
2. **Reduce image size:** Use `.dockerignore`
3. **Use smaller base image:** Already using `python:3.11-slim`
4. **Multi-stage builds:** Consider if you need multiple stages

**Check cache:**
```yaml
# Cache is enabled with:
cache-from: type=gha
cache-to: type=gha,mode=max
```

---

### ❌ ARM64 build fails

**Problem:** ARM64 platform fails while AMD64 succeeds.

**Solutions:**
1. **Use QEMU:** Already configured in `build.yml`
2. **Test locally:**
   ```bash
   docker buildx build --platform linux/arm64 -t test .
   ```
3. **Temporarily build single platform:**
   ```yaml
   platforms: linux/amd64  # Remove ,linux/arm64
   ```

---

### ❌ Vulnerability scan fails build

**Problem:** Trivy finds critical vulnerabilities.

**Solutions:**
1. **Review vulnerabilities:** Check Security tab
2. **Update base image:**
   ```dockerfile
   FROM python:3.11-slim  # Use latest
   ```
3. **Update dependencies:**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```
4. **Temporarily allow failures:**
   ```yaml
   exit-code: '0'  # Don't fail on vulnerabilities
   ```

---

### ❌ Secrets not working in workflow

**Problem:** Environment variables from secrets are empty.

**Solutions:**
1. **Don't use secrets in builds:** Secrets aren't available during `docker build`
2. **Use build args for non-sensitive data:**
   ```yaml
   build-args: |
     VERSION=${{ github.sha }}
   ```
3. **Inject secrets at runtime:** Not during build
   ```bash
   docker run -e SECRET_KEY=$SECRET_KEY myimage
   ```

---

### ❌ Workflow takes too long (times out)

**Problem:** Build exceeds 6 hour timeout.

**Solutions:**
1. **Optimize Dockerfile:** Multi-stage builds, smaller base
2. **Reduce platforms:** Build only linux/amd64
3. **Use self-hosted runner:** For large projects
4. **Split into multiple workflows**

---

## Workflow Recommendations

### ✅ Recommended: Use `build.yml`

**Simple, reliable, tested:**
```yaml
# .github/workflows/build.yml
# - Builds on push to main/develop
# - Multi-platform (amd64, arm64)
# - Automatic tagging
# - Fast and reliable
```

### ⚠️ Optional: `docker-security.yml`

**Use only if you need:**
- Security scanning reports
- Python linting
- SARIF uploads to GitHub Security

**Note:** More complex, requires additional setup

### 🚫 Deprecated: `docker-publish.yml`

**Don't use:** Has attestation issues on some configurations.
**Instead use:** `build.yml`

---

## Debugging Workflows

### View Detailed Logs

1. Go to **Actions** tab
2. Click failed workflow run
3. Click failed job
4. Expand step to see full logs

### Enable Debug Logging

Add to your workflow:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Test Locally

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act push
```

---

## Quick Fixes

### Reset Everything

```bash
# 1. Delete all workflow runs
# GitHub → Actions → Click ... → Delete workflow runs

# 2. Delete package
# GitHub → Packages → Package settings → Delete package

# 3. Re-run workflow
# Actions → Build → Re-run all jobs
```

### Force Rebuild (No Cache)

Add to workflow temporarily:
```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    no-cache: true  # Add this line
    # ... rest of config
```

### Test Build Locally

```bash
# Build locally to test
docker build -t test .

# Build multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t test .
```

---

## Getting Help

### Check These First:
1. ✅ Workflow syntax correct?
2. ✅ Permissions enabled?
3. ✅ Branch name matches trigger?
4. ✅ Docker syntax correct?
5. ✅ Check Actions tab for errors?

### Still Stuck?

1. **Review workflow logs:** Actions → Failed run → View logs
2. **Check Docker build:** Test locally first
3. **Simplify:** Use `build.yml` instead of complex workflows
4. **Check GitHub Status:** https://www.githubstatus.com/

---

## Workflow Comparison

| Feature | build.yml | docker-security.yml | docker-publish.yml |
|---------|-----------|---------------------|-------------------|
| Complexity | ✅ Simple | ⚠️ Complex | ⚠️ Medium |
| Reliability | ✅ High | ⚠️ Medium | ❌ Issues |
| Security Scan | ❌ No | ✅ Yes | ❌ No |
| Speed | ✅ Fast | ⚠️ Slower | ✅ Fast |
| **Recommended** | **YES** | Optional | No |

---

**Recommendation:** Start with `build.yml` - it's simple, reliable, and does everything you need!
