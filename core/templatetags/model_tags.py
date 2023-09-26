from django import template
from dynamic_preferences.registries import global_preferences_registry

from django.conf import settings

from apps.frontend.models import Event, Promotion

register = template.Library()

@register.inclusion_tag('templatetags/upcoming_events.html')
def upcoming_events():
    events = Event.published.all().order_by('published_at')
    context = {
        'events':events
    }
    return context

@register.inclusion_tag('templatetags/promotion_sidebar.html')
def promotion_sidebar():
    promotions = Promotion.actives.all()
    context = {
        'promotions':promotions
    }
    return context