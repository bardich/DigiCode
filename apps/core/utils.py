import re
from django.utils.text import slugify
from unidecode import unidecode


def arabic_slugify(text):
    """
    Create a URL-friendly slug from Arabic or mixed text.
    
    For Arabic text: Uses transliteration to create Latin characters
    For mixed text: Preserves Latin characters and transliterates Arabic
    """
    if not text:
        return ''
    
    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)
    
    # Check if text contains Arabic characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    has_arabic = arabic_pattern.search(text)
    
    if has_arabic:
        # For Arabic text, use transliteration
        # First try unidecode for basic transliteration
        slug = unidecode(text)
        
        # Clean up the transliterated text
        slug = re.sub(r'[^\w\s-]', '', slug.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # If transliteration resulted in mostly non-Latin, create a numeric-based slug
        if not re.match(r'^[a-z0-9-]+$', slug):
            # Create hash-based slug for pure Arabic
            import hashlib
            hash_obj = hashlib.md5(text.encode('utf-8'))
            slug = f"ar-{hash_obj.hexdigest()[:8]}"
    else:
        # For non-Arabic text, use normal slugify
        slug = slugify(text)
    
    # Ensure slug is not empty
    if not slug:
        import hashlib
        hash_obj = hashlib.md5(text.encode('utf-8'))
        slug = f"slug-{hash_obj.hexdigest()[:8]}"
    
    # Limit length
    if len(slug) > 50:
        slug = slug[:50].rstrip('-')
    
    return slug


def create_unique_slug(model_class, title, instance=None):
    """
    Create a unique slug for a model instance.
    
    Args:
        model_class: The model class (Service, Project, etc.)
        title: The title to create slug from
        instance: Current instance (for updates)
    
    Returns:
        Unique slug string
    """
    slug = arabic_slugify(title)
    original_slug = slug
    counter = 1
    
    # Build query to check for existing slugs
    queryset = model_class.objects.filter(slug__startswith=slug)
    if instance:
        queryset = queryset.exclude(pk=instance.pk)
    
    # Check if slug exists and make it unique
    while queryset.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug


def normalize_arabic_text(text):
    """
    Normalize Arabic text for consistent processing.
    """
    if not text:
        return text
    
    # Normalize Arabic characters
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = text.replace('ى', 'ي')
    
    # Remove diacritics (optional)
    # text = re.sub(r'[\u064B-\u0652]', '', text)
    
    return text.strip()


def whatsapp_url(number, message=''):
    from urllib.parse import urlencode
    digits = re.sub(r'\D', '', number or '')
    if digits.startswith('00'):
        digits = digits[2:]
    if not 8 <= len(digits) <= 15:
        return ''
    return 'https://wa.me/' + digits + ('?' + urlencode({'text': message}) if message else '')
