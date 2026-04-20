# DigiCode Web Agency

A professional Django web agency website for Morocco with multilingual support (French + Arabic), showcasing website creation services.

## Features

- **Services Showcase**: Rental Cars, Used Cars Marketplace, E-commerce, Real Estate, Custom Business Websites
- **Multilingual**: French (LTR) and Arabic (RTL) support
- **WhatsApp Integration**: Direct contact via WhatsApp with dynamic messages
- **Dashboard**: Manage services, analytics, and content
- **SEO Optimized**: Meta tags, sitemap, canonical URLs
- **Modern UI**: Tailwind CSS with Alpine.js interactivity
- **Docker Deployment**: Production-ready with Docker Compose

## Tech Stack

- **Backend**: Django 5+
- **Frontend**: Django Templates + Tailwind CSS + Alpine.js
- **Database**: PostgreSQL
- **Cache**: Redis
- **Deployment**: Docker + Nginx + Gunicorn

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/digicode-webagency.git
   cd digicode-webagency
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Compile translations**:
   ```bash
   python manage.py compilemessages
   ```

8. **Start development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

### Default Credentials
- **Admin**: admin / admin123

### Docker Deployment

```bash
docker-compose up -d
```

## Project Structure

```
DigiCode/
├── apps/
│   ├── core/           # Core functionality, site settings
│   ├── services/       # Services management
│   ├── dashboard/      # Admin dashboard
│   ├── analytics/      # Tracking and analytics
│   └── users/          # User management
├── templates/          # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded files
├── locale/            # Translation files
├── config/            # Django configuration
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DEBUG` | Enable debug mode |
| `SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Comma-separated list of hosts |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `REDIS_URL` | Redis connection URL |
| `WHATSAPP_NUMBER` | Business WhatsApp number |

## Color Palette

- **Primary**: #0F172A (Dark Slate)
- **Accent**: #2563EB (Blue)
- **Highlight**: #F59E0B (Amber)
- **Background**: #F8FAFC (Light Gray)

## License

MIT License
