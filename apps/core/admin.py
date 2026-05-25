from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Project


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'whatsapp_number', 'email']
    
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'title_ar', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title_fr', 'title_ar']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('title_fr', 'title_ar', 'image')
        }),
        (_('Description'), {
            'fields': (
                'short_description_fr', 'short_description_ar',
                'full_description_fr', 'full_description_ar'
            )
        }),
        (_('Link & Status'), {
            'fields': ('link', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
