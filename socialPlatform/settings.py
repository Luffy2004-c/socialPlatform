from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+)ie=3%#!v%h&oyut9c10a^l(s6iy!wxp36_t2owjzt$fahf=0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "channels",
    "myapp.apps.MyappConfig",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "myapp.middleware.auth.AuthMiddleware",
]

ROOT_URLCONF = "socialPlatform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "socialPlatform.wsgi.application"


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "course_design",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# 添加存放图片类路径
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "myapp.User"


WHITE_REGEX_URL_LIST = [
    "/register/",
    "/login/",
    "/img/code/",
    "/index/",
    "/admin/",
]
# 添加用于处理实时功能的CHANNEL_LAYERS设置
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
ASGI_APPLICATION = "socialPlatform.asgi.application"
LOGIN_REDIRECT_URL = "chat-page"
LOGOUT_REDIRECT_URL = "login-user"


ADDFRIEND_MESSAGE = {
    "added": {
        "message": {
            "content": "你已经与对方是好友了，快去和他聊天吧！",
            "type": "success",
        },
        "button": "聊天",
    },
    "notAdded": {
        "message": {"content": "你和他还不和好友关系，快添加他吧！", "type": "info"},
        "button": "添加",
    },
    "notself": {
        "message": {"content": "不能添加自己为好友！", "type": "warning"},
        "button": "添加",
    },
    "havefor": {
        "message": {
            "content": "你已经向ta发过申请了，请不要重复操作！",
            "type": "warning",
        },
        "button": "添加",
    },
}
