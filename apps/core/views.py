from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View, ListView, DetailView
from django.utils.translation import activate, get_language
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from apps.core.models import Project, Inquiry
from .forms import InquiryForm, bilingual
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.urls import reverse
from urllib.parse import urlsplit
from django.utils.http import url_has_allowed_host_and_scheme


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.services.models import Service
        from apps.core.models import HeroSlide
        context['featured_services'] = Service.objects.filter(
            is_active=True, is_featured=True
        )[:6]
        context['services'] = Service.objects.filter(
            is_active=True
        )[:8]
        context['hero_slides'] = HeroSlide.objects.filter(
            is_active=True
        ).order_by('order')
        context['featured_projects'] = Project.objects.filter(is_active=True, is_featured=True).order_by('display_order', '-created_at')[:3]
        return context


class SetLanguageView(View):
    def get(self, request, lang):
        if lang in ['fr', 'ar']:
            request.session['language'] = lang
            activate(lang)
        
        next_url = request.META.get('HTTP_REFERER', '/')
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'
        return redirect(next_url)


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            from apps.services.models import Service
            service = Service.objects.filter(is_active=True, slug=self.request.GET.get('service', '')).first()
            initial = {'service': service}
            project = Project.objects.filter(is_active=True, slug=self.request.GET.get('project', '')).first()
            intent = self.request.GET.get('intent', '')
            if project and intent in ['demo', 'quote']:
                business_fr = 'Mon entreprise' if project.landing_page == 'ecommerce' else 'Mon agence'
                business_ar = 'نشاطي' if project.landing_page == 'ecommerce' else 'وكالتي'
                initial['brief'] = bilingual(
                    f"Je souhaite {'une démonstration' if intent == 'demo' else 'un devis'} pour {project.get_title()}. {business_fr} : ",
                    f"أرغب في {'عرض توضيحي' if intent == 'demo' else 'عرض سعر'} لمشروع {project.get_title()}. {business_ar}: "
                )
            context['form'] = InquiryForm(initial=initial)
        context['submitted'] = self.request.session.pop('inquiry_submitted', False)
        return context

    def post(self, request, *args, **kwargs):
        form = InquiryForm(request.POST)
        if request.POST.get('website'):
            form.add_error(None, bilingual('Votre demande n’a pas pu être envoyée.', 'تعذر إرسال طلبك.'))
            return self.render_to_response(self.get_context_data(form=form), status=400)
        if form.is_valid():
            # Database-backed limit also works with the development dummy cache.
            # Lock a stable row to serialize submissions on production PostgreSQL.
            from .models import SiteSettings
            with transaction.atomic():
                SiteSettings.load()
                SiteSettings.objects.select_for_update().get(pk=1)
                recent = Inquiry.objects.filter(email__iexact=form.cleaned_data['email'], created_at__gte=timezone.now() - timedelta(minutes=15)).count()
                last_submission = request.session.get('inquiry_last_submission', 0)
                if recent >= 3 or timezone.now().timestamp() - last_submission < 60:
                    form.add_error(None, bilingual('Veuillez patienter avant d’envoyer une autre demande.', 'يرجى الانتظار قبل إرسال طلب آخر.'))
                    return self.render_to_response(self.get_context_data(form=form), status=429)
                inquiry = form.save(commit=False)
                inquiry.language = get_language()[:2]
                referrer = request.META.get('HTTP_REFERER', '')
                inquiry.source_page = urlsplit(referrer).path[:500] if url_has_allowed_host_and_scheme(referrer, {request.get_host()}) else request.path
                inquiry.save()
            request.session['inquiry_last_submission'] = timezone.now().timestamp()
            request.session['inquiry_submitted'] = True
            return redirect(reverse('core:contact') + '#project-form')
        return self.render_to_response(self.get_context_data(form=form), status=400)


class ProjectListView(ListView):
    """Public page listing all active projects."""
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_active=True).order_by('-created_at')


class ProjectDetailView(DetailView):
    """Public page showing a single project."""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(is_active=True)

    def get_template_names(self):
        if self.object.landing_page == 'car_rental':
            return ['core/project_rental.html']
        if self.object.landing_page == 'ecommerce':
            return ['core/project_ecommerce.html']
        if self.object.landing_page == 'used_cars':
            return ['core/project_usedcars.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.landing_page == 'car_rental':
            from .rental_content import rental_context
            context.update(rental_context(self.request, self.object))
        elif self.object.landing_page == 'ecommerce':
            from .ecommerce_content import ecommerce_context
            context.update(ecommerce_context(self.request, self.object))
        elif self.object.landing_page == 'used_cars':
            from .usedcars_content import usedcars_context
            context.update(usedcars_context(self.request, self.object))
        return context
