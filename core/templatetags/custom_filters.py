import locale
import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from core.utils import humanreadable_timedelta as hrt

register = template.Library()


#########################################
#     ____  _____ ____  _   _  ____     #
#    |  _ \| ____| __ )| | | |/ ___|    #
#    | | | |  _| |  _ \| | | | |  _     #
#    | |_| | |___| |_) | |_| | |_| |    #
#    |____/|_____|____/ \___/ \____|    #
#                                       #
#########################################
@register.filter
def pdb(element):
    import pdb
    pdb.set_trace()
    return element


##############################################################
#     _   _ ____   ____ ____      _    ____  _____ ____      #
#    | | | |  _ \ / ___|  _ \    / \  |  _ \| ____/ ___|     #
#    | | | | |_) | |  _| |_) |  / _ \ | | | |  _| \___ \     #
#    | |_| |  __/| |_| |  _ <  / ___ \| |_| | |___ ___) |    #
#     \___/|_|    \____|_| \_\/_/   \_\____/|_____|____/     #
#                                                            #
##############################################################
@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)


@register.filter(name='range')
def filter_range(start, end):
    return range(int(start), int(end))


@register.filter
def lookup(d, key):
    return d[key]


@register.filter(name='get_type', is_safe=False)
def get_type(value):
    t = type(value)
    return t.__module__ + "." + t.__name__


###############################################
#     _____ ___  ____  __  __    _  _____     #
#    |  ___/ _ \|  _ \|  \/  |  / \|_   _|    #
#    | |_ | | | | |_) | |\/| | / _ \ | |      #
#    |  _|| |_| |  _ <| |  | |/ ___ \| |      #
#    |_|   \___/|_| \_\_|  |_/_/   \_\_|      #
#                                             #
###############################################
@register.filter(name='pretty_json')
def pretty_json(json_text):
    try:
        pretty_json_text = json.dumps(json_text, indent=4)
        return pretty_json_text
    except Exception:
        return json_text


@register.filter
def currency(value):
    if not value:
        value = 0
    return '{} €'.format(
        locale.currency(value, symbol=False)
    )


@register.filter(name='humanreadable', is_safe=True)
def humanreadable_timedelta(
        theDateAndTime,
        precise=False,
        complete=False,
        fromDate=None):

    return hrt(theDateAndTime, precise=False, complete=False, fromDate=None)


@register.filter()
def link(value, variant=None):

    if variant == 'phone':
        url = value

        for ch in ['(', ')', ' ']:
            url.replace(ch,'')

        if '+' in url:
            url.replace('+', '00')

        url = '0034' + url if not '00' in url[0:2] else url

        return mark_safe('<a href="tel:{}">{}</a>'.format(url, value))

    elif variant == 'email':
        return mark_safe('<a href="mailto:{}">{}</a>'.format(value, value))

    elif variant == 'http':
        return mark_safe('<a href="//{}">{}</a>'.format(value, value))

    elif variant == 'blank':
        return mark_safe(
            '<a href="{}" target="_BLANK">{}</a>'.format(value, value)
        )

    else:
        return mark_safe(
            '<a href="{}">{}</a>'.format(value, value)
        )



