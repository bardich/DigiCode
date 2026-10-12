from django import template
from django.utils.translation import get_language
from apps.core.utils import whatsapp_url
from django.utils.html import escape
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def text(fr, ar):
    value = ar if get_language() == 'ar' else fr
    return mark_safe(escape(value).replace('&lt;br&gt;', '<br>'))

@register.simple_tag
def whatsapp(number, message=''):
    return whatsapp_url(number, message)
