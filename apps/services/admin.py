from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'slug', 'is_active', 'is_featured', 'display_order', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    list_editable = ['is_active', 'is_featured', 'display_order']
    search_fields = ['title_fr', 'title_ar', 'slug']
    prepopulated_fields = {'slug': ('title_fr',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('title_fr', 'title_ar', 'slug', 'featured_image')
        }),
        (_('Description'), {
            'fields': (
                'short_description_fr', 'short_description_ar',
                'full_description_fr', 'full_description_ar'
            )
        }),
        (_('Benefits'), {
            'fields': ('benefits_fr', 'benefits_ar')
        }),
        (_('Media'), {
            'fields': ('youtube_url',)
        }),
        (_('SEO'), {
            'fields': (
                'meta_title_fr', 'meta_title_ar',
                'meta_description_fr', 'meta_description_ar'
            ),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
