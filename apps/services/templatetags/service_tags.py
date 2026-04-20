from django import template
import re

register = template.Library()


@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed URL."""
    if not url:
        return ''
    
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s?]+)',
        r'youtube\.com\/watch\?.*v=([^&\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    return url
