from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.core.models import MarketingSnippet, SiteSettings
from apps.core.forms import bilingual
from .marketing_forms import MarketingSnippetForm


class SuperuserOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_superuser


class MarketingListView(SuperuserOnlyMixin, ListView):
    model = MarketingSnippet
    template_name = 'dashboard/marketing_list.html'
    context_object_name = 'snippets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marketing_enabled'] = SiteSettings.load().marketing_enabled
        return context


class EditorMixin(SuperuserOnlyMixin):
    model = MarketingSnippet
    form_class = MarketingSnippetForm
    template_name = 'dashboard/marketing_form.html'
    success_url = reverse_lazy('dashboard:marketing_list')

    def form_valid(self, form):
        form.instance.last_editor = self.request.user
        messages.success(self.request, bilingual('Extrait enregistré.', 'تم حفظ المقتطف.'))
        return super().form_valid(form)


class MarketingCreateView(EditorMixin, CreateView):
    pass


class MarketingUpdateView(EditorMixin, UpdateView):
    pass


class MarketingDeleteView(SuperuserOnlyMixin, DeleteView):
    model = MarketingSnippet
    template_name = 'dashboard/marketing_delete.html'
    success_url = reverse_lazy('dashboard:marketing_list')


class MarketingToggleView(SuperuserOnlyMixin, View):
    def post(self, request, pk):
        snippet = get_object_or_404(MarketingSnippet, pk=pk)
        snippet.is_enabled = not snippet.is_enabled
        snippet.last_editor = request.user
        snippet.save(update_fields=['is_enabled', 'last_editor', 'updated_at'])
        return redirect('dashboard:marketing_list')


class MarketingGlobalView(SuperuserOnlyMixin, View):
    def post(self, request):
        settings = SiteSettings.load()
        settings.marketing_enabled = request.POST.get('enabled') == '1'
        settings.save(update_fields=['marketing_enabled'])
        return redirect('dashboard:marketing_list')
