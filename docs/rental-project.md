# Rental project landing page

The portfolio project and `/services/lp/rental/` use the same French/Arabic sales presentation. The existing untitled rental entry was completed, preserving `/projects/project-1/`; new installations create `/projects/car-rental/`.

The external project link is `https://rental.digicode.ma/`. The entry is active and featured, and appears in the portfolio, homepage and project sitemap. Uploaded project images take precedence over the bundled, language-matched public screenshots.

## Installation

```sh
python manage.py migrate
python manage.py seed_rental_project
npm ci
npm run build
python manage.py collectstatic --noinput
```

The seed command reuses an untitled entry already linked to the rental domain or creates a new project. Repeated runs preserve edited descriptions, images and the existing slug. The dashboard’s project form exposes the presentation choice.

## Content and inquiries

The copy is adapted from the supplied Arabic project brief. The agency dashboard is described as French-only; the rental customer interface supports Arabic, French and English. Booking requests require agency confirmation. Pending requests retain dates until handled; no automatic expiry is promised. Pricing formulas include both pickup and return dates, with a separate deposit. Booking-value indicators are distinguished from collected payments and profit. Online payment and separate multi-agency accounts are explicitly outside the current version.

Demo/quote buttons open the existing contact form with an editable localized brief. WhatsApp links use DigiCode’s configured seller number and a rental-specific message. No messages are automatically sent.

The public screenshots were captured from the actual rental site on 13 October 2026. They are not fabricated fleet or administration images. The live fleet was empty at capture time; no private dashboard screenshot is included.
