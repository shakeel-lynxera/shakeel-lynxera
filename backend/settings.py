import json, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = '*risgat(t_tb@b0ird(+0m-kqw%pl#x6)p2#+w*n&f1f92@=89'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'utilities'
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

ConfigFile = os.path.join(BASE_DIR, 'backend', 'project_settings.json')
SettingInfo = ConfigFile
SettingInfo = open(SettingInfo, 'r')
SettingInfo = json.loads(SettingInfo.read())
Data = SettingInfo['data']
SettingInfo = Data['connectionString']
SettingInfo = SettingInfo.split(';')
SettingInfoDic = {}

for x in SettingInfo:
    if x != '':
        x = x.split('=')
        SettingInfoDic[x[0]] = x[1]

HostName = SettingInfoDic['Server']
UserId = SettingInfoDic['UserId']
Password = SettingInfoDic['Password']
Database = SettingInfoDic['Database']
Port = SettingInfoDic['Port']

MAX_UPLOAD_SIZE = Data['MAX_UPLOAD_SIZE']
IS_PRODUCTION = Data['IsProduction']
DEBUG = Data['Debug']

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
