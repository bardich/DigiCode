# Full Windsurf Prompt — Django Web Agency Website (Morocco)

## PROJECT OVERVIEW


### Tech Stack
- Backend: Django 5+
- Frontend: Django Templates
- CSS: Tailwind CSS
- Interactivity: Alpine.js
- Database: PostgreSQL
- Deployment: Docker + Nginx + Gunicorn
- Languages: Arabic + French (Multilingual)
- SEO Optimized
- Mobile First

---

## BUSINESS IDEA

The website promotes website creation services and showcases different types of websites:

- Rental Cars Website
- Used Cars Marketplace
- E-commerce Website
- Real Estate Website
- Custom Business Websites

Each service has a dedicated landing page with:
- Description
- Benefits
- YouTube video
- WhatsApp contact CTA

---

## DEVELOPMENT PHASES

### PHASE 1 — PROJECT INITIALIZATION

- Create virtual environment venv as a first step
- Setup Django project (modular)
- PostgreSQL config
- TailwindCSS integration
- Alpine.js setup
- Multilingual setup (FR + AR)
- Static/media config
- Docker setup
- Env variables

Structure:
project/
├── apps/
│   ├── core/
│   ├── services/
│   ├── dashboard/
│   ├── analytics/
│   └── users/
├── templates/
├── static/
├── media/
└── config/

---

### PHASE 2 — DATABASE MODELS

Service Model:
- title_fr
- title_ar
- slug
- short_description_fr
- short_description_ar
- full_description_fr
- full_description_ar
- benefits_fr
- benefits_ar
- youtube_url
- featured_image
- is_active
- created_at
- updated_at

---

### PHASE 3 — PUBLIC WEBSITE

Homepage:
- Hero Section
- Services Overview
- Featured Services
- Why Choose Us
- Process Section
- Testimonials
- Contact CTA
- WhatsApp Button

Services Page:
- Grid of services
- Multilingual content

Service Landing Page:
- Title
- Description
- Benefits
- YouTube Button
- WhatsApp CTA

---

### PHASE 4 — WHATSAPP SYSTEM

Dynamic WhatsApp message:
"Hello, I'm interested in your [Service Name] service. Please send me more details."

---

### PHASE 5 — DASHBOARD

- Manage services
- Add/Edit/Delete
- Manage FR/AR content
- Add YouTube link
- Toggle active status

---

### PHASE 6 — ANALYTICS

- Service views
- Popular services
- Click tracking

---

### PHASE 7 — SEO

- Multilingual SEO
- Meta tags
- Sitemap
- Canonical URLs

---

### PHASE 8 — MULTILINGUAL ( Use Django i18n + django-modeltranslation )

- Arabic RTL
- French LTR
- Language switcher

---

### PHASE 9 — UI/UX

Style:
- Clean agency look
- Strong CTA
- Smooth animations

Palette:
- Primary: #0F172A
- Accent: #2563EB
- Highlight: #F59E0B
- Background: #F8FAFC

---

### PHASE 10 — PRODUCTION

- Secure settings
- Logging
- Error pages
- Optimization
- Docker deployment

---

## FINAL OUTPUT

Build step-by-step, explain each phase, show file changes, wait confirmation.

---


