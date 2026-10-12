from django import forms
from django.utils.translation import get_language
from apps.services.models import Service
from .models import Inquiry


def bilingual(fr, ar):
    return ar if get_language() == 'ar' else fr


class InquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}))

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'company', 'phone', 'service', 'brief']
        widgets = {'brief': forms.Textarea(attrs={'rows': 5, 'minlength': 20})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'name': ('Votre nom', 'اسمك'), 'email': ('Adresse e-mail', 'البريد الإلكتروني'),
            'company': ('Entreprise · facultatif', 'الشركة · اختياري'),
            'phone': ('Téléphone · facultatif', 'الهاتف · اختياري'),
            'service': ('Service · facultatif', 'الخدمة · اختياري'),
            'brief': ('Parlez-nous de votre projet', 'حدثنا عن مشروعك'),
        }
        for name, (fr, ar) in labels.items():
            field = self.fields[name]
            field.label = bilingual(fr, ar)
            field.error_messages['required'] = bilingual('Ce champ est obligatoire.', 'هذا الحقل مطلوب.')
            field.error_messages['max_length'] = bilingual('Le texte est trop long.', 'النص طويل جداً.')
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-describedby'] = f'{name}-errors'
        self.fields['email'].error_messages['invalid'] = bilingual('Saisissez une adresse e-mail valide.', 'أدخل بريداً إلكترونياً صالحاً.')
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = bilingual('Un projet sur mesure / à définir', 'مشروع مخصص / للتحديد')
        self.fields['service'].error_messages['invalid_choice'] = bilingual('Choisissez un service disponible.', 'اختر خدمة متاحة.')
        for name, autocomplete in [('name', 'name'), ('email', 'email'), ('company', 'organization'), ('phone', 'tel')]:
            self.fields[name].widget.attrs['autocomplete'] = autocomplete
        for name in ['email', 'phone']:
            self.fields[name].widget.attrs['dir'] = 'ltr'

    def clean_brief(self):
        brief = self.cleaned_data['brief'].strip()
        if len(brief) < 20:
            raise forms.ValidationError(bilingual('Décrivez votre projet en au moins 20 caractères.', 'صف مشروعك في 20 حرفاً على الأقل.'))
        return brief
