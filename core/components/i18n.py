from django.utils.translation import gettext_lazy

#############################
#     ___ _  ___  _   _     #
#    |_ _/ |( _ )| \ | |    #
#     | || |/ _ \|  \| |    #
#     | || | (_) | |\  |    #
#    |___|_|\___/|_| \_|    #
#                           #
#############################
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('es', gettext_lazy('Español')),
    ('en', gettext_lazy('English')),
)
LOCALE_PATHS = (BASE_DIR / 'locale', )
