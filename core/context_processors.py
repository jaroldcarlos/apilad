import re

from django import db
from django.contrib.sites.shortcuts import get_current_site

from apps.frontend.models import Promotion

def custom_context(request):
    '''Custom context processor for the frontend app'''
    mobile_re = re.compile(
        r".*(iphone|mobile|androidtouch)",
        re.IGNORECASE
    )
    if mobile_re.match(request.META['HTTP_USER_AGENT']):
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
