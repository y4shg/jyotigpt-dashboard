# JyotiGPT Command Center Dashboard

A production-ready Flask dashboard for managing JyotiGPT services, with authentication, JyotiGPT analytics integration, and HuggingFace Spaces management.

## Features

- 🔐 **Secure Authentication** - Flask-Login with password hashing
- 📊 **JyotiGPT Analytics** - Real-time usage statistics and model performance
- 🚀 **HuggingFace Spaces Management** - Monitor and control your Spaces
- 🔗 **Service Links** - Quick access to all AI and internal services
- 📡 **Uptime Monitoring** - Embedded Uptime Kuma status
- 🎨 **Cyberpunk UI** - Modern, responsive design
- 🔒 **Production Ready** - Session management, CSRF protection, secure cookies

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Active JyotiGPT instance with admin access
- HuggingFace account with API token (optional)
- Uptime Kuma instance (optional)

## Installation

### 1. Clone or download the project

```bash
cd jyotigpt-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-generate-with-python-secrets
FLASK_ENV=production
PORT=5000

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password-here

# JyotiGPT Configuration
JYOTIGPT_URL=https://your-jyotigpt-instance.com
JYOTIGPT_ADMIN_TOKEN=your-admin-bearer-token

# HuggingFace Configuration (optional)
HF_TOKEN=hf_your_token_here
HF_SPACE_IDS=username/space1,username/space2
```

### 6. Generate a secure secret key

```python
import secrets
print(secrets.token_hex(32))
```

Use this value for `SECRET_KEY` in your `.env` file.

## Running the Application

### Development Mode

```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`

### Production Mode

It's recommended to use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with more options:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - app:app
```

## Configuration

### JyotiGPT Setup

1. Log in to your JyotiGPT instance as admin
2. Navigate to Settings > Account
3. Generate an API token
4. Copy the token and add it to your `.env` file as `JYOTIGPT_ADMIN_TOKEN`

### HuggingFace Spaces Setup

1. Go to https://huggingface.co/settings/tokens
2. Create a new token with `read` and `write` access
3. Add the token to your `.env` file as `HF_TOKEN`
4. List your space IDs (format: `username/space-name`) in `HF_SPACE_IDS`, separated by commas

### Uptime Kuma Setup

The dashboard embeds your Uptime Kuma status page. Make sure:
- Your Uptime Kuma instance is publicly accessible
- The status page is enabled in Uptime Kuma settings
- Update the iframe URL in `templates/dashboard.html` if needed

## Security Considerations

### Production Deployment Checklist

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Use a strong, random `SECRET_KEY`
- [ ] Use a strong admin password
- [ ] Enable HTTPS (use nginx or Caddy as reverse proxy)
- [ ] Set `SESSION_COOKIE_SECURE=True` when using HTTPS
- [ ] Restrict access using firewall rules
- [ ] Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- [ ] Set up regular backups
- [ ] Monitor application logs
- [ ] Use environment variables for all secrets (never commit `.env`)

### Nginx Reverse Proxy Example

```nginx
server {
    listen 80;
    server_name dashboard.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using with Systemd

Create `/etc/systemd/system/jyotigpt-dashboard.service`:

```ini
[Unit]
Description=JyotiGPT Dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/jyotigpt-dashboard
Environment="PATH=/path/to/jyotigpt-dashboard/venv/bin"
ExecStart=/path/to/jyotigpt-dashboard/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable jyotigpt-dashboard
sudo systemctl start jyotigpt-dashboard
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Submit login credentials
- `GET /logout` - Logout and clear session

### Dashboard
- `GET /dashboard` - Main dashboard (requires authentication)

### JyotiGPT API
- `GET /api/jyotigpt/summary` - Get analytics summary
- `GET /api/jyotigpt/models` - Get model usage data
- `GET /api/jyotigpt/users` - Get user activity data

### HuggingFace API
- `GET /api/hf/spaces` - List configured spaces with status
- `POST /api/hf/space/<space_id>/restart` - Restart a space
- `POST /api/hf/space/<space_id>/pause` - Pause a space

### Utility
- `GET /api/health` - Health check endpoint

## Troubleshooting

### Cannot connect to JyotiGPT

- Verify `JYOTIGPT_URL` is correct (include `https://`)
- Ensure `JYOTIGPT_ADMIN_TOKEN` is valid
- Check if your JyotiGPT instance is accessible from the dashboard server
- Review JyotiGPT logs for authentication errors

### Cannot manage HuggingFace Spaces

- Verify `HF_TOKEN` has correct permissions
- Ensure `HF_SPACE_IDS` format is correct (`username/space-name`)
- Check HuggingFace API status
- Verify spaces exist and you have access

### Session expires quickly

- Increase `PERMANENT_SESSION_LIFETIME` in `app.py`
- Make sure cookies are enabled in your browser
- Check if `SECRET_KEY` changes between restarts

### Dashboard not loading

- Check application logs: `gunicorn --log-level debug -w 1 -b 0.0.0.0:5000 app:app`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure port 5000 is not in use: `lsof -i :5000`

## Project Structure

```
jyotigpt-dashboard/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your actual environment variables (not in git)
├── README.md              # This file
├── templates/
│   ├── login.html         # Login page
│   ├── dashboard.html     # Main dashboard
│   └── error.html         # Error pages
└── static/                # Static files (if needed)
```

## Customization

### Adding More Services

Edit `templates/dashboard.html` and add new service links in the AI Services or Internal Services cards.

### Changing the Theme

Modify CSS variables in the `<style>` sections of the templates:

```css
:root {
    --bg-primary: #0a0e27;     /* Main background */
    --accent-cyan: #00fff9;     /* Primary accent */
    --accent-magenta: #ff00ff;  /* Secondary accent */
    /* ... other variables */
}
```

### Adding Users

Currently, the app supports a single admin user. To add more users, modify the `USERS` dictionary in `app.py` or implement a database backend.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for personal and commercial use.

## Support

For issues and questions, please check the troubleshooting section first.

## Changelog

### Version 1.0.0
- Initial release
- Flask authentication system
- JyotiGPT analytics integration
- HuggingFace Spaces management
- Responsive dashboard UI
- Production-ready configuration
