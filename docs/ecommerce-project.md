# Safaa e-commerce project

The featured portfolio entry is at `/projects/safaa-ecommerce/`. Its presentation type is `ecommerce`, and its external URL is blank. All page calls to action open the Contact form, prefilled for this project with a demo or quote request. The rental project remains separate.

## Installation

```sh
python manage.py migrate
python manage.py seed_ecommerce_project
npm run build
python manage.py collectstatic --noinput
```

The seed is repeatable and preserves edited descriptions and images. It explicitly keeps the external URL blank. The dashboard project form includes the e-commerce presentation option.

The French/Arabic copy is adapted from the supplied e-commerce landing-page document. Safaa is described as a demonstration with sample content and public ordering disabled. Current COD operations, separate cash-remittance tracking, 48-hour unconfirmed stock reservations and shipment-time stock deductions are distinguished from future online payments, automated messaging, customer accounts and courier integrations.

The cream/brown/gold preview is an explicitly labeled CSS illustration, not a screenshot or live storefront. An uploaded project image can replace the portfolio illustration. No external demonstration is published or linked.
