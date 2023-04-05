import cssutils

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils.html import mark_safe


register = template.Library()


_styles = None


@register.simple_tag()
def style(names):
    global _styles
    if _styles is None or settings.DEBUG:
        _load_styles()

    style = ';'.join(_styles.get(name, '') for name in names.split())
    return mark_safe(f'style="{style}"')


def _load_styles():
    global _styles
    _styles = {}

    sheet = cssutils.parseFile(finders.find('email/email_styles.css'))
    for rule in sheet.cssRules:
        for selector in rule.selectorList:
            _styles[selector.selectorText] = rule.style.cssText


