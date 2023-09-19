import re

from django.conf import settings
from django import template
from django.template import Node, TemplateSyntaxError
from django.utils.translation import gettext as _
from django.utils.http import urlencode
from core.utils import currency


register = template.Library()



###############################################
#     _____ ___  ____  __  __    _  _____     #
#    |  ___/ _ \|  _ \|  \/  |  / \|_   _|    #
#    | |_ | | | | |_) | |\/| | / _ \ | |      #
#    |  _|| |_| |  _ <| |  | |/ ___ \| |      #
#    |_|   \___/|_| \_\_|  |_/_/   \_\_|      #
#                                             #
###############################################
@register.simple_tag(name="currency")
def currency_tag(value):
    return currency(value)


@register.simple_tag(name="pprint")
def pprint_tag(value):
    return value

##############################################################
#     _   _ ____   ____ ____      _    ____  _____ ____      #
#    | | | |  _ \ / ___|  _ \    / \  |  _ \| ____/ ___|     #
#    | | | | |_) | |  _| |_) |  / _ \ | | | |  _| \___ \     #
#    | |_| |  __/| |_| |  _ <  / ___ \| |_| | |___ ___) |    #
#     \___/|_|    \____|_| \_\/_/   \_\____/|_____|____/     #
#                                                            #
##############################################################
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag(name='verbose_name')
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()


class SetVarNode(template.Node):
    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = self.new_val
        return ''


@register.tag
def setvar(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise(
            template.TemplateSyntaxError,
            "{} tag requires arguments".format(token.contents.split()[0])
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise(
            template.TemplateSyntaxError,
            "{} tag had invalid arguments".format(tag_name)
        )
    new_val, var_name = m.groups()
    if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
        raise(
            template.TemplateSyntaxError,
            "{} tag's argument should be in quotes".format(tag_name)
        )
    return SetVarNode(new_val[1:-1], var_name)


class SetVariable(template.Node):
    def __init__(self, varname, value, is_string=False):
        self.varname = varname
        self.value = value
        self.is_string = is_string

    def render(self, context):
        if self.is_string or not context[self.value]:
            context[self.varname] = self.value
        else:
            context[self.varname] = context[self.value]
        return ''


@register.tag('set_var')
def set_var(parser, token):
    """
    Set value to variable. If value is object or variable
    copy pointer of that object/variable to new variable.

        {% set_var variable value %}

    Set string to variable.
        {% set_var variable "new string" %}
    """

    from re import split
    bits = split(r'\s+', token.contents, 2)
    if bits[2][:1] in '"\'' and bits[2][-1:] in '"\'':
        return SetVariable(bits[1], bits[2][1:-1], True)

    return SetVariable(bits[1], bits[2])


class CaptureNode(Node):
    def __init__(self, nodelist, varname, silent):
        self.nodelist = nodelist
        self.varname = varname
        self.silent = silent

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        if self.silent:
            return ''
        else:
            return output


@register.tag(name='capture')
def do_capture(parser, token):
    """
    Capture the contents of a tag output.
    Usage:
    .. code-block:: html+django
        {% capture %}..{% endcapture %}                    # output in {{ capture }}
        {% capture silent %}..{% endcapture %}             # output in {{ capture }} only
        {% capture as varname %}..{% endcapture %}         # output in {{ varname }}
        {% capture as varname silent %}..{% endcapture %}  # output in {{ varname }} only
    For example:
    .. code-block:: html+django
        {# Allow templates to override the page title/description #}
        <meta name="description" content="{% capture as meta_description %}{% block meta-description %}{% endblock %}{% endcapture %}" />
        <title>{% capture as meta_title %}{% block meta-title %}Untitled{% endblock %}{% endcapture %}</title>
        {# copy the values to the Social Media meta tags #}
        <meta property="og:description" content="{% block og-description %}{{ meta_description }}{% endblock %}" />
        <meta name="twitter:title" content="{% block twitter-title %}{{ meta_title }}{% endblock %}" />
    """
    bits = token.split_contents()

    # tokens
    t_as = 'as'
    t_silent = 'silent'
    var = 'capture'
    silent = False

    num_bits = len(bits)
    if len(bits) > 4:
        raise TemplateSyntaxError("'capture' node supports '[as variable] [silent]' parameters.")
    elif num_bits == 4:
        t_name, t_as, var, t_silent = bits
        silent = True
    elif num_bits == 3:
        t_name, t_as, var = bits
    elif num_bits == 2:
        t_name, t_silent = bits
        silent = True
    else:
        var = 'capture'
        silent = False

    if t_silent != 'silent' or t_as != 'as':
        raise TemplateSyntaxError("'capture' node expects 'as variable' or 'silent' syntax.")

    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    return CaptureNode(nodelist, var, silent)


####################################
#     __  __    _  _____ _   _     #
#    |  \/  |  / \|_   _| | | |    #
#    | |\/| | / _ \ | | | |_| |    #
#    | |  | |/ ___ \| | |  _  |    #
#    |_|  |_/_/   \_\_| |_| |_|    #
#                                  #
####################################
@register.simple_tag()
def mul(value1, value2):
    return value1 * value2


@register.simple_tag()
def div(value1, value2):
    return value1 / value2


@register.simple_tag()
def sub(value1, value2):
    return value1 - value2


@register.inclusion_tag('templatetags/picture.html')
def picture(url=None, format='default', alt=None, css_class=None):
    settings_formats = settings.THUMBNAIL_FORMATS
    sizes = settings_formats.get(
        format.strip(),
        None
    )
    context = {
        'url': url,
        'sizes': sizes,
        'alt': alt,
        'class': css_class
    }
    return context


@register.simple_tag(takes_context=True)
def url_whatsapp(context):
    request = context['request']
    whatsapp_api_url = 'https://api.whatsapp.com/send'
    text = _('Hola, me interesaría información sobre APILAD')

    text += ".\r\n\r\n"
    params = {
        'phone': '+34602542505',
        'text': text
    }
    url = '{api_url}?{params}'.format(
        api_url=whatsapp_api_url,
        params=urlencode(params)
    )
    return url
