"""
Django settings for mms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jn+d(o)cl04(s9jkr!hmlwj6$!)*mk$&7jm)ick%8co)57i&7u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'ir',
		'ik',
		'ikr',
		)

MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		)

ROOT_URLCONF = 'mms.urls'

WSGI_APPLICATION = 'mms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'mms',
			'USER': 'hurrman',
			'PASSWORD': 'art319',
			'HOST': 'localhost',
			'PORT': '3306',
			}
		}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'Asia/Shanghai'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')

STATICFILES_DIRS = (
		os.path.join(BASE_DIR, 'ir', 'statics'),
		os.path.join(BASE_DIR, 'ik', 'statics'),
		os.path.join(BASE_DIR, 'ikr', 'statics'),
		)

MEDIA_URL = '/media/'
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')

TEMPLATE_DIRS = (
		os.path.join(BASE_DIR, 'templates'),
		os.path.join(BASE_DIR, 'ir', 'templates'),
		os.path.join(BASE_DIR, 'ik', 'templates'),
		os.path.join(BASE_DIR, 'ikr', 'templates'),
		)
