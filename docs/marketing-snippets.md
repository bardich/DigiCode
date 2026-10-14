# Marketing snippets and visitor choice

Superusers can manage snippets at `/dashboard/marketing/`, with separate creation, edit, delete-confirmation, enable/disable and global-switch controls. Ordinary staff cannot access these endpoints or their Django admin equivalents. The ordinary settings screen cannot change the global switch. The existing Google Analytics ID is retained as an inactive legacy value.

## Installation

1. Paste a complete platform-provided fragment, including `<script>` tags, into a named snippet. Code is displayed as escaped text in the editor and is never executed there.
2. Choose `head` or `body_start`, then set its display order. For a platform that supplies two positions, create two records.
3. Save, then explicitly enable the snippet and global loading. New snippets and the global switch default to disabled.
4. Test on a staging agency page with the platform's own verification tools after accepting optional tracking.

Supported markup is script tags, comments, whitespace and optional noscript blocks containing image/iframe fallbacks. Each snippet is limited to 50 KiB of UTF-8 text. Plain JavaScript without tags, document wrappers, arbitrary HTML, event-handler attributes, unsupported script types and document.write()/writeln() fragments are rejected. Snippet code is trusted executable code managed by superusers: validation is not a JavaScript security audit. Noscript fallbacks are retained in storage but never emitted as active elements; with JavaScript disabled, optional tracking stays unloaded.

Avoid installing the same platform both directly and through Google Tag Manager. No conversion-event configuration, form-value serialization, server-side tracking or campaign management is included.

## Public behavior

Only the named agency routes for Home, About, Contact, Services (including specialist pages) and Projects receive inert JSON configuration and the local loader. Dashboard/login routes, CV demo routes, error templates and non-HTML endpoints do not load it. No vendor preconnects, scripts, pixels or iframes are emitted before acceptance.

The French/Arabic banner offers equal accept-all/reject-all buttons. A footer control reopens it. A local-storage record (`digicode.marketing-consent.v1`) holds the choice, active-configuration fingerprint and 180-day expiry. Unknown, expired, malformed or mismatched preferences default to no loading. If storage is blocked, an explicit choice applies only to the current page.

Changes to enabled membership, pasted code, placement or order change the fingerprint and require a new choice. Renaming a record or editing a disabled record does not. Global disable suppresses both configuration and loader on subsequent page loads; it does not unload a vendor from an already-open page.

After acceptance, scripts are inserted in configured order. Non-async external scripts are awaited before subsequent initialization; explicitly async scripts retain their own async behavior. A failed or stalled external script does not block the website; after eight seconds, subsequent snippets may proceed. If a stalled vendor eventually loads, strict dependency timing can no longer be guaranteed, so vendor-specific integration verification remains necessary. No automatic retries occur.

Rejecting after activation persists rejection and reloads the page. This removes this integration's scripts from the new document; it cannot retract already transmitted data or universally remove vendor cookies. The banner is not a legal-compliance certification or a third-party consent platform.

## Setup and checks

Apply the additive migration using `venv/bin/python manage.py migrate`. Run `npm run build` and `venv/bin/python manage.py collectstatic --noinput`. The migration installs no vendor code and keeps global loading disabled. Existing data is preserved.

Validation commands:

- `venv/bin/python manage.py test apps.core` — public route coverage, permission checks, forms, CSRF, ordering, fingerprint changes, disabled defaults, admin protections and existing website behavior.
- `node tests/marketing-consent.test.cjs` — 11 behavioral tests running the real loader against a fake DOM and mocked vendors, without real network calls.
- `venv/bin/python manage.py check` and `venv/bin/python manage.py makemigrations --check --dry-run`.

Browser validation uses an isolated SQLite database under `/tmp`, a localhost-only QA user middleware, and harmless local scripts. It verifies no load before consent, one execution per accepted page, dependency ordering, inactive noscript pixels, rejection/reload, no scripts in the dashboard, and French/Arabic banner layouts at 360, 390, 768, 1024 and 1440 px. The normal website database remains empty of marketing snippets and globally disabled. Real integrations and deployment are separate steps.
