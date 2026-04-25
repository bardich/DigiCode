from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, render
from apps.services.models import Service
from apps.analytics.models import PageView, ClickEvent, ServiceViewCount
from apps.core.models import SiteSettings, HeroSlide


from django.utils import timezone
from datetime import timedelta

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['featured_services'] = Service.objects.filter(is_featured=True).count()
        context['total_page_views'] = PageView.objects.count()
        context['recent_services'] = Service.objects.order_by('-created_at')[:5]
        context['popular_services'] = ServiceViewCount.objects.order_by('-total_views')[:5]
        
        # Today's stats
        today = timezone.now().date()
        context['new_services_today'] = Service.objects.filter(
            created_at__date=today
        ).count()
        context['views_today'] = PageView.objects.filter(
            timestamp__date=today
        ).count()
        
        return context


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'dashboard/service_list.html'
    context_object_name = 'services'
    paginate_by = 20


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'dashboard/service_form.html'
    fields = [
        'title_fr', 'title_ar', 'slug', 'featured_image',
        'short_description_fr', 'short_description_ar',
        'full_description_fr', 'full_description_ar',
        'benefits_fr', 'benefits_ar',
        'youtube_url',
        'meta_title_fr', 'meta_title_ar',
        'meta_description_fr', 'meta_description_ar',
        'is_active', 'is_featured', 'display_order'
    ]
    success_url = reverse_lazy('dashboard:service_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Service created successfully.'))
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    template_name = 'dashboard/service_form.html'
    fields = [
        'title_fr', 'title_ar', 'slug', 'featured_image',
        'short_description_fr', 'short_description_ar',
        'full_description_fr', 'full_description_ar',
        'benefits_fr', 'benefits_ar',
        'youtube_url',
        'meta_title_fr', 'meta_title_ar',
        'meta_description_fr', 'meta_description_ar',
        'is_active', 'is_featured', 'display_order'
    ]
    success_url = reverse_lazy('dashboard:service_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Service updated successfully.'))
        return super().form_valid(form)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'dashboard/service_confirm_delete.html'
    success_url = reverse_lazy('dashboard:service_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Service deleted successfully.'))
        return super().delete(request, *args, **kwargs)


class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_page_views'] = PageView.objects.count()
        context['total_clicks'] = ClickEvent.objects.count()
        context['recent_views'] = PageView.objects.all()[:20]
        context['recent_clicks'] = ClickEvent.objects.all()[:20]
        context['popular_services'] = ServiceViewCount.objects.order_by('-total_views')[:10]
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.first()
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order')
        context['icon_choices'] = HeroSlide.ICON_CHOICES
        context['color_choices'] = HeroSlide.COLOR_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle HeroSlide management
        if 'slide_action' in request.POST:
            return self.handle_slide_action(request)
        
        # Handle site settings
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
        
        fields = [
            'site_name', 'whatsapp_number', 'email', 'phone',
            'address_fr', 'address_ar', 'facebook_url', 'instagram_url',
            'linkedin_url', 'youtube_url', 'meta_title', 'meta_description',
            'google_analytics_id',
            'footer_text_fr', 'footer_text_ar',
            'primary_color', 'accent_color', 'highlight_color'
        ]
        
        for field in fields:
            if field in request.POST:
                setattr(settings, field, request.POST.get(field))
        
        # Handle description fields
        if 'site_description_fr' in request.POST:
            settings.site_description_fr = request.POST.get('site_description_fr')
        if 'site_description_ar' in request.POST:
            settings.site_description_ar = request.POST.get('site_description_ar')
        
        if 'logo' in request.FILES:
            settings.logo = request.FILES['logo']
        if 'favicon' in request.FILES:
            settings.favicon = request.FILES['favicon']
        
        settings.save()
        messages.success(request, _('Settings updated successfully.'))
        return redirect('dashboard:settings')
    
    def handle_slide_action(self, request):
        action = request.POST.get('slide_action')
        
        if action == 'add':
            HeroSlide.objects.create(
                title_fr=request.POST.get('slide_title_fr', ''),
                title_ar=request.POST.get('slide_title_ar', ''),
                description_fr=request.POST.get('slide_description_fr', ''),
                description_ar=request.POST.get('slide_description_ar', ''),
                icon=request.POST.get('slide_icon', 'code'),
                color_theme=request.POST.get('slide_color', 'blue'),
                link=request.POST.get('slide_link', ''),
                order=HeroSlide.objects.count()
            )
            messages.success(request, _('Slide added successfully.'))
            
        elif action == 'edit':
            slide_id = request.POST.get('slide_id')
            try:
                slide = HeroSlide.objects.get(id=slide_id)
                slide.title_fr = request.POST.get('slide_title_fr', '')
                slide.title_ar = request.POST.get('slide_title_ar', '')
                slide.description_fr = request.POST.get('slide_description_fr', '')
                slide.description_ar = request.POST.get('slide_description_ar', '')
                slide.icon = request.POST.get('slide_icon', 'code')
                slide.color_theme = request.POST.get('slide_color', 'blue')
                slide.link = request.POST.get('slide_link', '')
                slide.is_active = request.POST.get('slide_is_active') == 'on'
                slide.save()
                messages.success(request, _('Slide updated successfully.'))
            except HeroSlide.DoesNotExist:
                messages.error(request, _('Slide not found.'))
                
        elif action == 'delete':
            slide_id = request.POST.get('slide_id')
            try:
                slide = HeroSlide.objects.get(id=slide_id)
                slide.delete()
                messages.success(request, _('Slide deleted successfully.'))
            except HeroSlide.DoesNotExist:
                messages.error(request, _('Slide not found.'))
                
        elif action == 'reorder':
            slide_id = request.POST.get('slide_id')
            direction = request.POST.get('direction')
            try:
                slide = HeroSlide.objects.get(id=slide_id)
                if direction == 'up':
                    slide.order = max(0, slide.order - 1)
                else:
                    slide.order = slide.order + 1
                slide.save()
                messages.success(request, _('Slide order updated.'))
            except HeroSlide.DoesNotExist:
                messages.error(request, _('Slide not found.'))
        
        return redirect('dashboard:settings')


class DashboardLoginView(TemplateView):
    """Custom login view for dashboard."""
    template_name = 'dashboard/login.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect if already authenticated
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, _('Welcome back!'))
                # Redirect to next URL if provided, otherwise to dashboard
                next_url = request.GET.get('next', 'dashboard:index')
                return redirect(next_url)
            else:
                messages.error(request, _('Your account is disabled.'))
        else:
            messages.error(request, _('Invalid username or password.'))
        
        return render(request, self.template_name)


class DashboardLogoutView(TemplateView):
    """Logout view that redirects to login page."""
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _('You have been logged out.'))
        return redirect('dashboard:login')
