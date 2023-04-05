from django.contrib.sitemaps import Sitemap
from django.urls import reverse as url_reverse
from .models import Event, Page

class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Event.objects.filter(status='p')

    def lastmod(self, obj):
        return obj.published_at

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.modified_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['frontend:latramoya_view', 'frontend:project_igualarte_teatro', 'frontend:event_list', 'frontend:home']

    def location(self, item):
        return url_reverse(item)
