
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from core.test import test
from apps.backend.views import register
from apps.frontend.sitemap import EventSitemap, PageSitemap, StaticViewSitemap

handler404 = 'apps.frontend.views.my_custom_page_not_found_view'
handler403 = 'apps.frontend.views.custom_permission_denied_view'
handler400 = 'apps.frontend.views.custom_bad_request_view'
handler500 = 'apps.frontend.views.custom_error_view'

sitemaps = {
    'events': EventSitemap,
    'pages': PageSitemap,
    'static': StaticViewSitemap
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('blog/', include('apps.blog.urls')),
    path('contact/', include('apps.contact.urls')),
    path('backend/', include('apps.backend.urls')),
    path('tests/', test, name='tests'),
    path('', include('apps.frontend.urls')),
    path("cookies/", include("apps.cookie_consent.urls")),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [path('rosetta/', include('rosetta.urls'))]

if 'dynamic_preferences' in settings.INSTALLED_APPS:
    urlpatterns += [path('preferences/', include('dynamic_preferences.urls'))]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    