ALLOWED_HOSTS = [
    '*',
]

INTERNAL_IPS = [
    '*',
    "127.0.0.1"
]

# Databases
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'db.sqlite3',
#    }
#}

# Email configuration
SERVER_EMAIL = 'noreply@ecdesign.es'
ADMINS = [
    ('Developer', 'info@ecdesign.es')
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
