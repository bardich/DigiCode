from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Site-wide settings model."""
    # Site Info
    site_name = models.CharField(_('Site Name'), max_length=100, default='DigiCode Web Agency')
    site_description_fr = models.TextField(_('Site Description (FR)'), blank=True)
    site_description_ar = models.TextField(_('Site Description (AR)'), blank=True)

    # Footer Text
    footer_text_fr = models.TextField(_('Footer Text (FR)'), blank=True, help_text=_('Copyright text or tagline for footer'))
    footer_text_ar = models.TextField(_('Footer Text (AR)'), blank=True, help_text=_('Copyright text or tagline for footer (Arabic)'))

    # Contact Info
    whatsapp_number = models.CharField(_('WhatsApp Number'), max_length=20, default='+212600000000')
    email = models.EmailField(_('Email'), default='contact@digicode.ma')
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    address_fr = models.TextField(_('Address (FR)'), blank=True)
    address_ar = models.TextField(_('Address (AR)'), blank=True)

    # Social Media
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True)

    # Images
    logo = models.ImageField(_('Logo'), upload_to='site/', blank=True)
    favicon = models.ImageField(_('Favicon'), upload_to='site/', blank=True)

    # SEO
    meta_title = models.CharField(_('Meta Title'), max_length=70, blank=True)
    meta_description = models.TextField(_('Meta Description'), blank=True)
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=20, blank=True)

    # Theme Colors
    primary_color = models.CharField(_('Primary Color'), max_length=7, default='#0F172A', help_text=_('Dark slate color'))
    accent_color = models.CharField(_('Accent Color'), max_length=7, default='#2563EB', help_text=_('Blue color'))
    highlight_color = models.CharField(_('Highlight Color'), max_length=7, default='#F59E0B', help_text=_('Amber/gold color'))
    
    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
