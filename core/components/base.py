
from pathlib import Path
from decouple import config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


##################################################################
#    __     ___    ____  ___    _    ____  _     _____ ____      #
#    \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____/ ___|     #
#     \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _| \___ \     #
#      \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ ___) |    #
#       \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|____/     #
#                                                                #
##################################################################

BASE_DIR = Path(__file__).resolve().parent.parent
SERVER_DOMAIN = config('SERVER_DOMAIN', default='localhost')

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


###################################
#     _   _ ____  _     ____      #
#    | | | |  _ \| |   / ___|     #
#    | | | | |_) | |   \___ \     #
#    | |_| |  _ <| |___ ___) |    #
#     \___/|_| \_\_____|____/     #
#                                 #
###################################
ALLOWED_HOSTS = [SERVER_DOMAIN, ]
INTERNAL_IPS = [SERVER_DOMAIN, "127.0.0.1"]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

#####################################
#        _    ____  ____  ____      #
#       / \  |  _ \|  _ \/ ___|     #
#      / _ \ | |_) | |_) \___ \     #
#     / ___ \|  __/|  __/ ___) |    #
#    /_/   \_\_|   |_|   |____/     #
#                                   #
#####################################
DJANGO_APPS = [
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
THIRDPARTY_APPS_DEV = [
    'debug_toolbar',
    'django_extensions',
    'django_admin_generator',
]
THIRDPARTY_APPS = [
    'dynamic_preferences',
    'crispy_forms',
    'render_block',
    'rosetta',
    'sorl.thumbnail',
    'ckeditor',
    'meta',
    #'corsheaders'
]
LOCAL_APPS = [
    'apps.cookie_consent',
    'apps.backend',
    'apps.frontend',
    'apps.contact',
    'apps.blog',
]
LAST_APP = [
    'django_cleanup.apps.CleanupConfig',
]

if DEBUG:
    THIRDPARTY_APPS = THIRDPARTY_APPS_DEV + THIRDPARTY_APPS

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + LOCAL_APPS + LAST_APP

SITE_ID = 1

##########################################################################
#     __  __ ___ ____  ____  _     _______        ___    ____  _____     #
#    |  \/  |_ _|  _ \|  _ \| |   | ____\ \      / / \  |  _ \| ____|    #
#    | |\/| || || | | | | | | |   |  _|  \ \ /\ / / _ \ | |_) |  _|      #
#    | |  | || || |_| | |_| | |___| |___  \ V  V / ___ \|  _ <| |___     #
#    |_|  |_|___|____/|____/|_____|_____|  \_/\_/_/   \_\_| \_\_____|    #
#                                                                        #
##########################################################################
THIRDPARTY_MIDDLEWARE_DEV = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
THIRDPARTY_MIDDLEWARE = [
]
DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
LOCAL_MIDDLEWARE = [
    # 'core.middleware.LoginRequiredMiddleware',  # All urls login required
    'core.middleware.UserBasedExceptionMiddleware',
]

if DEBUG:
    THIRDPARTY_MIDDLEWARE = THIRDPARTY_MIDDLEWARE_DEV + THIRDPARTY_MIDDLEWARE

MIDDLEWARE = THIRDPARTY_MIDDLEWARE + DJANGO_MIDDLEWARE + LOCAL_MIDDLEWARE


##################################################################
#     _____ _____ __  __ ____  _        _  _____ _____ ____      #
#    |_   _| ____|  \/  |  _ \| |      / \|_   _| ____/ ___|     #
#      | | |  _| | |\/| | |_) | |     / _ \ | | |  _| \___ \     #
#      | | | |___| |  | |  __/| |___ / ___ \| | | |___ ___) |    #
#      |_| |_____|_|  |_|_|   |_____/_/   \_\_| |_____|____/     #
#                                                                #
##################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'dynamic_preferences.processors.global_preferences',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.custom_context',
            ],
            'libraries':{
                'custom_filters': 'core.templatetags.custom_filters',
                'custom_tags': 'core.templatetags.custom_tags',
                'email_tags': 'core.templatetags.email_tags',
                'model_tags': 'core.templatetags.model_tags',
                'instagram_tags': 'core.templatetags.instagram_tags'
            }
        },
    },
]


###################################################################
#     ____   _    ____ ______        _____  ____  ____  ____      #
#    |  _ \ / \  / ___/ ___\ \      / / _ \|  _ \|  _ \/ ___|     #
#    | |_) / _ \ \___ \___ \\ \ /\ / / | | | |_) | | | \___ \     #
#    |  __/ ___ \ ___) |__) |\ V  V /| |_| |  _ <| |_| |___) |    #
#    |_| /_/   \_\____/____/  \_/\_/  \___/|_| \_\____/|____/     #
#                                                                 #
###################################################################
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTH_USER_MODEL = 'backend.User'

#########################################################################
#     ____ _____  _  _____ ___ ____   __  __ _____ ____ ___    _        #
#    / ___|_   _|/ \|_   _|_ _/ ___| |  \/  | ____|  _ \_ _|  / \       #
#    \___ \ | | / _ \ | |  | | |     | |\/| |  _| | | | | |  / _ \      #
#     ___) || |/ ___ \| |  | | |___  | |  | | |___| |_| | | / ___ \     #
#    |____/ |_/_/   \_\_| |___\____| |_|  |_|_____|____/___/_/   \_\    #
#                                                                       #
#########################################################################
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '..' / 'public_html' / 'static'

MEDIA_URL = '/media/'

if not DEBUG:
    MEDIA_ROOT = BASE_DIR / '..' / 'public_html' / 'media'
else:
    MEDIA_ROOT = BASE_DIR / 'media'


STATICFILES_DIRS = (
    BASE_DIR / 'static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
