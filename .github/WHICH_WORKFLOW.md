# Which Workflow Should I Use?

## ⭐ TL;DR: Use `build.yml`

**Just use `.github/workflows/build.yml` - it's simple, reliable, and does everything you need.**

---

## Workflow Comparison

### ✅ `build.yml` - RECOMMENDED

**Use this one!**

**What it does:**
- Builds Docker image on push to main/develop
- Supports multi-platform (amd64, arm64)
- Pushes to GitHub Container Registry
- Automatic semantic versioning
- Fast build caching

**When to use:**
- ✅ Always (this is the default choice)
- ✅ You want something that just works
- ✅ You don't need security scanning reports
- ✅ You want fast, reliable builds

**Example:** 
```bash
# Push code
git push origin main

# Workflow automatically:
# 1. Builds your image
# 2. Pushes to ghcr.io/YOUR-USERNAME/jyotigpt-dashboard:latest
# 3. Done! Pull and use it
```

---

### 🔒 `docker-security.yml` - OPTIONAL

**Only use if you need security features.**

**What it does:**
- Everything `build.yml` does, PLUS:
- Python code linting (flake8)
- Security vulnerability scanning (Trivy, Bandit)
- SARIF report upload to GitHub Security tab
- Runs tests before building

**When to use:**
- ⚠️ You need security compliance reports
- ⚠️ You want automated vulnerability scanning
- ⚠️ You have GitHub Advanced Security enabled
- ⚠️ You need detailed security audit trails

**Tradeoffs:**
- ❌ Slower builds (runs tests + scans)
- ❌ More complex
- ❌ Requires additional GitHub features for full benefit

---

### 🚫 `docker-publish.yml` - DON'T USE

**Kept for reference only. Has known issues.**

**Issues:**
- ❌ Attestation problems on some configurations
- ❌ Less reliable than `build.yml`
- ❌ Not actively maintained

**Recommendation:** Delete this file and use `build.yml` instead.

---

## Quick Decision Tree

```
Do you need security scanning reports? 
├─ NO  → Use build.yml ✅
└─ YES → Do you have GitHub Advanced Security?
    ├─ NO  → Use build.yml ✅ (scanning won't help without it)
    └─ YES → Use docker-security.yml 🔒
```

---

## How to Switch Workflows

### Option 1: Use build.yml (Recommended)

**Already enabled!** Just push your code:

```bash
git add .
git commit -m "Update app"
git push origin main
```

The `build.yml` workflow will automatically run.

### Option 2: Enable docker-security.yml

If you really need security scanning:

1. **Keep both workflows** - They don't conflict
2. **build.yml** runs on every push (fast)
3. **docker-security.yml** runs on every push (with scans)
4. Both produce the same image

Or rename to disable `build.yml`:

```bash
mv .github/workflows/build.yml .github/workflows/build.yml.disabled
```

### Option 3: Disable a workflow

Delete or rename the file:

```bash
# Disable docker-security.yml
rm .github/workflows/docker-security.yml

# Or disable build.yml (not recommended)
rm .github/workflows/build.yml
```

---

## Testing Before Committing

### Test Locally First

```bash
# Build locally to verify it works
docker build -t test .

# Run it
docker run -d -p 5000:5000 --env-file .env test

# Test it
curl http://localhost:5000/api/health
```

### Dry Run with Act

```bash
# Install act (local GitHub Actions runner)
brew install act  # macOS
# or: https://github.com/nektos/act

# Test workflow locally
act push
```

---

## Monitoring Your Workflows

### Check Build Status

1. Go to **Actions** tab in your repository
2. See all workflow runs
3. Click on any run to see details

### Add Status Badge

Add to your `README.md`:

```markdown
![Build Status](https://github.com/YOUR-USERNAME/jyotigpt-dashboard/actions/workflows/build.yml/badge.svg)
```

---

## Common Questions

### Q: Can I use both build.yml and docker-security.yml?

**A:** Yes! They don't conflict. Both will run and produce the same image. Use `build.yml` for speed and `docker-security.yml` when you need the security reports.

### Q: Which one is faster?

**A:** `build.yml` is fastest (2-5 minutes). `docker-security.yml` takes longer (5-10 minutes) because of scanning.

### Q: Do I need both?

**A:** No. `build.yml` alone is sufficient for most users.

### Q: What about docker-publish.yml?

**A:** Don't use it. It has issues. Use `build.yml` instead.

### Q: Will this cost money?

**A:** GitHub Actions is free for public repositories. Private repos get 2000 minutes/month free.

---

## Troubleshooting

See `.github/TROUBLESHOOTING.md` for common issues and solutions.

**Most common fix:** Go to **Settings** → **Actions** → **General** → Enable "Read and write permissions"

---

## Summary

**Use `build.yml`** - it's the right choice for 99% of users. Simple, fast, reliable.

Only use `docker-security.yml` if you specifically need security scanning reports and have Advanced Security enabled.

Delete `docker-publish.yml` - it's outdated.

**That's it! Just push your code and watch it build! 🚀**
