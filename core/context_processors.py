# import git
import re

from django import db
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import resolve

from apps.frontend.models import Promotion

def custom_context(request):
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)",
        re.IGNORECASE
    )
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        mobile = True
    else:
        mobile = False
    database_name = db.utils.settings.DATABASES['default']['NAME']
    current_site = get_current_site(request)
    promotions = Promotion.actives.all()

    context = {
        'database_name': database_name,
        'mobile': mobile,
        'app_name': current_site.name,
        'app_domain': current_site.domain,
        'view_promotion': True if promotions.count() > 0 else False,
    }
    return context
