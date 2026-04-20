from .models import SiteSettings


def site_settings(request):
    """Add site settings to template context."""
    return {
        'site_settings': SiteSettings.load(),
    }


def current_language(request):
    """Add current language to template context."""
    from django.utils.translation import get_language
    return {
        'CURRENT_LANGUAGE': get_language(),
        'IS_RTL': get_language() == 'ar',
    }
