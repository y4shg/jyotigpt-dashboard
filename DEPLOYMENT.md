# Production Deployment Guide

This guide covers deploying the JyotiGPT Dashboard to production environments.

## Quick Deploy Options

### 1. Docker Deployment (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed
- `.env` file configured

**Steps:**

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

**Using Docker without Compose:**

```bash
# Build the image
docker build -t jyotigpt-dashboard .

# Run the container
docker run -d \
  --name jyotigpt-dashboard \
  -p 5000:5000 \
  --env-file .env \
  --restart unless-stopped \
  jyotigpt-dashboard
```

### 2. Systemd Service (Linux)

**Create service file:** `/etc/systemd/system/jyotigpt-dashboard.service`

```ini
[Unit]
Description=JyotiGPT Dashboard
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/jyotigpt-dashboard
Environment="PATH=/opt/jyotigpt-dashboard/venv/bin"
EnvironmentFile=/opt/jyotigpt-dashboard/.env
ExecStart=/opt/jyotigpt-dashboard/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/jyotigpt/access.log \
    --error-logfile /var/log/jyotigpt/error.log \
    app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
# Create log directory
sudo mkdir -p /var/log/jyotigpt
sudo chown www-data:www-data /var/log/jyotigpt

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable jyotigpt-dashboard

# Start service
sudo systemctl start jyotigpt-dashboard

# Check status
sudo systemctl status jyotigpt-dashboard

# View logs
sudo journalctl -u jyotigpt-dashboard -f
```

## Reverse Proxy Configuration

### Nginx

**Create config:** `/etc/nginx/sites-available/jyotigpt-dashboard`

```nginx
server {
    listen 80;
    server_name dashboard.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dashboard.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/dashboard.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dashboard.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files caching (if you add static assets)
    location /static/ {
        alias /opt/jyotigpt-dashboard/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    access_log /var/log/nginx/jyotigpt-access.log;
    error_log /var/log/nginx/jyotigpt-error.log;
}
```

**Enable and restart:**

```bash
sudo ln -s /etc/nginx/sites-available/jyotigpt-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Caddy (Automatic HTTPS)

**Create Caddyfile:**

```caddy
dashboard.yourdomain.com {
    reverse_proxy localhost:5000
    
    # Security headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
    }
    
    # Logging
    log {
        output file /var/log/caddy/jyotigpt-dashboard.log
    }
}
```

## SSL/TLS Certificates

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d dashboard.yourdomain.com

# Auto-renewal (already set up by certbot)
sudo certbot renew --dry-run
```

## Security Hardening

### 1. Firewall Configuration

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Deny direct access to port 5000
sudo ufw deny 5000/tcp
```

### 2. Rate Limiting (Nginx)

Add to your Nginx config:

```nginx
# Define rate limit zone
limit_req_zone $binary_remote_addr zone=dashboard_limit:10m rate=10r/s;

# Apply to location
location / {
    limit_req zone=dashboard_limit burst=20 nodelay;
    # ... rest of proxy config
}
```

### 3. Fail2Ban Protection

**Create filter:** `/etc/fail2ban/filter.d/jyotigpt-dashboard.conf`

```ini
[Definition]
failregex = ^.*Failed login attempt for username:.*$
ignoreregex =
```

**Create jail:** `/etc/fail2ban/jail.d/jyotigpt-dashboard.conf`

```ini
[jyotigpt-dashboard]
enabled = true
port = http,https
filter = jyotigpt-dashboard
logpath = /var/log/jyotigpt/error.log
maxretry = 5
bantime = 3600
findtime = 600
```

```bash
sudo systemctl restart fail2ban
```

## Monitoring and Logging

### Application Logs

```bash
# View live logs (systemd)
sudo journalctl -u jyotigpt-dashboard -f

# View live logs (Docker)
docker-compose logs -f

# Check error logs
tail -f /var/log/jyotigpt/error.log
```

### Health Checks

The application provides a health check endpoint:

```bash
# Check application health
curl http://localhost:5000/api/health
```

### Monitoring with Uptime Kuma

1. Add the health check endpoint to Uptime Kuma
2. Monitor: `https://dashboard.yourdomain.com/api/health`
3. Set appropriate check interval (e.g., 60 seconds)

## Backup Strategy

### 1. Environment Configuration

```bash
# Backup .env file (encrypted)
gpg -c .env
# Store .env.gpg securely
```

### 2. Application Files

```bash
# Create backup
tar -czf jyotigpt-dashboard-backup-$(date +%Y%m%d).tar.gz \
    /opt/jyotigpt-dashboard \
    --exclude=venv \
    --exclude=__pycache__

# Restore
tar -xzf jyotigpt-dashboard-backup-YYYYMMDD.tar.gz -C /
```

## Performance Tuning

### Gunicorn Workers

Calculate optimal workers:

```python
# Formula: (2 × CPU_CORES) + 1
# For 4 cores: (2 × 4) + 1 = 9 workers

gunicorn -w 9 -b 0.0.0.0:5000 app:app
```

### Connection Timeouts

For slow JyotiGPT/HF API responses:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 app:app
```

## Updating the Application

### Standard Update

```bash
cd /opt/jyotigpt-dashboard

# Backup current version
cp -r . ../jyotigpt-dashboard-backup

# Pull updates (if using git)
git pull

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart jyotigpt-dashboard
```

### Docker Update

```bash
# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Check Service Status

```bash
# Systemd
sudo systemctl status jyotigpt-dashboard

# Docker
docker-compose ps
docker logs jyotigpt-dashboard
```

### Port Already in Use

```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/jyotigpt-dashboard

# Fix permissions
chmod 755 /opt/jyotigpt-dashboard
chmod 600 /opt/jyotigpt-dashboard/.env
```

## Scaling

### Horizontal Scaling

Deploy multiple instances behind a load balancer:

```nginx
upstream dashboard_backend {
    least_conn;
    server 10.0.1.10:5000;
    server 10.0.1.11:5000;
    server 10.0.1.12:5000;
}

server {
    location / {
        proxy_pass http://dashboard_backend;
        # ... proxy settings
    }
}
```

### Database Session Store

For multiple instances, use Redis for sessions:

```python
# Install: pip install Flask-Session redis
from flask_session import Session
import redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

## Maintenance

### Regular Tasks

- **Weekly**: Review logs for errors
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Backup**: Daily automated backups

### Health Checklist

- [ ] Application responding (health endpoint)
- [ ] SSL certificate valid
- [ ] Logs rotating properly
- [ ] Disk space available
- [ ] Memory usage normal
- [ ] CPU usage normal
- [ ] Backups completing successfully

## Support

For production issues:
1. Check application logs
2. Review Nginx/Caddy logs
3. Verify environment variables
4. Test API endpoints manually
5. Check firewall rules

## Additional Resources

- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Best Practices](https://nginx.org/en/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
