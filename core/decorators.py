from functools import wraps

from django.conf import settings
from django.contrib import messages

import requests

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': request.POST.get('g-recaptcha-response')
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
