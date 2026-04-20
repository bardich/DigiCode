from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language


class Service(models.Model):
    """Service model for different website types."""
    
    SERVICE_TYPES = [
        ('rental_cars', _('Rental Cars Website')),
        ('used_cars', _('Used Cars Marketplace')),
        ('ecommerce', _('E-commerce Website')),
        ('real_estate', _('Real Estate Website')),
        ('custom', _('Custom Business Website')),
    ]
    
    # Title
    title_fr = models.CharField(_('Title (FR)'), max_length=200)
    title_ar = models.CharField(_('Title (AR)'), max_length=200, blank=True)
    
    # Slug for URL
    slug = models.SlugField(_('Slug'), unique=True)
    
    # Short description for listings
    short_description_fr = models.TextField(_('Short Description (FR)'))
    short_description_ar = models.TextField(_('Short Description (AR)'), blank=True)
    
    # Full description for detail page
    full_description_fr = models.TextField(_('Full Description (FR)'))
    full_description_ar = models.TextField(_('Full Description (AR)'), blank=True)
    
    # Benefits (JSON field for list of benefits)
    benefits_fr = models.JSONField(_('Benefits (FR)'), default=list)
    benefits_ar = models.JSONField(_('Benefits (AR)'), default=list)
    
    # Media
    featured_image = models.ImageField(_('Featured Image'), upload_to='services/')
    youtube_url = models.URLField(_('YouTube Video URL'), blank=True)
    
    # Meta
    meta_title_fr = models.CharField(_('Meta Title (FR)'), max_length=70, blank=True)
    meta_title_ar = models.CharField(_('Meta Title (AR)'), max_length=70, blank=True)
    meta_description_fr = models.TextField(_('Meta Description (FR)'), blank=True)
    meta_description_ar = models.TextField(_('Meta Description (AR)'), blank=True)
    
    # Status
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    display_order = models.PositiveIntegerField(_('Display Order'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
    
    def __str__(self):
        return self.title_fr
    
    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})
    
    def get_whatsapp_message(self):
        """Generate WhatsApp message for this service."""
        lang = get_language()
        if lang == 'ar':
            return f"مرحباً، أنا مهتم بخدمة {self.title_ar or self.title_fr}. يرجى إرسال المزيد من التفاصيل."
        return f"Bonjour, je suis intéressé par votre service {self.title_fr}. Veuillez m'envoyer plus de détails."
    
    def get_title(self):
        if get_language() == 'ar' and self.title_ar:
            return self.title_ar
        return self.title_fr
    
    def get_short_description(self):
        if get_language() == 'ar' and self.short_description_ar:
            return self.short_description_ar
        return self.short_description_fr
    
    def get_full_description(self):
        if get_language() == 'ar' and self.full_description_ar:
            return self.full_description_ar
        return self.full_description_fr
    
    def get_benefits(self):
        if get_language() == 'ar' and self.benefits_ar:
            return self.benefits_ar
        return self.benefits_fr
