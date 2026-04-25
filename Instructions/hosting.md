# DigiCode VPS Hosting Configuration

This guide covers deploying DigiCode on a Contabo VPS using **Caddy** as reverse proxy and **Gunicorn** as WSGI server.

## Prerequisites

```bash
# Create deployment directory
sudo mkdir -p /var/www/DigiCode
sudo chown -R $USER:$USER /var/www/DigiCode

# Create logs directory
sudo mkdir -p /var/www/DigiCode/logs
sudo chmod 755 /var/www/DigiCode/logs

# Create virtual environment
cd /var/www/DigiCode
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
python manage.py migrate
```

## Environment Variables (.env)

Create `/var/www/DigiCode/.env`:

```env
# Django
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-secure-secret-key-here
DEBUG=False

# Database
DATABASE_URL=sqlite:///var/www/DigiCode/db.sqlite3
# Or PostgreSQL: postgres://user:pass@localhost:5432/digicode

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Optional: Cloudflare or other CDN
# BEHIND_PROXY=True
```

## Gunicorn Service Configuration

Create `/etc/systemd/system/digicode.service`:

```ini
[Unit]
Description=Gunicorn daemon for DigiCode
After=network.target

[Service]
# Security: Run as non-root user (create this user first)
User=www-data
Group=www-data
WorkingDirectory=/var/www/DigiCode

# Create the user if it doesn't exist:
# sudo useradd -r -s /bin/false www-data
# sudo usermod -aG www-data $USER

# Load environment variables
EnvironmentFile=/var/www/DigiCode/.env

# Gunicorn process
ExecStart=/var/www/DigiCode/venv/bin/gunicorn \
          config.wsgi:application \
          --workers 3 \
          --worker-class sync \
          --bind 127.0.0.1:8000 \
          --access-logfile /var/www/DigiCode/logs/gunicorn-access.log \
          --error-logfile /var/www/DigiCode/logs/gunicorn-error.log \
          --log-level info \
          --timeout 120 \
          --keep-alive 2 \
          --max-requests 1000 \
          --max-requests-jitter 50

# Restart policy
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

**Note**: The WSGI module is `config.wsgi:application` (not `digicode.wsgi`), matching the project structure.

## Caddy Configuration

Create `/etc/caddy/Caddyfile`:

```
your-domain.com {
    # Enable logging
    log {
        output file /var/log/caddy/digicode-access.log
        format json
    }

    # Reverse proxy to Gunicorn
    reverse_proxy 127.0.0.1:8000 {
        # Health check
        health_uri /health/
        health_interval 30s
        health_timeout 5s
    }

    # Static files (served by Caddy directly for better performance)
    handle /static/* {
        root * /var/www/DigiCode
        file_server
        header Cache-Control "public, max-age=31536000, immutable"
    }

    # Media files
    handle /media/* {
        root * /var/www/DigiCode
        file_server
        header Cache-Control "public, max-age=86400"
    }

    # Security headers
    header {
        # Enable HSTS
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        # Prevent clickjacking
        X-Frame-Options "SAMEORIGIN"
        # XSS protection
        X-XSS-Protection "1; mode=block"
        # Content type sniffing
        X-Content-Type-Options "nosniff"
        # Referrer policy
        Referrer-Policy "strict-origin-when-cross-origin"
        # Permissions policy
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
    }

    # Compress responses
    encode gzip zstd

    # Handle 404s gracefully
    handle_errors {
        @404 {
            expression `{http.error.status_code} == 404`
        }
        rewrite @404 /404.html
    }
}
```

Replace `your-domain.com` with your actual domain name.

## Setup Commands

```bash
# 1. Reload systemd and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable digicode
sudo systemctl start digicode

# 2. Verify Gunicorn is running
sudo systemctl status digicode
sudo tail -f /var/www/DigiCode/logs/gunicorn-error.log

# 3. Reload Caddy configuration
sudo systemctl reload caddy
# Or if first time: sudo systemctl restart caddy

# 4. Verify Caddy is working
sudo systemctl status caddy
sudo tail -f /var/log/caddy/digicode-access.log
```

## SSL/HTTPS

Caddy automatically obtains and renews SSL certificates from Let's Encrypt. No additional configuration needed!

## Troubleshooting

### Check Gunicorn logs
```bash
sudo journalctl -u digicode -f
sudo tail -f /var/www/DigiCode/logs/gunicorn-error.log
```

### Check Caddy logs
```bash
sudo journalctl -u caddy -f
sudo tail -f /var/log/caddy/digicode-access.log
```

### Test Gunicorn directly
```bash
curl http://127.0.0.1:8000/
```

### Fix permissions
```bash
# Ensure www-data can read the project
sudo chown -R www-data:www-data /var/www/DigiCode
sudo chmod -R 755 /var/www/DigiCode/static
sudo chmod -R 755 /var/www/DigiCode/media
sudo chmod 644 /var/www/DigiCode/.env
```

### Database permissions (SQLite)
```bash
# If using SQLite
sudo chown www-data:www-data /var/www/DigiCode/db.sqlite3
sudo chmod 664 /var/www/DigiCode/db.sqlite3
sudo chown www-data:www-data /var/www/DigiCode
sudo chmod 775 /var/www/DigiCode
```

## Security Checklist

- [ ] Changed default admin password
- [ ] Set strong `SECRET_KEY` in `.env`
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] Running as non-root user (`www-data`)
- [ ] SSL certificates auto-renewing (Caddy handles this)
- [ ] Firewall configured (ufw or iptables)
- [ ] Regular backups set up for database and media files

## Updates/Redeployment

```bash
cd /var/www/DigiCode
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages

# Restart services
sudo systemctl restart digicode
sudo systemctl reload caddy
```
