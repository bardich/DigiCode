from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.template.loader import get_template, render_to_string
from .models import Inquiry, Project, SiteSettings
from .utils import whatsapp_url
from apps.services.models import Service

# Tracking is unrelated to these assertions and writes in background threads.
TEST_MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.core.middleware.LanguageMiddleware',
]


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class RedesignTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.settings = SiteSettings.objects.create()
        cls.service = Service.objects.create(title_fr='Site sur mesure', title_ar='موقع مخصص', slug='custom', short_description_fr='Votre activité en ligne', short_description_ar='نشاطك الرقمي', full_description_fr='Un site adapté à vos objectifs.', full_description_ar='موقع يناسب أهدافك.', benefits_fr=['Responsive'], benefits_ar=['متجاوب'])
        cls.project = Project.objects.create(title_fr='Projet public', title_ar='مشروع عام', slug='public', full_description_fr='<script>alert(1)</script>', is_featured=True)
        cls.hidden = Project.objects.create(title_fr='Projet privé', slug='private', is_active=False, is_featured=True)
        cls.user = get_user_model().objects.create_user(username='editor', password='test-password')

    def payload(self, **changes):
        data = {'name': 'Test Client', 'email': 'client@example.com', 'brief': 'Nous souhaitons créer un site pour notre entreprise.', 'service': str(self.service.pk)}
        data.update(changes)
        return data

    def test_all_public_pages_in_both_languages(self):
        paths = ['/', '/about/', '/contact/', '/services/', '/projects/', self.project.get_absolute_url(), self.service.get_absolute_url(), '/services/lp/rental/', '/services/lp/usedcars/', '/services/lp/artisana/']
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for path in paths:
                with self.subTest(lang=lang, path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, f'lang="{lang}"')
                    self.assertNotContains(response, 'cdn.tailwindcss.com')
                    self.assertNotContains(response, 'DH')
                    self.assertNotContains(response, '&lt;br&gt;')

    def test_visibility_empty_states_and_missing_image(self):
        home = self.client.get('/')
        self.assertContains(home, 'Projet public')
        self.assertNotContains(home, 'Projet privé')
        self.assertContains(home, 'Aperçu à venir')
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)
        Project.objects.update(is_active=False)
        self.assertNotContains(self.client.get('/'), 'Une sélection de nos projets')
        self.assertContains(self.client.get('/projects/'), 'Nos projets arrivent ici bientôt.')

    def test_project_detail_escapes_untrusted_content(self):
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')

    def test_service_preselection_and_inactive_rejection(self):
        response = self.client.get('/contact/?service=custom')
        self.assertEqual(response.context['form']['service'].value(), self.service.pk)
        self.service.is_active = False
        self.service.save()
        self.assertEqual(self.client.post('/contact/', self.payload()).status_code, 400)
        self.assertFalse(Inquiry.objects.exists())

    def test_inquiry_saved_and_confirmation_is_one_time(self):
        self.client.get('/set-language/ar/')
        response = self.client.post('/contact/', self.payload(), HTTP_REFERER='http://testserver/services/custom/')
        self.assertEqual(response.status_code, 302)
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.language, 'ar')
        self.assertEqual(inquiry.source_page, '/services/custom/')
        self.assertContains(self.client.get('/contact/'), 'تم استلام الطلب')
        self.assertNotContains(self.client.get('/contact/'), 'تم استلام الطلب')

    def test_invalid_payload_preserves_values_and_localizes(self):
        self.client.get('/set-language/ar/')
        response = self.client.post('/contact/', self.payload(email='invalid', brief='short'))
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Test Client', status_code=400)
        self.assertContains(response, 'أدخل بريداً إلكترونياً صالحاً.', status_code=400)
        self.assertFalse(Inquiry.objects.exists())

    def test_honeypot_and_csrf(self):
        self.assertEqual(self.client.post('/contact/', self.payload(website='spam')).status_code, 400)
        self.assertFalse(Inquiry.objects.exists())
        csrf_client = Client(enforce_csrf_checks=True)
        self.assertEqual(csrf_client.post('/contact/', self.payload()).status_code, 403)
        csrf_client.get('/contact/')
        data = self.payload(csrfmiddlewaretoken=csrf_client.cookies['csrftoken'].value)
        self.assertEqual(csrf_client.post('/contact/', data).status_code, 302)

    def test_rate_limits_session_and_email(self):
        self.assertEqual(self.client.post('/contact/', self.payload()).status_code, 302)
        self.assertEqual(self.client.post('/contact/', self.payload(email='other@example.com')).status_code, 429)
        for i in range(2):
            self.assertEqual(Client().post('/contact/', self.payload()).status_code, 302)
        self.assertEqual(Client().post('/contact/', self.payload(email='CLIENT@example.com')).status_code, 429)
        self.assertEqual(Inquiry.objects.count(), 3)
        Inquiry.objects.update(created_at=timezone.now()-timedelta(minutes=16))
        self.assertEqual(Client().post('/contact/', self.payload()).status_code, 302)

    def test_dashboard_permissions_and_status(self):
        inquiry = Inquiry.objects.create(name='Client', email='client@example.com', brief='A project brief.', language='fr')
        detail = reverse('dashboard:inquiry_detail', args=[inquiry.pk])
        self.assertEqual(self.client.get('/dashboard/inquiries/').status_code, 302)
        self.assertEqual(self.client.post(detail, {'status': 'closed'}).status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.status, 'new')
        self.client.force_login(self.user)
        self.assertContains(self.client.get('/dashboard/inquiries/'), 'client@example.com')
        self.assertEqual(self.client.get(detail).status_code, 200)
        self.assertEqual(self.client.post(detail, {'status': 'invalid'}).status_code, 200)
        self.assertEqual(self.client.post(detail, {'status': 'contacted'}).status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.status, 'contacted')

    def test_dashboard_pages_and_additional_fields(self):
        self.client.force_login(self.user)
        for path in ['/dashboard/', '/dashboard/settings/', '/dashboard/services/', '/dashboard/projects/', '/dashboard/projects/create/', f'/dashboard/projects/{self.project.pk}/edit/', f'/dashboard/services/{self.service.pk}/edit/']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        form = self.client.get(f'/dashboard/projects/{self.project.pk}/edit/').context['form']
        self.assertIn('is_featured', form.fields)
        self.assertIn('display_order', form.fields)

    def test_settings_home_copy(self):
        self.client.force_login(self.user)
        self.client.post('/dashboard/settings/', {'home_heading_fr': 'Une nouvelle vision', 'home_heading_ar': 'رؤية جديدة'})
        self.assertContains(self.client.get('/'), 'Une nouvelle vision')
        self.client.get('/set-language/ar/')
        self.assertContains(self.client.get('/'), 'رؤية جديدة')

    def test_sitemap_active_projects_and_safe_language_redirect(self):
        response = self.client.get('/sitemap.xml')
        self.assertContains(response, self.project.get_absolute_url())
        self.assertNotContains(response, self.hidden.get_absolute_url())
        response = self.client.get('/set-language/ar/', HTTP_REFERER='https://untrusted.example/')
        self.assertEqual(response.url, '/')

    def test_whatsapp_normalization(self):
        self.assertEqual(whatsapp_url('+212 600-123-456', 'Bonjour & مرحباً'), 'https://wa.me/212600123456?text=Bonjour+%26+%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D9%8B')
        self.assertEqual(whatsapp_url('00212600123456'), 'https://wa.me/212600123456')
        self.assertEqual(whatsapp_url(''), '')

    def test_error_templates_render(self):
        for name in ['404.html', '500.html']:
            self.assertIn('DigiCode', render_to_string(name, {'CURRENT_LANGUAGE':'fr'}))

    def test_specialist_pages_have_consistent_language(self):
        titles = {'rental': ('Site de location de voitures', 'موقع تأجير السيارات'),
                  'usedcars': ('Site de vente de voitures d’occasion', 'موقع بيع السيارات المستعملة'),
                  'artisana': ('Boutique en ligne pour les artisans', 'متجر إلكتروني للحرفيين')}
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for slug, (fr, ar) in titles.items():
                with self.subTest(language=lang, page=slug):
                    response = self.client.get(f'/services/lp/{slug}/')
                    self.assertContains(response, fr if lang == 'fr' else ar)
                    self.assertNotContains(response, ar if lang == 'fr' else fr)
                    self.assertContains(response, 'dir="ltr"' if lang == 'fr' else 'dir="rtl"')
                    cta = ('Demander une démonstration' if lang == 'fr' else 'اطلب عرضاً توضيحياً') if slug == 'rental' else ('Démarrer mon projet' if lang == 'fr' else 'ابدأ مشروعي')
                    if slug == 'usedcars':
                        cta = 'Demander un devis' if lang == 'fr' else 'اطلب عرض سعر'
                    self.assertContains(response, cta)
                    self.assertNotContains(response, 'En Vedette')
                    self.assertNotContains(response, 'real-time')
                    if lang == 'ar':
                        self.assertContains(response, 'fonts/beiruti-arabic.woff2')
                    else:
                        self.assertNotContains(response, 'fonts/beiruti-arabic.woff2')

    def test_missing_translations_do_not_leak_another_language(self):
        from django.utils.translation import override
        service = Service(title_fr='French-only title', short_description_fr='French-only summary', full_description_fr='French-only details', benefits_fr=['French-only benefit'])
        project = Project(title_fr='French-only project', short_description_fr='French-only summary', full_description_fr='French-only details')
        with override('ar'):
            for obj in [service, project]:
                for method in ['get_title', 'get_short_description', 'get_full_description']:
                    self.assertNotIn('French-only', getattr(obj, method)())
                    self.assertTrue(getattr(obj, method)())
            self.assertEqual(service.get_benefits(), [])
            self.assertNotIn('French-only', service.get_whatsapp_message())
        service = Service(title_ar='عنوان عربي', short_description_ar='وصف عربي', full_description_ar='تفاصيل عربية')
        project = Project(title_ar='عنوان عربي', short_description_ar='وصف عربي', full_description_ar='تفاصيل عربية')
        with override('fr'):
            for obj in [service, project]:
                for method in ['get_title', 'get_short_description', 'get_full_description']:
                    self.assertNotIn('عربي', getattr(obj, method)())
                    self.assertTrue(getattr(obj, method)())

    def test_arabic_font_is_beiruti_in_public_and_login(self):
        from pathlib import Path
        from django.conf import settings
        self.client.get('/set-language/ar/')
        for path in ['/', '/contact/', '/dashboard/login/']:
            self.assertContains(self.client.get(path), 'fonts/beiruti-arabic.woff2')
        css = (settings.BASE_DIR / 'static/css/site.css').read_text()
        self.assertIn('font-family:Beiruti', css)
        self.assertNotIn('Noto Sans Arabic', css)
        self.assertTrue((settings.BASE_DIR / 'static/fonts/beiruti-arabic.woff2').exists())

    def test_project_without_slug_does_not_break_gallery(self):
        Project.objects.filter(pk=self.project.pk).update(slug='')
        self.project.refresh_from_db()
        self.assertEqual(self.project.get_absolute_url(), reverse('core:project_list'))
        self.assertEqual(self.client.get('/projects/').status_code, 200)
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_untitled_projects_receive_unique_slugs(self):
        first = Project.objects.create()
        second = Project.objects.create()
        self.assertTrue(first.slug)
        self.assertTrue(second.slug)
        self.assertNotEqual(first.slug, second.slug)
        self.assertEqual(self.client.get(first.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(second.get_absolute_url()).status_code, 200)

    def test_save_with_update_fields_repairs_legacy_slug(self):
        Project.objects.filter(pk=self.project.pk).update(slug='', title_fr='', title_ar='')
        self.project.refresh_from_db()
        self.project.save(update_fields=['is_active'])
        self.project.refresh_from_db()
        self.assertEqual(self.project.slug, f'project-{self.project.pk}')
        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 200)

    def test_data_migration_backfills_slug_and_handles_collisions(self):
        from importlib import import_module
        from django.apps import apps
        from django.db import connection
        from types import SimpleNamespace
        migration = import_module('apps.core.migrations.0012_backfill_project_slugs')
        collision = Project.objects.create(title_fr='Collision', slug='existing')
        Project.objects.filter(pk=self.project.pk).update(slug='', title_fr='Existing', title_ar='')
        migration.backfill_project_slugs(apps, SimpleNamespace(connection=connection))
        self.project.refresh_from_db()
        self.assertEqual(self.project.slug, 'existing-1')
        collision.refresh_from_db()
        self.assertEqual(collision.slug, 'existing')
        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 200)
        Project.objects.filter(pk=self.project.pk).update(slug='', title_fr='', title_ar='')
        migration.backfill_project_slugs(apps, SimpleNamespace(connection=connection))
        self.project.refresh_from_db()
        self.assertEqual(self.project.slug, f'project-{self.project.pk}')


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class RentalProjectTests(TestCase):
    def setUp(self):
        SiteSettings.objects.create(whatsapp_number='+212 600-123-456')

    def seed(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_rental_project', stdout=StringIO())
        return Project.objects.get(landing_page='car_rental')

    def test_seed_reuses_legacy_entry_and_is_repeatable(self):
        legacy = Project.objects.create(slug='project-1', link='https://rental.digicode.ma/')
        project = self.seed()
        self.assertEqual(project.pk, legacy.pk)
        self.assertEqual(project.slug, 'project-1')
        self.assertEqual(project.link, 'https://rental.digicode.ma/')
        self.assertTrue(project.is_active and project.is_featured)
        self.assertTrue(project.title_ar and project.title_fr)
        project.title_fr = 'Titre édité par le propriétaire'
        project.save()
        self.assertEqual(self.seed().title_fr, 'Titre édité par le propriétaire')
        self.assertEqual(Project.objects.count(), 1)

    def test_seed_creates_new_project_without_replacing_named_project(self):
        original = Project.objects.create(title_fr='Un autre projet', link='https://rental.digicode.ma/')
        project = self.seed()
        self.assertNotEqual(original.pk, project.pk)
        self.assertEqual(project.slug, 'car-rental')
        self.assertEqual(Project.objects.count(), 2)

    def test_project_gallery_home_and_sitemap_include_rental(self):
        project = self.seed()
        self.assertContains(self.client.get('/projects/'), project.get_absolute_url())
        self.assertContains(self.client.get('/'), project.get_absolute_url())
        self.assertContains(self.client.get('/sitemap.xml'), project.get_absolute_url())
        self.assertContains(self.client.get('/projects/'), 'images/rental-public-fr.png')

    def test_bilingual_landing_and_accurate_scope(self):
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for path in [project.get_absolute_url(), '/services/lp/rental/']:
                with self.subTest(lang=lang, path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, 'core/project_rental.html')
                    self.assertContains(response, 'https://rental.digicode.ma/')
                    self.assertContains(response, f'images/rental-public-{lang}.png')
                    self.assertContains(response, '7 à 29 jours' if lang == 'fr' else 'من 7 إلى 29 يوماً')
                    self.assertContains(response, 'Le paiement en ligne n’est pas disponible' if lang == 'fr' else 'الدفع الإلكتروني غير موجود')
                    self.assertContains(response, 'sans expiration automatique' if lang == 'fr' else 'دون انتهاء تلقائي')
                    self.assertContains(response, 'pas les paiements encaissés ni les bénéfices' if lang == 'fr' else 'ليست مدفوعات محصلة أو أرباحاً')
                    self.assertContains(response, 'https://wa.me/212600123456?text=')
                    self.assertContains(response, f'project={project.slug}&amp;intent=demo')
                    self.assertNotContains(response, 'GPS')

    def test_inactive_project_is_not_published(self):
        project = self.seed()
        project.is_active = False
        project.save()
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get('/projects/'), project.get_absolute_url())

    def test_demo_and_quote_prefill_and_successful_submission(self):
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for intent in ['demo', 'quote']:
                response = self.client.get(f'/contact/?project={project.slug}&intent={intent}')
                brief = response.context['form']['brief'].value()
                self.assertIn(project.get_title(), brief)
                self.assertIn('Je souhaite' if lang == 'fr' else 'أرغب', brief)
        response = self.client.post('/contact/', {'name':'Owner', 'email':'owner@example.com', 'brief': brief + ' Agence de Casablanca.'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('أرغب', Inquiry.objects.get().brief)
        project.is_active = False
        project.save()
        response = self.client.get(f'/contact/?project={project.slug}&intent=demo')
        self.assertIsNone(response.context['form']['brief'].value())


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class EcommerceProjectTests(TestCase):
    def setUp(self):
        SiteSettings.objects.create()

    def seed(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_ecommerce_project', stdout=StringIO())
        return Project.objects.get(landing_page='ecommerce')

    def test_seed_adds_separate_project_without_external_link(self):
        rental = Project.objects.create(title_fr='Location', slug='rental-existing', landing_page='car_rental', link='https://rental.digicode.ma/')
        project = self.seed()
        self.assertEqual(project.slug, 'safaa-ecommerce')
        self.assertEqual(project.link, '')
        self.assertTrue(project.is_active and project.is_featured)
        self.assertTrue(project.title_ar and project.title_fr)
        rental.refresh_from_db()
        self.assertEqual(rental.link, 'https://rental.digicode.ma/')
        self.assertEqual(Project.objects.count(), 2)
        project.title_fr = 'Safaa, titre personnalisé'
        project.short_description_ar = 'وصف معدل'
        project.save()
        again = self.seed()
        self.assertEqual(again.title_fr, 'Safaa, titre personnalisé')
        self.assertEqual(again.short_description_ar, 'وصف معدل')
        self.assertEqual(Project.objects.count(), 2)

    def test_bilingual_page_explains_demo_and_future_features(self):
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            response = self.client.get(project.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'core/project_ecommerce.html')
            self.assertContains(response, 'Les commandes publiques sont désactivées' if lang == 'fr' else 'الطلبات العامة معطلة')
            self.assertContains(response, 'expiration après 48 heures' if lang == 'fr' else 'تنتهي بعد 48 ساعة')
            self.assertContains(response, ('le stock physique est déduit à l’expédition' if lang == 'fr' else 'يُخصم المخزون الفعلي عند الشحن'))
            self.assertContains(response, 'ne font pas partie de la première version' if lang == 'fr' else 'ليست ضمن النسخة الأولى')
            self.assertContains(response, 'Composition illustrative' if lang == 'fr' else 'تكوين توضيحي')
            self.assertContains(response, 'Un seul code par commande' if lang == 'fr' else 'رمز واحد لكل طلب')
            self.assertContains(response, ('Démonstration, pas boutique en activité' if lang == 'fr' else 'عرض تجريبي وليس متجراً نشطاً'))
            self.assertNotContains(response, 'rental.digicode.ma')
            self.assertNotContains(response, 'Visiter le site')
            self.assertNotContains(response, 'rental-public-')
            self.assertNotContains(response, '37 backend')

    def test_all_project_calls_to_action_use_contact(self):
        from html.parser import HTMLParser
        class MainLinks(HTMLParser):
            in_main = False
            links = []
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'main':
                    self.in_main = True
                if tag == 'a' and self.in_main:
                    self.links.append(attrs.get('href'))
            def handle_endtag(self, tag):
                if tag == 'main':
                    self.in_main = False
        project = self.seed()
        response = self.client.get(project.get_absolute_url())
        parser = MainLinks()
        parser.feed(response.content.decode())
        self.assertGreaterEqual(len(parser.links), 6)
        for link in parser.links:
            self.assertTrue(link.startswith('/contact/?project=safaa-ecommerce&intent='), link)
            self.assertTrue(link.endswith('#project-form'), link)

    def test_portfolio_home_and_sitemap_show_project(self):
        project = self.seed()
        for path in ['/', '/projects/', '/sitemap.xml']:
            self.assertContains(self.client.get(path), project.get_absolute_url())
        self.assertContains(self.client.get('/projects/'), 'Composition illustrative')
        project.is_active = False
        project.save()
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get('/projects/'), project.get_absolute_url())

    def test_demo_and_quote_contact_briefs_match_each_language(self):
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for intent in ['demo', 'quote']:
                response = self.client.get(f'/contact/?project={project.slug}&intent={intent}')
                brief = response.context['form']['brief'].value()
                self.assertIn(project.get_title(), brief)
                self.assertIn('Je souhaite' if lang == 'fr' else 'أرغب', brief)
                self.assertIn('Mon entreprise' if lang == 'fr' else 'نشاطي', brief)
        response = self.client.post('/contact/', {'name':'Merchant', 'email':'merchant@example.com', 'brief':brief + ' متجر للمنتجات الطبيعية.'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('صفاء', Inquiry.objects.get().brief)


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class UsedCarsProjectTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.settings = SiteSettings.objects.create(whatsapp_number='+212 682-868-549')

    def tearDown(self):
        from django.core.cache import cache
        cache.clear()

    def seed(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_usedcars_project', stdout=StringIO())
        return Project.objects.get(landing_page='used_cars')

    def test_seed_preserves_other_projects_and_custom_content(self):
        previous = Project.objects.create(title_fr='Safaa', landing_page='ecommerce', link='')
        project = self.seed()
        self.assertEqual(project.link, 'https://cars.digicode.ma/')
        self.assertTrue(project.title_ar and project.title_fr and project.is_featured)
        project.title_fr = 'Mon titre'
        project.full_description_ar = 'وصف مخصص'
        project.save()
        again = self.seed()
        self.assertEqual(again.pk, project.pk)
        self.assertEqual(again.title_fr, 'Mon titre')
        self.assertEqual(again.full_description_ar, 'وصف مخصص')
        self.assertEqual(Project.objects.count(), 2)
        previous.refresh_from_db()
        self.assertEqual(previous.link, '')

    def test_complete_bilingual_page_and_existing_route(self):
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            for path in [project.get_absolute_url(), '/services/lp/usedcars/']:
                response = self.client.get(path)
                self.assertTemplateUsed(response, 'core/project_usedcars.html')
                self.assertContains(response, 'Achat unique' if lang == 'fr' else 'شراء لمرة واحدة')
                self.assertContains(response, 'jusqu’à 15 photos' if lang == 'fr' else 'حتى 15 صورة')
                self.assertContains(response, 'sur son appareil' if lang == 'fr' else 'على جهازه')
                self.assertContains(response, 'convenus séparément' if lang == 'fr' else 'باتفاق منفصل')
                self.assertContains(response, 'traduction automatique n’est pas incluse' if lang == 'fr' else 'لا يشمل الحل ترجمة آلية')
                self.assertContains(response, 'cars-public-' + lang + '.png')
                self.assertContains(response, 'dir="rtl"' if lang == 'ar' else 'dir="ltr"')
                self.assertNotContains(response, 'Votre showroom en ligne' if lang == 'ar' else 'معرضك على الإنترنت')
                self.assertEqual(len(response.context['cars_rows']), 16)
                self.assertEqual(len(response.context['cars_faq']), 8)

    def test_contextual_whatsapp_and_external_link(self):
        from urllib.parse import urlparse, parse_qs
        project = self.seed()
        for lang in ['fr', 'ar']:
            self.client.get(f'/set-language/{lang}/')
            response = self.client.get(project.get_absolute_url())
            url = urlparse(response.context['cars_sales_url'])
            self.assertEqual(url.netloc, 'wa.me')
            self.assertEqual(url.path, '/212682868549')
            message = parse_qs(url.query)['text'][0]
            self.assertIn('achat unique' if lang == 'fr' else 'لمرة واحدة', message)
            self.assertEqual(response.context['cars_external_url'], project.link)
            self.assertContains(response, 'href="https://cars.digicode.ma/"')

    def test_missing_whatsapp_falls_back_to_contact(self):
        from django.core.cache import cache
        project = self.seed()
        self.settings.whatsapp_number = ''
        self.settings.save()
        cache.clear()
        response = self.client.get(project.get_absolute_url())
        self.assertEqual(response.context['cars_sales_url'], '/contact/#project-form')
        self.assertFalse(response.context['cars_has_whatsapp'])
        self.assertNotContains(response, 'href=""')

    def test_visibility_home_gallery_and_sitemap(self):
        project = self.seed()
        for path in ['/', '/projects/', '/sitemap.xml']:
            self.assertContains(self.client.get(path), project.get_absolute_url())
        project.is_active = False
        project.save()
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 404)
        for path in ['/', '/projects/', '/sitemap.xml']:
            self.assertNotContains(self.client.get(path), project.get_absolute_url())
