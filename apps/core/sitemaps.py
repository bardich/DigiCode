from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'services:list']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
