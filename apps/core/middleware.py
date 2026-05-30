from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseNotFound
from django.conf import settings


class LanguageMiddleware(MiddlewareMixin):
    """Middleware to handle language switching."""
    
    def process_request(self, request):
        language = request.session.get('language')
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = language


class AdminSecurityMiddleware:
    """Block access to /admin/ and restrict new admin URL by IP."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Block the default /admin/ URL completely
        if request.path.startswith('/admin/'):
            return HttpResponseNotFound()
        
        # Restrict secret admin URL to specific IPs (if configured)
        if request.path.startswith('/secret-admin-dc2024/'):
            allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
            if allowed_ips:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                if ip not in allowed_ips:
                    return HttpResponseNotFound()
        
        return self.get_response(request)
