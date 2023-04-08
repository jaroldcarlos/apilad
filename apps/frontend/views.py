from django.shortcuts import render, get_object_or_404
from django.conf import settings
from meta.views import Meta
from meta.views import MetadataMixin

from django.views.generic import TemplateView, DetailView, View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from .models import Page, Event

from apps.cookie_consent.util import get_cookie_value_from_request


def home(request):
    def _should_set_cookie() -> bool:
        if "force" in request.GET:
            return True
        cookie_value = get_cookie_value_from_request(request, "optional")
        return cookie_value is True

    current_site = get_current_site(request)
    meta = Meta(
        title = _('Asociación para la inclusión laboral y la atención a la diversidad'),
        description = 'El objetivo principal de la Asociación es especialmente la atención a la plena inclusión social y laboral de las personas con discapacidad intelectual.',
        keywords=['diversidad', 'asociación sin ánimo de lucro', 'inclusión', 'teatro', 'APILAD'],
        use_sites=True,
        image='frontend/images/logo.jpeg',
        extra_props={
            'designer': 'ecDesignStudio',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {
        'meta':meta,
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None,
    }
    template_name = 'frontend/home.html'
    response = render(request, template_name, context)

    if _should_set_cookie():
        val = "optional cookie set from django"
        response.set_cookie("optional_test_cookie", val)

    return response


def project_igualarte_teatro(request):
    current_site = get_current_site(request)
    meta = Meta(
        title = _('IgualArte: Teatro e inclusión, uno de los proyectos de APILAD'),
        description =  'El Proyecto IgualArte: Teatro e Inclusión es una herramienta para aprender, desarrollar y demostrar que el Teatro es un elemento fundamental para la transformación personal y social en el ámbito de la diversidad intelectual',
        keywords=['diversidad', 'asociación sin ánimo de lucro', 'inclusión', 'teatro', 'APILAD'],
        use_sites=True,
        image='frontend/images/logo.jpeg',
        extra_props={
            'designer': 'ecDesignStudio',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {
        'meta':meta,
    }
    return render(request, 'frontend/project/igualarte-teatro.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    meta = Meta(
        title = event.meta_title,
        description = event.meta_description,
        keywords=f'[{event.meta_keywords}]',
        use_sites=True,
        image=event.image.url if event.image else 'frontend/images/logo.jpeg',
        extra_props={
            'designer': 'ecDesignStudio',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {
        'meta':meta,
        'event':event
    }
    template_name = 'frontend/page/event_view.html'
    return render(request, template_name, context)

def my_custom_page_not_found_view(request, exception):
    return render (request, 'errors/404.html', {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})

class PageDetailView(DetailView):
    model = Page
    template_name = 'frontend/page.html'

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context

def latramoya_view(request):
    meta = Meta(
        title = _('La Tramoya, historia de un centro Ocupacional de Madrid'),
        description = 'La Tramoya surge en 1992 como una actividad terapéutica e inclusiva dentro de un Centro Ocupacional',
        keywords='actividad, terapéutica, centro òcupacional, teatro',
        use_sites=True,
        image='frontend/images/logo.jpeg',
        extra_props={
            'designer': 'ecDesignStudio',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {
        'meta':meta,
    }
    return render(request, 'frontend/page/tramoya.html', context)


def event_list(request):
    meta = Meta(
        title = _('Listado de eventos de la Asociación APILAD'),
        description = 'La página de listado de eventos ofrece una amplia variedad de opciones para explorar y participar en eventos emocionantes.',
        keywords=['actividad', 'terapéutica', 'centro ocupacional', 'teatro'],
        use_sites=True,
        image='frontend/images/logo.jpeg',
        extra_props={
            'designer': 'ecDesignStudio',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    event_list = Event.objects.exclude(status__in={'o','d'})
    if not event_list:
        return redirect('frontend:home')
    context = {
        'event_list':event_list,
        'meta': meta
    }
    template_name = 'frontend/page/event_list.html'
    return render(request, template_name, context)
