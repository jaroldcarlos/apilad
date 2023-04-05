#########################################################################
#    _____ _   _ ___ ____  ____    ____   _    ____ _______   __
#   |_   _| | | |_ _|  _ \|  _ \  |  _ \ / \  |  _ \_   _\ \ / /
#     | | | |_| || || |_) | | | | | |_) / _ \ | |_) || |  \ V /
#     | | |  _  || ||  _ <| |_| | |  __/ ___ \|  _ < | |   | |
#     |_| |_| |_|___|_| \_\____/  |_| /_/   \_\_| \_\|_|   |_|
#
#########################################################################

DYNAMIC_PREFERENCES = {
    'MANAGER_ATTRIBUTE': 'preferences',
    'REGISTRY_MODULE': 'dynamic_preferences_registry',
    'ADMIN_ENABLE_CHANGELIST_FORM': False,
    'SECTION_KEY_SEPARATOR': '__',
    'ENABLE_GLOBAL_MODEL_AUTO_REGISTRATION': True,
    'ENABLE_CACHE': True,
    'VALIDATE_NAMES': True,
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Table'],
            ['RemoveFormat', 'Source']
        ]
    }
}


########################################
#     _____ _____ ____ _____ ____      #
#    |_   _| ____/ ___|_   _/ ___|     #
#      | | |  _| \___ \ | | \___ \     #
#      | | | |___ ___) || |  ___) |    #
#      |_| |_____|____/ |_| |____/     #
#                                      #
########################################
# easy-thumbnails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

THUMBNAIL_FORMATS = {
    'default': {
        's':    {'screen':'max-width:544px',  'size': '300',    'crop': 'center'},
        'm':    {'screen':'min-width:545px',  'size': '545',    'crop': 'center'},
        'l':    {'screen':'min-width:769px',  'size': '769',    'crop': 'center'},
        'xl':   {'screen':'min-width:1200px', 'size': '993',    'crop': 'center'},
        'xxl':  {'screen':'min-width:1920px', 'size': '1201',   'crop': 'center'}
    },
    'logo': {
        's': {'screen':'max-width:544px', 'size': '80',   'crop': 'center'},
        'm': {'screen':'min-width:769px', 'size': '120',   'crop': 'center'},
        'l': {'screen':'min-width:1200px','size': '150', 'crop': 'center'}
    }
}


META_SITE_PROTOCOL = 'http' if DEBUG else 'https'
META_SITE_DOMAIN = SERVER_DOMAIN
META_USE_TITLE_TAG = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_SCHEMAORG_PROPERTIES = True


if DEBUG:
    RECAPTCHA_PUBLIC_KEY  = config('RECAPTCHA_PUBLIC_KEY_DEBUG')
    RECAPTCHA_PRIVATE_KEY  = config('RECAPTCHA_PRIVATE_KEY_DEBUG')
else:
    RECAPTCHA_PUBLIC_KEY  = config('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY  = config('RECAPTCHA_PRIVATE_KEY')

