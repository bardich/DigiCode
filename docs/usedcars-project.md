# AutoMaroc dealership project

The supplied `Complete usedcars Sales landig page.md` is used as content reference for equivalent French and Arabic copy. Its content-only instruction does not replace the user's explicit request to implement a project landing page.

- Project: `/projects/automaroc-usedcars/`, featured on the homepage and listed in the portfolio and sitemap while active.
- External website: `https://cars.digicode.ma/`.
- Existing URL preserved: `/services/lp/usedcars/` renders the same bilingual presentation.
- Purchase CTA: localized WhatsApp message using the configured SiteSettings number; contact form fallback when no valid number is configured.
- Screenshots: real public homepage captures in French and Arabic. The live demonstration currently has an empty inventory; no vehicle listings or private dashboard images have been fabricated.
- Offer: one dealership, one-time purchase with installation, initial branding/setup and training. Hosting and ongoing support are separately agreed. No public price or invented delivery commitment.
- Favorites/comparison live on the visitor's device; vehicle descriptions are entered by staff; inquiry inbox is not a full CRM; operational statistics are estimates, not verified revenue.

## Setup on another environment

Run `venv/bin/python manage.py migrate`, then `venv/bin/python manage.py seed_usedcars_project`. The seed command is repeatable, preserves existing project descriptions, slugs and images, and leaves other projects intact. It sets AutoMaroc's landing type, active/featured flags and requested external link. Run `npm run build` and `venv/bin/python manage.py collectstatic --noinput` for static assets.

## Verification

37 core tests passed, including five AutoMaroc tests for repeatable setup, bilingual content, configured contextual WhatsApp URLs, fallback contact and active/inactive visibility. Django checks, migration drift check, CSS build and static collection passed. Browser checks covered both languages at 360, 390, 768, 1024 and 1440 pixels without horizontal overflow, with loaded preview images. Body copy remains 18 px French / 20 px Arabic on desktop, and 16 px / 18 px on mobile. The existing Beiruti font and shared reduced-motion styles are preserved. No deployment was performed.
