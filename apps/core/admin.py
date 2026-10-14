from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Project, Inquiry


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'whatsapp_number', 'email']

    def get_readonly_fields(self, request, obj=None):
        return [] if request.user.is_superuser else ['marketing_enabled']
    
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
            'fields': ('link', 'is_active', 'is_featured', 'display_order', 'landing_page')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'status', 'created_at']
    list_filter = ['status', 'language']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['name', 'email', 'company', 'phone', 'service', 'brief', 'language', 'source_page', 'created_at']

    def has_add_permission(self, request):
        return False


from apps.core.models import MarketingSnippet
from apps.dashboard.marketing_forms import MarketingSnippetForm


@admin.register(MarketingSnippet)
class MarketingSnippetAdmin(admin.ModelAdmin):
    form = MarketingSnippetForm
    list_display = ['name', 'position', 'is_enabled', 'display_order', 'last_editor', 'updated_at']
    readonly_fields = ['last_editor', 'created_at', 'updated_at']

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user
        super().save_model(request, obj, form, change)
