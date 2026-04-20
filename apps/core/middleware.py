from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    """Middleware to handle language switching."""
    
    def process_request(self, request):
        language = request.session.get('language')
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = language
