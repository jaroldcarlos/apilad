#################################################################
#     ____    _  _____  _    ____    _    ____  _____ ____      #
#    |  _ \  / \|_   _|/ \  | __ )  / \  / ___|| ____/ ___|     #
#    | | | |/ _ \ | | / _ \ |  _ \ / _ \ \___ \|  _| \___ \     #
#    | |_| / ___ \| |/ ___ \| |_) / ___ \ ___) | |___ ___) |    #
#    |____/_/   \_\_/_/   \_\____/_/   \_\____/|_____|____/     #
#                                                               #
#################################################################
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('BD_NAME'),
        'USER': config('BD_USER'),
        'PASSWORD': config('BD_PASS'),
        'HOST': config('BD_HOST'),
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },

}

if DEBUG:
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    