from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from django.urls import reverse
from apps.core.utils import create_unique_slug, normalize_arabic_text


class HeroSlide(models.Model):
    """Hero slider slide model for homepage."""
    
    ICON_CHOICES = [
        ('car', _('Car')),
        ('shopping-bag', _('Shopping Bag')),
        ('building', _('Building')),
        ('briefcase', _('Briefcase')),
        ('code', _('Code')),
        ('globe', _('Globe')),
        ('smartphone', _('Smartphone')),
        ('zap', _('Zap')),
    ]
    
    COLOR_CHOICES = [
        ('blue', _('Blue (Rental)')),
        ('purple', _('Purple (E-commerce)')),
        ('emerald', _('Emerald (Business)')),
        ('orange', _('Orange (Portfolio)')),
        ('red', _('Red')),
        ('pink', _('Pink')),
        ('cyan', _('Cyan')),
        ('indigo', _('Indigo')),
    ]
    
    title_fr = models.CharField(_('Title (French)'), max_length=100)
    title_ar = models.CharField(_('Title (Arabic)'), max_length=100, blank=True)
    description_fr = models.TextField(_('Description (French)'), max_length=300)
    description_ar = models.TextField(_('Description (Arabic)'), max_length=300, blank=True)
    icon = models.CharField(_('Icon'), max_length=20, choices=ICON_CHOICES, default='code')
    color_theme = models.CharField(_('Color Theme'), max_length=20, choices=COLOR_CHOICES, default='blue')
    link = models.URLField(_('Link'), blank=True, help_text=_('Optional link for the slide'))
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = _('Hero Slide')
        verbose_name_plural = _('Hero Slides')
    
    def __str__(self):
        return self.title_fr
    
    def get_title(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ar' and self.title_ar:
            return self.title_ar
        return self.title_fr
    
    def get_description(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ar' and self.description_ar:
            return self.description_ar
        return self.description_fr
    
    def get_color_classes(self):
        """Return gradient and background classes based on color theme."""
        color_map = {
            'blue': ('from-blue-500 to-cyan-400', 'bg-blue-500/20'),
            'purple': ('from-purple-500 to-pink-400', 'bg-purple-500/20'),
            'emerald': ('from-emerald-500 to-teal-400', 'bg-emerald-500/20'),
            'orange': ('from-orange-500 to-amber-400', 'bg-orange-500/20'),
            'red': ('from-red-500 to-pink-500', 'bg-red-500/20'),
            'pink': ('from-pink-500 to-rose-400', 'bg-pink-500/20'),
            'cyan': ('from-cyan-500 to-blue-400', 'bg-cyan-500/20'),
            'indigo': ('from-indigo-500 to-purple-400', 'bg-indigo-500/20'),
        }
        return color_map.get(self.color_theme, ('from-blue-500 to-cyan-400', 'bg-blue-500/20'))


class SiteSettings(models.Model):
    """Site-wide settings model."""
    # Site Info
    site_name = models.CharField(_('Site Name'), max_length=100, default='DigiCode Web Agency')
    site_description_fr = models.TextField(_('Site Description (FR)'), blank=True)
    site_description_ar = models.TextField(_('Site Description (AR)'), blank=True)

    home_heading_fr = models.CharField(max_length=180, blank=True)
    home_heading_ar = models.CharField(max_length=180, blank=True)
    home_subheading_fr = models.TextField(max_length=500, blank=True)
    home_subheading_ar = models.TextField(max_length=500, blank=True)

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

    @classmethod
    def load(cls):
        """Get or create the singleton SiteSettings instance (cached for 5 minutes)."""
        from django.core.cache import cache
        cache_key = 'site_settings'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        obj, created = cls.objects.get_or_create(pk=1, defaults={
            'site_name': 'DigiCode Web Agency',
            'email': 'contact@digicode.ma',
            'whatsapp_number': '+212600000000',
        })
        cache.set(cache_key, obj, 300)  # Cache for 5 minutes
        return obj
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        from django.core.cache import cache
        cache.delete('site_settings')  # Invalidate cache on save
    
    def delete(self, *args, **kwargs):
        pass


class Project(models.Model):
    """Project/portfolio item showcasing completed work."""
    title_fr = models.CharField(_('Title (FR)'), max_length=200, default='')
    title_ar = models.CharField(_('Title (AR)'), max_length=200, blank=True, default='')
    slug = models.SlugField(_('Slug'), unique=True, max_length=100, blank=True)
    image = models.ImageField(_('Image'), upload_to='projects/', blank=True, null=True, help_text=_('Project thumbnail or screenshot'))
    short_description_fr = models.TextField(_('Short Description (FR)'), max_length=500, default='', help_text=_('Brief summary shown on the list page'))
    short_description_ar = models.TextField(_('Short Description (AR)'), max_length=500, blank=True, default='')
    full_description_fr = models.TextField(_('Full Description (FR)'), default='', help_text=_('Detailed description shown on the detail page'))
    full_description_ar = models.TextField(_('Full Description (AR)'), blank=True, default='')
    link = models.URLField(_('Project Link'), blank=True, null=True, help_text=_('External link to the live project'))
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self):
        return self.title_fr

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
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            # Use Arabic title if available, otherwise French
            title = self.title_ar if self.title_ar else self.title_fr
            self.slug = create_unique_slug(Project, title, self)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})


class Inquiry(models.Model):
    STATUS_CHOICES = [('new', _('New')), ('contacted', _('Contacted')), ('closed', _('Closed'))]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    service = models.ForeignKey('services.Service', null=True, blank=True, on_delete=models.SET_NULL)
    brief = models.TextField(max_length=5000)
    language = models.CharField(max_length=2, choices=[('fr', 'Français'), ('ar', 'العربية')])
    source_page = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'
