import json
from django.test import TestCase, Client, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from django.template.loader import render_to_string
from .models import MarketingSnippet, SiteSettings
from .marketing import parse_snippet, marketing_context
from .tests import TEST_MIDDLEWARE
from apps.dashboard.marketing_forms import MarketingSnippetForm


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class MarketingTests(TestCase):
    def setUp(self):
        cache.clear()
        self.settings = SiteSettings.objects.create(google_analytics_id='G-LEGACY')
        User=get_user_model()
        self.admin=User.objects.create_superuser(username='marketer',email='admin@example.test',password='test-pass')
        self.staff=User.objects.create_user(username='staff',password='test-pass',is_staff=True)
        self.snippet=MarketingSnippet.objects.create(name='Meta example',code='<script>window.example = "<unsafe>";</script>',is_enabled=True)

    def tearDown(self):
        cache.clear()

    def config(self, path='/'):
        request=RequestFactory().get(path)
        request.resolver_match=resolve(path)
        return marketing_context(request).get('marketing_config')

    def enable_global(self):
        self.settings.marketing_enabled=True
        self.settings.save()

    def test_default_disabled_and_legacy_preserved(self):
        self.assertIsNone(self.config())
        self.assertNotContains(self.client.get('/'), 'marketing-config')
        self.assertFalse(MarketingSnippet(name='New',code='<script>x()</script>').is_enabled)
        self.assertEqual(SiteSettings.load().google_analytics_id,'G-LEGACY')

    def test_public_allowlist_and_exclusions(self):
        self.enable_global()
        for path in ['/','/about/','/contact/','/services/','/projects/','/services/lp/rental/','/services/lp/usedcars/','/services/lp/artisana/']:
            with self.subTest(path=path):
                response=self.client.get(path)
                self.assertContains(response,'id="marketing-config"',count=1)
                self.assertContains(response,'js/marketing-consent.js',count=1)
                self.assertContains(response,'digicode-marketing-body-start')
                self.assertNotContains(response,'<script>window.example')
                self.assertContains(response,'\\u003Cunsafe\\u003E')
        for path in ['/dashboard/','/dashboard/login/','/demos/cv-professionnel/','/demos/portfolio-creatif/']:
            self.assertIsNone(self.config(path))
        for template in ['404.html','500.html']:
            request=RequestFactory().get('/projects/missing/')
            request.resolver_match=resolve('/projects/missing/')
            html=render_to_string(template,request=request)
            self.assertNotIn('marketing-config',html)
            self.assertNotIn('marketing-consent.js',html)
            self.assertNotIn('data-marketing-preferences',html)

    def test_fingerprint_changes_and_order(self):
        self.enable_global()
        initial=self.config()['fingerprint']
        self.snippet.name='Renamed';self.snippet.save()
        self.assertEqual(self.config()['fingerprint'],initial)
        inactive=MarketingSnippet.objects.create(name='Inactive',code='<script>ignored()</script>',display_order=1)
        self.assertEqual(self.config()['fingerprint'],initial)
        for field,value in [('position','body_start'),('display_order',5),('code','<script>updated()</script>')]:
            setattr(self.snippet,field,value);self.snippet.save()
            updated=self.config()['fingerprint'];self.assertNotEqual(updated,initial);initial=updated
        inactive.is_enabled=True;inactive.save()
        config=self.config()
        self.assertEqual(config['snippets'][0]['scripts'][0]['text'],'ignored()')
        self.assertNotEqual(config['fingerprint'],initial)
        inactive.delete()
        self.snippet.is_enabled=False;self.snippet.save()
        self.assertIsNone(self.config())

    def test_snippet_parser_and_validation(self):
        valid=[
            '<!-- Meta Pixel --><script>!function(f){f.fbq=function(){}}(window);</script><noscript><img src="https://example.test/pixel"></noscript>',
            '<script async src="https://example.test/gtag.js?id=G-TEST"></script><script>window.dataLayer=[];function gtag(){dataLayer.push(arguments)}gtag("config","G-TEST");</script>',
            '<noscript><iframe src="https://example.test/ns.html?id=GTM-TEST" height="0" width="0"></iframe></noscript>',
            '<script type="module">window.moduleTest=true;</script>',
        ]
        for code in valid: parse_snippet(code)
        invalid=['', '<script></script>', '<script>unclosed', '<html><head><script>x()</script></head></html>', '<img src="https://example.test/pixel">','alert(1)','<script src="javascript:alert(1)"></script>','<script onload="x()" src="/x.js"></script>','<script>document.write("x")</script>', '<script/>', '<script src>window.bad()</script>','<script type="text/plain">x()</script>', '<script>'+('é'*26000)+'</script>']
        for code in invalid:
            with self.subTest(code=code[:60]), self.assertRaises(ValidationError): parse_snippet(code)

    def test_form_round_trip_and_invalid_values(self):
        code='\r\n<!-- sample -->\r\n<script>window.test = "& < >";</script>\r\n'
        form=MarketingSnippetForm(data={'name':'Test','code':code,'position':'head','display_order':0})
        self.assertTrue(form.is_valid(),form.errors)
        self.assertEqual(form.save().code,code)
        bad=MarketingSnippetForm(data={'name':'Test','code':'<iframe></iframe>','position':'head','display_order':0})
        self.assertFalse(bad.is_valid());self.assertEqual(bad['code'].value(),'<iframe></iframe>')

    def test_every_endpoint_requires_superuser(self):
        paths=[reverse('dashboard:marketing_list'),reverse('dashboard:marketing_create'),reverse('dashboard:marketing_edit',args=[self.snippet.pk]),reverse('dashboard:marketing_delete',args=[self.snippet.pk]),reverse('dashboard:marketing_toggle',args=[self.snippet.pk]),reverse('dashboard:marketing_global')]
        for path in paths:
            self.assertEqual(self.client.get(path).status_code,302)
        self.client.force_login(self.staff)
        for path in paths:
            self.assertEqual(self.client.get(path).status_code,403)
            self.assertEqual(self.client.post(path,{}).status_code,403)
        self.assertNotContains(self.client.get('/dashboard/'),'href="/dashboard/marketing/"')
        # General settings cannot act as an alternative global-toggle endpoint.
        self.client.post('/dashboard/settings/', {'marketing_enabled':'1'})
        self.settings.refresh_from_db();self.assertFalse(self.settings.marketing_enabled)

    def test_admin_permission_and_global_readonly(self):
        from .admin import MarketingSnippetAdmin,SiteSettingsAdmin
        from django.contrib.admin.sites import AdminSite
        request=RequestFactory().get('/');request.user=self.staff
        admin=MarketingSnippetAdmin(MarketingSnippet,AdminSite())
        for method in ['has_module_permission','has_add_permission','has_view_permission','has_change_permission','has_delete_permission']:
            self.assertFalse(getattr(admin,method)(request))
        self.assertIn('marketing_enabled',SiteSettingsAdmin(SiteSettings,AdminSite()).get_readonly_fields(request))
        request.user=self.admin
        self.assertTrue(admin.has_change_permission(request))

    def test_management_csrf_ordering_toggle_and_delete(self):
        self.client.force_login(self.admin)
        csrf=Client(enforce_csrf_checks=True);csrf.force_login(self.admin)
        self.assertEqual(csrf.post(reverse('dashboard:marketing_global'),{'enabled':'1'}).status_code,403)
        create=reverse('dashboard:marketing_create')
        response=self.client.post(create,{'name':'Google','code':'<script>window.googleTest=true;</script>','position':'body_start','display_order':3})
        self.assertEqual(response.status_code,302)
        snippet=MarketingSnippet.objects.get(name='Google')
        self.assertFalse(snippet.is_enabled);self.assertEqual(snippet.last_editor,self.admin)
        response=self.client.get(reverse('dashboard:marketing_edit',args=[self.snippet.pk]))
        self.assertContains(response,'&lt;script&gt;window.example')
        self.assertNotContains(response,'<script>window.example')
        self.client.post(reverse('dashboard:marketing_toggle',args=[snippet.pk]))
        snippet.refresh_from_db();self.assertTrue(snippet.is_enabled)
        self.client.post(reverse('dashboard:marketing_global'),{'enabled':'1'})
        self.assertIsNotNone(self.config())
        self.client.post(reverse('dashboard:marketing_edit',args=[snippet.pk]),{'name':'Google','code':snippet.code,'position':'head','display_order':7,'is_enabled':'on'})
        snippet.refresh_from_db();self.assertEqual(snippet.display_order,7)
        self.client.post(reverse('dashboard:marketing_delete',args=[snippet.pk]))
        self.assertFalse(MarketingSnippet.objects.filter(pk=snippet.pk).exists())
        self.client.post(reverse('dashboard:marketing_global'),{'enabled':'0'})
        self.assertIsNone(self.config())

    def test_invalid_import_fails_closed(self):
        self.enable_global()
        MarketingSnippet.objects.filter(pk=self.snippet.pk).update(code='<html>bad</html>')
        self.assertIsNone(self.config())
