from django.shortcuts import redirect
from django.views.generic import TemplateView, View, ListView
from django.utils.translation import activate, get_language
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from apps.core.models import Project


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.services.models import Service
        from apps.core.models import HeroSlide
        context['featured_services'] = Service.objects.filter(is_active=True, is_featured=True)[:6]
        context['services'] = Service.objects.filter(is_active=True)[:8]
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order')
        return context


class SetLanguageView(View):
    def get(self, request, lang):
        if lang in ['fr', 'ar']:
            request.session['language'] = lang
            activate(lang)
            messages.success(request, _('Language changed successfully.'))
        
        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class ProjectListView(ListView):
    """Public page listing all active projects."""
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_active=True).order_by('-created_at')
