from .models import Service


def services_processor(request):
    """Add services to template context."""
    return {
        'header_services': Service.objects.filter(is_active=True)[:5],
    }
