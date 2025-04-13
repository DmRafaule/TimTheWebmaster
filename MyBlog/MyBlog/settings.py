"""
Django settings for MyBlog project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-da4fk(86vwdw7^kre!viz_3n2)80i7jon^-50=@8+18-@45f@5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    # model translation
    'modeltranslation',
    ###
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # captcha
    'captcha',
    ###
    'Main.apps.MainConfig',
    'Admin.apps.AdminConfig',
    'WebGLEngine.apps.WebglengineConfig',
    'Post.apps.PostConfig',
    'PostFilter.apps.PostfilterConfig',
    'PostEditor.apps.PostEditorConfig',
    'PagiScroll.apps.PagiscrollConfig',
    'PagiScrollEditor.apps.PagiscrolleditorConfig',
    'Engagement.apps.EngagementConfig',
    'Breadcrumbs.apps.BreadcrumbsConfig',
    'ImageThief.apps.ImagethiefConfig',
    'RSSAggregator.apps.RssaggregatorConfig',
    'ShaderToy.apps.ShadertoyConfig',
    # Django-Cleanup
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'Engagement.middleware.EngagementMiddleware',
    'Breadcrumbs.middleware.BreadcrumbsMiddleware',
    'PostFilter.middleware.PostFilterMiddleware',
    'PagiScrollEditor.middleware.PagiScrollEditorMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'media/'),
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


WSGI_APPLICATION = 'MyBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CSRF_USE_SESSIONS = True
SESSION_SAVE_EVERY_REQUEST = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LANGUAGES = [
        ("ru", _("Русский")),
        ("en", _("Английский")),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = "ru"


# For email sending 
DEFAULT_FROM_EMAIL = 'timachuduk@timthewebmaster.com'
DEFAULT_TO_EMAIL = 'timachuduk@gmail.com'
EMAIL_HOST = 'smtp.beget.com'
EMAIL_PORT = 25 
EMAIL_HOST_USER = 'timachuduk@timthewebmaster.com' # Maybe change to timachuduk@timthewebmaster.com
EMAIL_HOST_PASSWORD = 'EXNIkq1&yfOx'
