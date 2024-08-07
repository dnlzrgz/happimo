"""
Django settings for happimo project.
"""

import django
from pathlib import Path
from environs import Env

# Read environment variables
env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY",
    "django-insecure-&*5$6q%@%+$43rb)adunu3ao&myzyu!y*3o(^ra7*m1&n!o-p^",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool(
    "DEBUG",
    False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    ["*"],
)

ADMIN_URL = env.str(
    "ADMIN_URL",
    "admin/",
)

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]


# Application definition

INSTALLED_APPS = [
    # 1st party
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.forms",
    # Static files
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # django-allauth
    "allauth",
    "allauth.account",
    # Local
    "accounts",
    "moods",
    "pages",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_browser_reload",
        "silk",
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
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        "silk.middleware.SilkyMiddleware",
    ]

ROOT_URLCONF = "happimo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            django.__path__[0] + "/forms/templates",
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

DATABASE_ENGINE = env.str("DB_ENGINE", "sqlite3")
DATABASES = {}

if DATABASE_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("POSTGRES_DB"),
            "USER": env.str("POSTGRES_USER"),
            "PASSWORD": env.str("POSTGRES_PASSWORD"),
            "HOST": env.str("POSTGRES_HOST"),
            "PORT": env.str("POSTGRES_PORT", 5432),
        }
    }
elif DATABASE_ENGINE == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    raise ValueError("Invalid DATABASE_ENGINE value. Must be 'postgres' or 'sqlite3'.")


DATABASES["default"]["ATOMIC_REQUESTS"] = env.bool(
    "DATABASE_ATOMIC_REQUESTS",
    True,
)


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Cache
# https://docs.djangoproject.com/en/5.0/topics/cache/

if env.bool("USE_REDIS", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": env.str("REDIS_LOCATION", ""),
        }
    }
elif env.bool("USE_MEMCACHE", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": env.str("MEMCACHE_LOCATION", ""),
        }
    }
else:
    if DEBUG:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        }
    else:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }

CACHE_TIMEOUT_SECONDS = env.int("CACHE_TIMEOUT_SECONDS", 0)


# Sqids settings
# # https://github.com/julianwachholz/django-sqids

DJANGO_SQIDS_MIN_LENGTH = env.int("SQIDS_MIN_LENGTH", 5)

DJANGO_SQIDS_MIN_ALPHABET = env.str(
    "SQIDS_MIN_ALPHABET",
    "9FbwkL2mUvroAlcWsxi8NgGt7nDTjQMzI1Hfq6KyP0VeO5dZJCpYBaRS4Euh3X",
)


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


# Silk
# https://github.com/jazzband/django-silk

SILKY_AUTHENTICATION = env.bool("SILKY_AUTHENTICATION", True)

SILKY_AUTHORISATION = env.bool("SILKY_AUTHORISATION", True)


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
