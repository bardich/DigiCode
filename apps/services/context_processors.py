from django.core.cache import cache
from .models import Service


def services_processor(request):
    """Add services to template context (cached for 5 minutes)."""
    cache_key = 'header_services'
    header_services = cache.get(cache_key)
    
    if header_services is None:
        header_services = list(Service.objects.filter(is_active=True)[:5])
        cache.set(cache_key, header_services, 300)  # Cache for 5 minutes
    
    return {
        'header_services': header_services,
    }
