"""
Django settings for ideam_cdc project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$1%5%5d+d5*zzi!f4h#$rqx@rvzo@h)mnfmze-fsn-6wg(=&tv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.106.11']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'public',
	'django.contrib.sites',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'user_profile',
	'storage',
	'algorithm',
	'execution',
	'template',
	'ingest',
	'rest_framework',
	'ingest_template',
]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ideam_cdc.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			BASE_DIR + '/templates/',
		],
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

WSGI_APPLICATION = 'ideam_cdc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {'default': dj_database_url.parse(os.environ.get('IDEAM_PRODUCTION_DATABASE_URL'))}
if DEBUG:
	DATABASES = {'default': dj_database_url.parse(os.environ.get('IDEAM_DATABASE_URL'))}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root')
STATIC_URL = '/static_dirs/'


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
	os.path.join(PROJECT_ROOT, 'static_dirs'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Allauth configuration

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
ACCOUNT_SIGNUP_FORM_CLASS = 'user_profile.forms.SignupForm'
LOGIN_REDIRECT_URL = '/home/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_ADAPTER = 'user_profile.adapters.MyAccountAdapter'

# Sendgrid

EMAIL_HOST = os.environ.get('IDEAM_MAIL_HOST')
EMAIL_HOST_USER = os.environ.get('IDEAM_MAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('IDEAM_MAIL_PASSWORD')
EMAIL_PORT = os.environ.get('IDEAM_MAIL_PORT')
EMAIL_USE_TLS = True

# CDCOL Parameters

STORAGE_UNIT_DIRECTORY_PATH = os.environ.get('IDEAM_STORAGE_UNIT_DIRECTORY_PATH')
DC_STORAGE_PATH = os.environ.get('IDEAM_DC_STORAGE_PATH')
WEB_STORAGE_PATH = os.environ.get('IDEAM_WEB_STORAGE_PATH')
API_URL = os.environ.get('IDEAM_API_URL')

# STATIC Files Part 2

MEDIA_ROOT = os.path.join(WEB_STORAGE_PATH, 'media_root')
MEDIA_URL = '/static_media_dirs/'
