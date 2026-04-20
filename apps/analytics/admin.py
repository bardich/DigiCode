from django.contrib import admin
from .models import PageView, ClickEvent, ServiceViewCount


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'ip_address', 'timestamp']
    list_filter = ['timestamp']
    date_hierarchy = 'timestamp'
    readonly_fields = ['url', 'path', 'session_key', 'ip_address', 'user_agent', 'referrer', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ['click_type', 'element_id', 'page_url', 'timestamp']
    list_filter = ['click_type', 'timestamp']
    date_hierarchy = 'timestamp'
    readonly_fields = ['click_type', 'element_id', 'url', 'page_url', 'session_key', 'ip_address', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ServiceViewCount)
class ServiceViewCountAdmin(admin.ModelAdmin):
    list_display = ['service', 'total_views', 'unique_views', 'last_viewed']
    readonly_fields = ['service', 'total_views', 'unique_views', 'last_viewed']
