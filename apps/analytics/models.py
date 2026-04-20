from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class PageView(models.Model):
    """Track page views."""
    url = models.URLField(_('URL'))
    path = models.CharField(_('Path'), max_length=500)
    session_key = models.CharField(_('Session Key'), max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    referrer = models.URLField(_('Referrer'), blank=True)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    
    # Generic foreign key to track viewed object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Page View')
        verbose_name_plural = _('Page Views')
        indexes = [
            models.Index(fields=['path', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.timestamp}"


class ClickEvent(models.Model):
    """Track click events."""
    CLICK_TYPES = [
        ('whatsapp', _('WhatsApp')),
        ('email', _('Email')),
        ('phone', _('Phone')),
        ('link', _('Link')),
        ('button', _('Button')),
    ]
    
    click_type = models.CharField(_('Click Type'), max_length=20, choices=CLICK_TYPES)
    element_id = models.CharField(_('Element ID'), max_length=100, blank=True)
    url = models.URLField(_('URL'), blank=True)
    page_url = models.URLField(_('Page URL'))
    session_key = models.CharField(_('Session Key'), max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    
    # Generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Click Event')
        verbose_name_plural = _('Click Events')
    
    def __str__(self):
        return f"{self.click_type} - {self.timestamp}"


class ServiceViewCount(models.Model):
    """Aggregate view counts for services."""
    service = models.OneToOneField('services.Service', on_delete=models.CASCADE, related_name='view_count')
    total_views = models.PositiveIntegerField(_('Total Views'), default=0)
    unique_views = models.PositiveIntegerField(_('Unique Views'), default=0)
    last_viewed = models.DateTimeField(_('Last Viewed'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Service View Count')
        verbose_name_plural = _('Service View Counts')
    
    def __str__(self):
        return f"{self.service.title_fr}: {self.total_views} views"
