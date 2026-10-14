# CV-to-Portfolio service and examples

The bilingual service is available at `/services/cv-portfolio/`. The examples are single-page fictional personal websites with in-page navigation:

- Professional CV: `/demos/cv-professionnel/`; project `/projects/cv-professionnel/`.
- Creative portfolio: `/demos/portfolio-creatif/`; project `/projects/portfolio-creatif/`.

Both examples use the existing French/Arabic session switch, locally served Inter/Beiruti fonts and a separate stylesheet/script. The light professional profile and dark creative profile contain fictional names, organizations and experience. Concept work is original CSS artwork, explicitly labelled illustrative. No real personal contacts, testimonials or client claims appear. Actual screenshots in both languages supply the service and project previews.

Quotes use the existing contact route with `service`, `project` and `intent=quote` parameters. The editable brief names the example; valid submissions save the existing Inquiry with the selected Service. Contextual WhatsApp messages use the centrally normalized configured number. If WhatsApp is unavailable, its buttons are omitted. No CV upload is requested; CV sharing happens privately after discussion.

Delivery is static HTML/CSS/JS, with approved content, internal navigation and basic search metadata. Domain, hosting, publication and updates are agreed separately. The examples are rendered by Django for local demonstration; this phase does not implement automatic client exports, automatic conversion or a personal-site CMS.

## Setup on another environment

Run `venv/bin/python manage.py migrate`, then `venv/bin/python manage.py seed_cv_portfolio`, `npm run build`, and `venv/bin/python manage.py collectstatic --noinput`. The additive migration adds project presentation choices. The seed command preserves existing service/demo customizations and visibility; new demo projects are active and unfeatured, so the homepage slideshow selection is unchanged. Reserved slugs belonging to other projects are skipped and reported rather than overwritten. The service and demo visibility remain editable in the dashboard.

## Validation

46 core tests cover both languages, active/inactive routes and sitemap entries, internal anchors, quote prefills and encoded WhatsApp messages, valid/invalid inquiries, dashboard choices, repeatable setup and readable server HTML without JavaScript. Production build, static collection, Django checks and migration drift check pass. Browser validation covers both demos at 360, 390, 768, 1024 and 1440 px in French and Arabic. Mobile section links close the menu, focus the destination and update the active section; Escape returns focus to the menu toggle. Reduced motion disables entrances/transitions and prevents hiding reveal content; it is implemented through CSS/media-query handling, without a separate browser emulation run. Deployment is not part of this change.
