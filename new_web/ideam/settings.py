"""
Django settings for ideam project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(!l@d8u0fco6b+m&vr6i&&@c@ne_a%2+@hmi5*5o=p7ic*@6)!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# WEB VARIABLES

"""
Datacube REST API URL
The web app interact with the datacube API 
to perform some tasks.
"""
DC_API_URL = 'http://api:8000'

"""
The datacube storage:
* Keep the product (satelite) metadata file (yaml)
* Ingestion metadata file (yaml)
* Image metadata generation script (.py)

the dc_storage may contain a folder for each product:}

Example:

dc_storage/
    LS7_ETM_LEDAPS/
        ingest_file.yml
        description_file.yml
        mgen_script.py
    LS8_OLI_LEDAPS/
        ingest_file.yml
        description_file.yml
        mgen_script.py
"""
DC_STORAGE_PATH = '/dc_storage'

"""
The web storage will contains:
    - algorithms: Algorithm versions uploaded by the user thorugh this web app.
    - dags: Dags created by the user an stored manually.
    - logs: 
    - plugins:
    - thumbnails: preview of satelite imagery.
    - input: Contains the input data for each execution perfomed.
    - results: The exectuion results will be placed here.
    - template (new): The .yaml product confguration and ingestion files and also 
        the image metadata generation script for each product (satelite).

"""
WEB_STORAGE_PATH = '/web_storage'

"""
Execution module in the web pages is refreshed with javascritp 
each number of seconds specified on this variables.
"""
WEB_EXECUTION_TEMPORIZER = 10


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # `allauth` needs this from django
    'django.contrib.sites',

    # `allauth`
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework_datatables',

    'bootstrap3',

    'index',
    'user_profile',
    'execution',
    'algorithm',
    'storage',
    'template',
    'ingest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ideam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ideam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'web_db',
        'PORT': '5432',
        'NAME': 'cdcol',
        'USER': 'cdcol',
        'PASSWORD': 'cdcol'
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'j \d\e F,Y'

DATETIME_FORMAT = 'j \d\e F,Y H:i:s'

TIME_FORMAT = 'H:i:s'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    # When debugging
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

if not DEBUG:
    # For deployment
    STATIC_ROOT = os.path.join(
        BASE_DIR, "static"
    )


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = WEB_STORAGE_PATH

# `allauth`
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# `allauth`
SITE_ID = 1

# User registration form.
# A custom template is required in templates/account/signup.html
ACCOUNT_SIGNUP_FORM_CLASS = 'user_profile.forms.SignupForm'
LOGIN_REDIRECT_URL = '/index/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_ADAPTER = 'user_profile.adapters.MyAccountAdapter'

# Email service
# this variables are needed for 'allouth' to perform password reset 
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "aucarvideo@gmail.com"
EMAIL_HOST_PASSWORD = "aucar2018"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True

# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    # django-rest-framework-datatables
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
        # 'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    #  The page size is driven by the datatable in the html 
    'PAGE_SIZE': 10,
    
}


