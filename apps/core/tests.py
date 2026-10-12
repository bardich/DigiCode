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
