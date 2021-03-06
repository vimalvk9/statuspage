"""
Django settings for statuspage project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json


data = open('yellowant_app_credentials.json').read()
data_json = json.loads(data)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_name = os.environ.get("HEROKU_APP_NAME")
BASE_URL = "https://{}.herokuapp.com".format(app_name)
SITE_PROTOCOL = "http://"
BASE_HREF = "/"

DEV_ENV = os.environ.get('ENV', 'DEV')
print(DEV_ENV)
if DEV_ENV=="DEV":
    BASE_URL = "http://82c2eb63.ngrok.io"
    SITE_DOMAIN_URL = "ngrok.io"
elif DEV_ENV=="HEROKU":
    BASE_URL = "https://{}.herokuapp.com/".format(app_name)
    app_name = os.environ.get("HEROKU_APP_NAME")
    SITE_DOMAIN_URL = "herokuapp.com"

### Hardcoded Part


## Required parameters for integration with statuspage
# STATUSPAGE_ACCESS_TOKEN = "11649b9b-ea84-47fa-aecb-9faf3ab447bd"
# PAGE_ID = "gvl671ncn9wm"
#
# ## Optional parameter for integration with statuspage
# ORGANIZATION_ID = "zs0dhxtjvt6g"
#
# ### End of Hardcoded Part



# ### Statuspage specific settings ###
#
#
# # Common part for the endpoints
# SP_API_BASE1 = "https://api.statuspage.io/v1/pages/"
# SP_API_BASE2 = "https://api.statuspage.io/v0/organizations/"
# END = ".json"
#
#
# # URL for getting page profile details
# USER_PROFILE_ENDPOINT = PAGE_ID + END
#
# # URL for getting components as well as creating components
# USER_COMPONENTS_ENDPOINT = PAGE_ID + "/components" + END
#
# # URL for getting incidents
# USER_ALL_INCIDENTS_ENDPOINT = PAGE_ID + "/incidents" + END
#
# # URL for getting unresolved incidents
# USER_UNRESOLVED_ENDPOINT = PAGE_ID + "/incidents/unresolved" + END
#
# # URL for creating incidents
# CREATE_INCIDENT = PAGE_ID + "/incidents" + END
#
# ### End of Statuspage specific settings ###

# Statuspage API URLs
SP_API_BASE1 = "https://api.statuspage.io/v1/pages/"
SP_API_BASE2 = "https://api.statuspage.io/v0/organizations/"
END = ".json"
#

YELLOWANT_OAUTH_URL = "https://www.yellowant.com/api/oauth2/authorize/"
YA_APP_ID = str(data_json['application_id'])

YELLOWANT_CLIENT_ID = str(data_json['client_id'])
YELLOWANT_CLIENT_SECRET = str(data_json['client_secret'])
YELLOWANT_VERIFICATION_TOKEN = str(data_json['verification_token'])
YELLOWANT_REDIRECT_URL = BASE_URL + "yellowantredirecturl/"




# ### YellowAnt specific settings ###
#
# # URL to obtain oauth2 access for a YA user
# YELLOWANT_OAUTH_URL = "https://www.yellowant.com/api/oauth2/authorize/"
#
# # URL to receive oauth2 codes from YA for user authentication.
# # As a developer, you need to provide this URL in the YA
# # developer console so that YA knows exactly where to send the oauth2 codes.
# YELLOWANT_REDIRECT_URL = BASE_URL + "/yellowantredirecturl/"
#
# # Numerical ID generated when you register your application through
# #  the YA developer console
# YA_APP_ID = "343"
#
# # Client ID generated from the YA developer console.
# # Required to identify requests from this application to YA
# YELLOWANT_CLIENT_ID = "EyJ51G3GGMroQjd6VtVBmz2cCGVitL9S93wnNHCe"
#
# # Client secret generated from the YA developer console.
# # Required to identify requests from this application to YA
# YELLOWANT_CLIENT_SECRET = "8AsfOHpfs5oIsTYR9Ibbcvb2Zv3z3a1u\
# Rfrg5vaaYFMEcAGD8VbhORy0GdTRTfTW0uDHh0DjvOv3yHWhYKKmQckxGTJ0\
# IOn2XPdmKjyu3Uf400tk7k6VbozmNDig9p3A"
#
# # Verification token generated from the YA developer console.
# # This application can verify requests from YA as they will
# # carry the verification token
# YELLOWANT_VERIFICATION_TOKEN = "7flQD3YMVQoSXBwIfIpaEFRUwY0FBMV\
# v6FJcmTmSWopDBkTc2mhyaKShiTuOKDlGR553Q2GRmbOD98eN82whb0ao8aUtyaC\
# bGrcds5CUSQS0zeyccCPtxrT8i7n2DcAO"
#
# ### END YellowAnt specific settings ###


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x(x(&j#%$a9jmh7bmw*4f59hdmyn7uih)+0zd2rwib7o$0!+7r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','{}.herokuapp.com'.format(app_name)]


# Application definition

INSTALLED_APPS = [
    'lib.web',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lib.records'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'statuspage.urls'

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

WSGI_APPLICATION = 'statuspage.wsgi.application'


# Local database settings
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'statusdb',
        'USER': 'root',
        'PASSWORD': 'vimal_1996',
        'HOST': 'localhost',
        'PORT': '',
    }
}

if DEV_ENV=="HEROKU":
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)
    DATABASES['default']['CONN_MAX_AGE'] = 500

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')