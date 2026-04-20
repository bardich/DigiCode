from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Site-wide settings model."""
    site_name = models.CharField(_('Site Name'), max_length=100, default='DigiCode Web Agency')
    site_description_fr = models.TextField(_('Site Description (FR)'), blank=True)
    site_description_ar = models.TextField(_('Site Description (AR)'), blank=True)
    whatsapp_number = models.CharField(_('WhatsApp Number'), max_length=20, default='+212600000000')
    email = models.EmailField(_('Email'), default='contact@digicode.ma')
    address_fr = models.TextField(_('Address (FR)'), blank=True)
    address_ar = models.TextField(_('Address (AR)'), blank=True)
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True)
    logo = models.ImageField(_('Logo'), upload_to='site/', blank=True)
    favicon = models.ImageField(_('Favicon'), upload_to='site/', blank=True)
    
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
