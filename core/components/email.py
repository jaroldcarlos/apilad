##########################################
#     _____ __  __    _    ___ _         #
#    | ____|  \/  |  / \  |_ _| |        #
#    |  _| | |\/| | / _ \  | || |        #
#    | |___| |  | |/ ___ \ | || |___     #
#    |_____|_|  |_/_/   \_\___|_____|    #
#                                        #
##########################################

SERVER_EMAIL = f'noreply@{SERVER_DOMAIN}'
CONTACT_EMAIL = f'info@{SERVER_DOMAIN}'

ADMINS = [
    ('Developer', 'django@ecdesign.es')
]

MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = SERVER_DOMAIN
DEFAULT_FROM_EMAIL = f'noreply@{SERVER_DOMAIN}'
EMAIL_HOST_USER = f'noreply@{SERVER_DOMAIN}'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default='not_set')

EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
