import uuid
from django.utils import timezone
from .models import PageView


class AnalyticsMiddleware:
    """Middleware to track page views."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip tracking for static/media files and admin
        if request.path.startswith(('/static/', '/media/', '/admin/', '/__reload__/')):
            return self.get_response(request)
        
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create page view record
        try:
            PageView.objects.create(
                url=request.build_absolute_uri(),
                path=request.path,
                session_key=request.session.session_key,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referrer=request.META.get('HTTP_REFERER', ''),
            )
        except Exception:
            pass  # Don't break the request if tracking fails
        
        response = self.get_response(request)
        return response
