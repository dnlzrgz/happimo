"""
Django settings for happimo project.
"""

from pathlib import Path
from environs import Env

# Read environment variables
env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    "django-insecure-&*5$6q%@%+$43rb)adunu3ao&myzyu!y*3o(^ra7*m1&n!o-p^",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool(
    "DEBUG",
    False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    [],
)

ADMIN_URL = env.str(
    "ADMIN_URL",
    "admin/",
)

INTERNAL_IPS = [
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    # 1st party
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Static files
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # django-allauth
    "allauth",
    "allauth.account",
    # Debug
    "debug_toolbar",
    "django_browser_reload",
    # Local
    "accounts",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "happimo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "happimo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# https://whitenoise.readthedocs.io/en/latest/

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom user accounts
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/

AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = env.str(
    "LOGIN_REDIRECT_URL",
    "home",
)

LOGOUT_REDIRECT_URL = env.str(
    "LOGOUT_REDIRECT_URL",
    "home",
)


# Allauth config
# https://docs.allauth.org/en/latest/index.html

ACCOUNT_EMAIL_REQUIRED = env.bool(
    "ACCOUNT_EMAIL_REQUIRED",
    True,
)

ACCOUNT_USERNAME_REQUIRED = env.bool(
    "ACCOUNT_USERNAME_REQUIRED",
    False,
)

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = env.bool(
    "ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE",
    True,
)

ACCOUNT_SESSION_REMEMBER = env.bool(
    "ACCOUNT_SESSION_REMEMBER",
    True,
)

ACCOUNT_AUTHENTICATION_METHOD = env.str(
    "ACCOUNT_AUTHENTICATION_METHOD",
    "email",
)

ACCOUNT_UNIQUE_EMAIL = env.bool(
    "ACCOUNT_UNIQUE_EMAIL",
    True,
)


# Email
# https://docs.djangoproject.com/en/5.0/topics/email

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)


# Logging
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}
