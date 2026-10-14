"""Validate trusted marketing fragments and expose inert, public-only configuration."""
import hashlib
import json
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit
from django.core.exceptions import ValidationError
from django.utils.translation import get_language

MAX_SNIPPET_BYTES = 50 * 1024
PUBLIC_ROUTES = {
    'core': {'home', 'about', 'contact', 'project_list', 'project_detail'},
    'services': {'list', 'detail', 'rental_landing', 'usedcars_landing', 'artisana_landing'},
}


def message(fr, ar):
    return ar if get_language() == 'ar' else fr


class SnippetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.scripts = []
        self.current = None
        self.fallbacks = 0

    def fail(self):
        raise ValidationError(message('Collez uniquement des balises <script> complètes et, si nécessaire, leur bloc <noscript>.', 'الصق فقط وسوم <script> كاملة وكتلة <noscript> عند الحاجة.'))

    def handle_starttag(self, tag, attrs):
        if any(name.startswith('on') for name, _ in attrs):
            self.fail()
        if not self.stack and tag == 'script':
            attributes = dict(attrs)
            if len(attributes) != len(attrs):
                self.fail()
            script_type = (attributes.get('type') or '').strip().lower()
            if script_type not in ('', 'text/javascript', 'application/javascript', 'module'):
                self.fail()
            src = attributes.get('src')
            if 'src' in attributes:
                if src is None or not src.strip() or urlsplit(src.strip()).scheme.lower() not in ('', 'http', 'https'):
                    self.fail()
            self.current = {'attributes': attributes, 'text': ''}
            self.stack.append(tag)
        elif not self.stack and tag == 'noscript':
            self.stack.append(tag)
            self.fallbacks += 1
        elif self.stack == ['noscript'] and tag in ('img', 'iframe'):
            if tag == 'iframe':
                self.stack.append(tag)
        else:
            self.fail()

    def handle_startendtag(self, tag, attrs):
        if self.stack == ['noscript'] and tag == 'img':
            self.handle_starttag(tag, attrs)
        else:
            self.fail()

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.fail()
        self.stack.pop()
        if tag == 'script':
            if not self.current['attributes'].get('src') and not self.current['text'].strip():
                self.fail()
            self.scripts.append(self.current)
            self.current = None

    def handle_data(self, data):
        if self.stack == ['script']:
            self.current['text'] += data
        elif data.strip() and not (self.stack and self.stack[0] == 'noscript'):
            self.fail()

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')

    def handle_decl(self, decl):
        self.fail()

    def handle_pi(self, data):
        self.fail()

    def unknown_decl(self, data):
        self.fail()


def parse_snippet(code):
    if not isinstance(code, str) or not code.strip():
        raise ValidationError(message('Collez un extrait de code.', 'الصق مقتطف الشفرة.'))
    if len(code.encode('utf-8')) > MAX_SNIPPET_BYTES:
        raise ValidationError(message('Un extrait ne peut pas dépasser 50 Ko.', 'لا يمكن أن يتجاوز المقتطف 50 كيلوبايت.'))
    if re.search(r'document\s*\.\s*write(?:ln)?\s*\(', code):
        raise ValidationError(message('Les extraits utilisant document.write() ne sont pas pris en charge.', 'المقتطفات التي تستخدم document.write() غير مدعومة.'))
    parser = SnippetParser()
    try:
        parser.feed(code)
        parser.close()
    except (ValueError, AssertionError):
        parser.fail()
    if parser.stack or not (parser.scripts or parser.fallbacks):
        parser.fail()
    return parser.scripts


def validate_snippet(code):
    parse_snippet(code)


def marketing_context(request):
    match = getattr(request, 'resolver_match', None)
    if not match or match.url_name not in PUBLIC_ROUTES.get(match.namespace, set()):
        return {}
    from .models import SiteSettings, MarketingSnippet
    if not SiteSettings.load().marketing_enabled:
        return {}
    snippets = []
    fingerprint_rows = []
    for snippet in MarketingSnippet.objects.filter(is_enabled=True).order_by('display_order', 'pk'):
        try:
            scripts = parse_snippet(snippet.code)
        except ValidationError:
            # Invalid direct database imports fail closed instead of breaking a public page.
            continue
        fingerprint_rows.append([snippet.pk, snippet.code, snippet.position, snippet.display_order])
        snippets.append({'position': snippet.position, 'scripts': scripts})
    if not snippets:
        return {}
    fingerprint = hashlib.sha256(json.dumps(fingerprint_rows, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    return {'marketing_config': {'fingerprint': fingerprint, 'snippets': snippets}}
