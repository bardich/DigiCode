from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.services.models import Service
from apps.analytics.models import PageView, ClickEvent, ServiceViewCount


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['featured_services'] = Service.objects.filter(is_featured=True).count()
        context['recent_views'] = PageView.objects.all()[:5]
        context['total_page_views'] = PageView.objects.count()
        context['popular_services'] = ServiceViewCount.objects.order_by('-total_views')[:5]
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
