from backend.settings.base import *

DATABASES = {
    'default': {
        'HOST': 'localhost',
        'NAME': 'przel',
        'USER': 'przel',
        'PASSWORD': '2-arrays-Wrists-7',
    }
}

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['127.0.0.1', 'przeliczacz.pl', 'przeliczacz.co.uk']

MEDIA_ROOT = '/var/www/przel/media/'

# STATIC_ROOT = os.path.join(PROJECT_DIR, 'public/static')

