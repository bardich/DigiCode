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
        
        # Process request first (don't block response with DB write)
        response = self.get_response(request)
        
        # Track analytics AFTER response is generated (non-blocking)
        self._track_page_view(request)
        
        return response
    
    def _track_page_view(self, request):
        """Track page view asynchronously using threading to not block response."""
        import threading
        
        def track():
            try:
                # Ensure session exists
                if not request.session.session_key:
                    request.session.create()
                
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')
                
                # Create page view record
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
        
        # Run tracking in background thread (non-blocking)
        thread = threading.Thread(target=track, daemon=True)
        thread.start()
