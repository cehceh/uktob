"""
Django settings for my_site project.

Generated by 'django-admin startproject' using Django 4.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import datetime
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


if DEBUG:
    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
else:
    ALLOWED_HOSTS = ['my_site.com']  #* In production if we have a site server name


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #* 3rd party 
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    # 'rest_framework_swagger',
    'debug_toolbar',         # new

    #* My Apps
    'apps.authentication.apps.AuthenticationConfig'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'my_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {

    'default': env.db_url(
        'SQLITE_URL',
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media Dirs
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#* 
AUTHENTICATION_BACKENDS = [
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'apps.authentication.apis.serializers.CustomRegisterSerializer',
}
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'apps.authentication.apis.serializers.CustomLoginSerializer',
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],

    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=90),
}

#* important to fix that issue ("Site matching query does not exist.")
SITE_ID = 1

ACCOUNT_ADAPTER = 'apps.authentication.adapter.CustomAccountAdapter'

AUTH_USER_MODEL = 'authentication.CustomUser'

ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'none'


if DEBUG: #* on local
    CORS_REPLACE_HTTPS_REFERER      = False
    HOST_SCHEME                     = "http://"
    SECURE_PROXY_SSL_HEADER         = None
    SECURE_SSL_REDIRECT             = False
    SESSION_COOKIE_SECURE           = False
    CSRF_COOKIE_SECURE              = False
    SECURE_HSTS_SECONDS             = None
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
    SECURE_FRAME_DENY               = False
else: #* on production
    # Let's Encrypt ssl/tls https
    CORS_REPLACE_HTTPS_REFERER      = True
    HOST_SCHEME                     = "https://"
    SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT             = True
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
    SECURE_HSTS_SECONDS             = 1000000
    SECURE_FRAME_DENY               = True

