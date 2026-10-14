from django import forms
from apps.core.models import MarketingSnippet
from apps.core.forms import bilingual


class MarketingSnippetForm(forms.ModelForm):
    code = forms.CharField(strip=False, widget=forms.Textarea(attrs={'rows':18, 'dir':'ltr', 'spellcheck':'false', 'class':'marketing-code'}))

    class Meta:
        model = MarketingSnippet
        fields = ['name', 'code', 'position', 'is_enabled', 'display_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {'name':('Nom de l’extrait','اسم المقتطف'), 'code':('Code complet','الشفرة كاملة'), 'position':('Emplacement','الموضع'), 'is_enabled':('Activer cet extrait','تفعيل هذا المقتطف'), 'display_order':('Ordre d’exécution','ترتيب التشغيل')}
        for name, (fr, ar) in labels.items():
            self.fields[name].label = bilingual(fr, ar)
            self.fields[name].error_messages['required'] = bilingual('Ce champ est obligatoire.', 'هذا الحقل مطلوب.')
            self.fields[name].widget.attrs['aria-describedby'] = f'{name}-errors'
        self.fields['position'].choices = [('head', bilingual('Dans <head>', 'داخل <head>')), ('body_start', bilingual('Au début de <body>', 'في بداية <body>'))]
