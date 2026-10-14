from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext_lazy as _
from .models import Service


class RentalLandingPageView(TemplateView):
    """Bilingual sales page for the car-rental project."""
    template_name = 'core/project_rental.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.core.models import Project
        from apps.core.rental_content import rental_context
        project = Project.objects.filter(is_active=True, landing_page='car_rental').order_by('display_order', 'pk').first()
        context['project'] = project
        context.update(rental_context(self.request, project))
        return context


class UsedCarsLandingPageView(TemplateView):
    """Bilingual AutoMaroc sales page, also available at its original URL."""
    template_name = 'core/project_usedcars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.core.models import Project
        from apps.core.usedcars_content import usedcars_context
        project = Project.objects.filter(is_active=True, landing_page='used_cars').order_by('display_order', 'pk').first()
        context['project'] = project
        context.update(usedcars_context(self.request, project))
        return context


class ArtisanaLandingPageView(TemplateView):
    """Landing page for Artisana e-commerce platform for artisans in Arabic."""
    template_name = 'services/lp_artisana_ar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the artisana service if it exists
        try:
            context['service'] = Service.objects.filter(
                is_active=True,
                slug__icontains='artisana'
            ).first()
        except Service.DoesNotExist:
            context['service'] = None
        return context


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'
    
    def get_template_names(self):
        if self.object.slug == 'cv-portfolio':
            return ['services/cv_portfolio.html']
        return super().get_template_names()

    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        if service.slug == 'cv-portfolio':
            from apps.core.cv_content import cv_context
            context.update(cv_context(self.request, service=service))
        
        # Get related services (exclude current)
        context['related_services'] = Service.objects.filter(
            is_active=True
        ).exclude(id=service.id)[:4]
        
        # WhatsApp message
        context['whatsapp_message'] = service.get_whatsapp_message()
        context['whatsapp_number'] = service.site_settings.whatsapp_number if hasattr(service, 'site_settings') else '+212600000000'
        
        return context
