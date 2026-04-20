from modeltranslation.translator import translator, TranslationOptions
from .models import Service


class ServiceTranslationOptions(TranslationOptions):
    fields = (
        'title_fr',
        'title_ar',
        'short_description_fr',
        'short_description_ar',
        'full_description_fr',
        'full_description_ar',
        'benefits_fr',
        'benefits_ar',
        'meta_title_fr',
        'meta_title_ar',
        'meta_description_fr',
        'meta_description_ar',
    )


# Note: modeltranslation requires the fields to be named differently
# We'll use a custom approach in the model
