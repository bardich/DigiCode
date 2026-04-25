from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext_lazy as _
from .models import Service


class RentalLandingPageView(TemplateView):
    """Landing page for Rental Cars service in Arabic."""
    template_name = 'services/lp_rental_ar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the rental cars service if it exists
        try:
            context['service'] = Service.objects.filter(
                is_active=True,
                slug__icontains='rental'
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
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        
        # Get related services (exclude current)
        context['related_services'] = Service.objects.filter(
            is_active=True
        ).exclude(id=service.id)[:4]
        
        # WhatsApp message
        context['whatsapp_message'] = service.get_whatsapp_message()
        context['whatsapp_number'] = service.site_settings.whatsapp_number if hasattr(service, 'site_settings') else '+212600000000'
        
        return context
