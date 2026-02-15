# JyotiGPT Dashboard - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Quick Setup (Recommended for Testing)

```bash
# 1. Navigate to the project directory
cd jyotigpt-dashboard

# 2. Run the setup script
bash setup.sh

# 3. Edit .env with your credentials
nano .env

# 4. Run the application
python app.py
```

Visit: http://localhost:5000

### Option 2: Docker (Recommended for Production)

```bash
# 1. Configure environment
cp .env.example .env
nano .env  # Edit with your credentials

# 2. Start with Docker Compose
docker-compose up -d

# 3. View logs
docker-compose logs -f
```

Visit: http://localhost:5000

## 📋 Configuration Checklist

Edit your `.env` file with these required values:

```env
✅ SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
✅ ADMIN_USERNAME=admin
✅ ADMIN_PASSWORD=<your secure password>
✅ JYOTIGPT_URL=https://your-jyotigpt-instance.com
✅ JYOTIGPT_ADMIN_TOKEN=<your admin token>

Optional (for HuggingFace Spaces management):
⭕ HF_TOKEN=hf_your_token_here
⭕ HF_SPACE_IDS=username/space1,username/space2
```

## 🔑 Getting Your Tokens

### JyotiGPT Admin Token
1. Log in to your JyotiGPT instance
2. Go to Settings → Account → API Keys
3. Click "Create new secret key"
4. Copy the token

### HuggingFace Token
1. Visit https://huggingface.co/settings/tokens
2. Click "New token"
3. Select "read" and "write" permissions
4. Copy the token

## 🔐 Default Login

- **Username**: admin (or your ADMIN_USERNAME)
- **Password**: (set in .env file)

⚠️ **Change the default password immediately!**

## 📊 Features Overview

### Dashboard Sections

1. **JyotiGPT Analytics**
   - Total messages, tokens, users, and chats
   - Real-time statistics from your instance

2. **Top Models**
   - Most used AI models
   - Message and token counts

3. **Top Users**
   - Most active users
   - Usage statistics

4. **HuggingFace Spaces**
   - Monitor space status (running/stopped)
   - Restart or pause spaces with one click

5. **Service Links**
   - Quick access to all AI services
   - Internal management tools

6. **System Status**
   - Embedded Uptime Kuma monitoring
   - Real-time service health

## 🔧 Common Commands

### Development
```bash
# Run in development mode
python app.py

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

### Production
```bash
# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Check logs (systemd)
sudo journalctl -u jyotigpt-dashboard -f

# Check logs (Docker)
docker-compose logs -f

# Restart service
sudo systemctl restart jyotigpt-dashboard
# or
docker-compose restart
```

## 🐛 Troubleshooting

### Cannot login
- Check ADMIN_USERNAME and ADMIN_PASSWORD in .env
- Ensure SECRET_KEY is set
- Clear browser cookies

### JyotiGPT data not loading
- Verify JYOTIGPT_URL is correct (include https://)
- Check JYOTIGPT_ADMIN_TOKEN is valid
- Test connection: `curl -H "Authorization: Bearer TOKEN" URL/api/v1/analytics/summary`

### HuggingFace Spaces not showing
- Verify HF_TOKEN has correct permissions
- Check HF_SPACE_IDS format (username/space-name)
- Ensure spaces exist and you have access

### Port 5000 already in use
```bash
# Find and kill the process
sudo lsof -i :5000
sudo kill -9 <PID>
```

## 📚 Documentation

- **README.md** - Complete documentation
- **DEPLOYMENT.md** - Production deployment guide
- **templates/** - HTML templates for customization

## 🔒 Security Best Practices

1. ✅ Use strong passwords (20+ characters)
2. ✅ Enable HTTPS in production (use Nginx/Caddy)
3. ✅ Set SESSION_COOKIE_SECURE=True with HTTPS
4. ✅ Keep dependencies updated
5. ✅ Never commit .env to version control
6. ✅ Use firewall to restrict access
7. ✅ Regular security audits
8. ✅ Enable fail2ban for brute force protection

## 🚀 Production Deployment

For production deployment, follow **DEPLOYMENT.md** for:
- Nginx/Caddy reverse proxy setup
- SSL/TLS certificate configuration
- Systemd service configuration
- Security hardening
- Monitoring and logging
- Backup strategies

## 📞 Support

- Review logs for errors
- Check configuration in .env
- Verify API endpoints are accessible
- Test with curl commands

## 📦 Project Structure

```
jyotigpt-dashboard/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example       # Configuration template
├── .env               # Your configuration (don't commit!)
├── setup.sh           # Quick setup script
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── README.md          # Full documentation
├── DEPLOYMENT.md      # Production guide
├── QUICKSTART.md      # This file
└── templates/
    ├── login.html     # Login page
    ├── dashboard.html # Main dashboard
    └── error.html     # Error pages
```

## ⚡ Quick Tips

1. **Auto-refresh**: Dashboard refreshes every 5 minutes automatically
2. **Manual refresh**: Click the "🔄 Refresh" button
3. **Space management**: Confirm before restarting/pausing spaces
4. **Session timeout**: 24 hours by default (configurable)
5. **Mobile friendly**: Responsive design works on all devices

## 🎯 Next Steps

1. ✅ Complete setup and configuration
2. ✅ Test all features
3. ✅ Set up reverse proxy (production)
4. ✅ Configure SSL/TLS certificates
5. ✅ Set up monitoring and backups
6. ✅ Review and adjust security settings

---

**Ready to deploy?** See DEPLOYMENT.md for production setup!
