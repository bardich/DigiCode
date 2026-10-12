from .models import SiteSettings


def site_settings(request):
    """Add site settings to template context."""
    from .models import SiteSettings
    try:
        settings = SiteSettings.load()
    except Exception:
        # Return default values if database isn't ready
        settings = None
    return {
        'site_settings': settings,
    }


def current_language(request):
    """Add current language to template context."""
    from django.utils.translation import get_language
    return {
        'CURRENT_LANGUAGE': get_language(),
        'IS_RTL': get_language() == 'ar',
    }


def redesign(request):
    from .utils import whatsapp_url
    from django.utils.translation import get_language
    from .forms import bilingual
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = SiteSettings()
    lang = get_language()[:2]
    heading = getattr(settings, f'home_heading_{lang}', '') or bilingual('Votre ambition. Notre savoir-faire digital.', 'طموحك. خبرتنا الرقمية.')
    subheading = getattr(settings, f'home_subheading_{lang}', '') or bilingual('Des sites web sur mesure, pensés pour votre activité et conçus pour aller plus loin. Du Maroc à l’international.', 'مواقع ويب مخصصة لنشاطك، مصممة لتفتح لك آفاقاً جديدة. من المغرب إلى العالم.')
    description = getattr(settings, f'site_description_{lang}', '') or subheading
    return {
        'home_heading': heading, 'home_subheading': subheading, 'page_description': description,
        'canonical_url': request.build_absolute_uri(request.path),
        'whatsapp_url': whatsapp_url(settings.whatsapp_number, bilingual('Bonjour, parlons de mon projet web.', 'مرحباً، أود مناقشة مشروع الويب الخاص بي.')),
    }
