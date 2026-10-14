from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'services:list', 'core:project_list', 'services:rental_landing', 'services:usedcars_landing', 'services:artisana_landing']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        from .models import Project
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class DemoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        from .models import Project
        return Project.objects.filter(is_active=True, landing_page__in=['cv_professional', 'cv_creative'])

    def location(self, obj):
        return obj.get_demo_url()

    def lastmod(self, obj):
        return obj.updated_at
