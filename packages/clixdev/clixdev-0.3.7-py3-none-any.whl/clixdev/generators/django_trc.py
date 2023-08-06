def MANAGE(proj_name):
    return f"""import os
import sys


def main():
\tos.environ.setdefault('DJANGO_SETTINGS_MODULE', '{proj_name}.settings')
\ttry:
\t\tfrom django.core.management import execute_from_command_line
\texcept ImportError as exc:
\t\traise ImportError(
\t\t\t"Couldn't import Django. Are you sure it's installed and "
\t\t\t"available on your PYTHONPATH environment variable? Did you "
\t\t\t"forget to activate a virtual environment?"
\t\t) from exc
\texecute_from_command_line(sys.argv)


if __name__ == '__main__':
\tmain()
"""


def URLS(apps):
    routes = [f"from {app['name']} import urls as {app['name']}_urls\n" for app in apps]

    includes = []
    for app in apps:
        includes.append(f"\tpath('{app['base_url']}', include({app['name']}_urls)),\n")

    
    return f"""from django.contrib import admin
from django.urls import path, include

{''.join(routes)}

urlpatterns = [
\tpath('admin/', admin.site.urls),
{''.join(includes)}]


admin.site.site_header = "Clix"
admin.site.site_title = "Clix.dev"
"""


def SETTINGS(proj_name, apps, settings, secret_key):
    settings = [setting[0]+ ' = ' + setting[1] + '\n' for setting in settings.values()]
    return f"""from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{secret_key}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#### SETTINGS ####
{''.join([setting for setting in settings])}


# Application definition

INSTALLED_APPS = [
\t'django.contrib.admin',
\t'django.contrib.auth',
\t'django.contrib.contenttypes',
\t'django.contrib.sessions',
\t'django.contrib.messages',
\t'django.contrib.staticfiles',

\t{','.join("'" + app['name'] + "'" for app in apps)},
]

MIDDLEWARE = [
\t'django.middleware.security.SecurityMiddleware',
\t'django.contrib.sessions.middleware.SessionMiddleware',
\t'django.middleware.common.CommonMiddleware',
\t'django.middleware.csrf.CsrfViewMiddleware',
\t'django.contrib.auth.middleware.AuthenticationMiddleware',
\t'django.contrib.messages.middleware.MessageMiddleware',
\t'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{proj_name}.urls'

TEMPLATES = [
\t{{
\t\t'BACKEND': 'django.template.backends.django.DjangoTemplates',
\t\t'DIRS': [BASE_DIR / 'templates'],
\t\t'APP_DIRS': True,
\t\t'OPTIONS': {{
\t\t\t'context_processors': [
\t\t\t\t'django.template.context_processors.debug',
\t\t\t\t'django.template.context_processors.request',
\t\t\t\t'django.contrib.auth.context_processors.auth',
\t\t\t\t'django.contrib.messages.context_processors.messages',
\t\t\t],
\t\t}},
\t}},
]

WSGI_APPLICATION = '{proj_name}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {{
\t'default': {{
\t\t'ENGINE': 'django.db.backends.sqlite3',
\t\t'NAME': BASE_DIR / 'db.sqlite3',
\t}}
}}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
\t{{
\t\t'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
\t}},
\t{{
\t\t'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
\t}},
\t{{
\t\t'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
\t}},
\t{{
\t\t'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
\t}},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

    """


def WSGI(proj_name):
    return f"""import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{proj_name}.settings')

application = get_wsgi_application()
"""


def VIEWS(app):
    endpoints = app['endpoints']
    defs = ["import json\nfrom django.http import JsonResponse\nfrom django.views.decorators.csrf import csrf_exempt\n\nfrom .models import *"]

    for endpoint in endpoints:
        misc = endpoint['misc']
        req = endpoint['request']
        response = endpoint.get('response')
        responses = ''.join([f'"{k}": "{v}",' for k, v in response.items()])
        csrf = '@csrf_exempt\n' if req.get('host') == 'localhost' else ''
        header_code = '\n\t\t\theaders = request.headers' if len(endpoint.get('headers').get('body').items()) > 0 else ''
        param_code = '\n\t\t\tparams = kwargs.items()' if len(endpoint.get('params').items()) > 0 else ''
        body_code = '\n\t\t\tbody = json.loads(request.body)\n\n' if len(endpoint.get('body').get('payload')) > 0 else '\n' if header_code != '' else ''

        defs.append(f"""
# Name: {endpoint.get('misc').get('name')}
# Headers: {', '.join([header[0]+'('+header[1]+')' for header in endpoint.get('headers').get('body').values() if header[0] and header[1]])}
# Params: {', '.join([param[0]+'('+param[1]+')' for param in endpoint.get('params').values() if param[0] and param[1]])}
# Body: {', '.join([payload[0]+'('+payload[1]+')' for payload in endpoint.get('body').get('payload').values() if payload[0] and payload[1]])}
{csrf}def {misc.get('token')}(request, *args, **kwargs):
\tif request.method == '{req.get('method')}':
\t\ttry:{header_code}{param_code}{body_code}
\t\t\t#### Add Your Logic Here ####


\t\t\treturn JsonResponse({{
\t\t\t\t{responses}
\t\t\t}}, safe=False)
\t\texcept Exception as e:
\t\t\treturn JsonResponse(False, safe=False)
\treturn JsonResponse(False, safe=False)
""")
    return '\n\n'.join(defs)


def MODELS(app):
    _class = ""
    for model in app.get('models'):
        _class += f'class {model.get("table_name")}(models.Model):\n'
        fields = model.get('fields')
        for field in fields.values():
            type = field[2]
            if type == 'UUIDField':
                _class += f"\t{field[1]} = models.UUIDField(primary_key=True, unique=True, editable=False, max_length=21, default=uuid.uuid4, auto_created=True"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif type == 'JSONField':
                _class += f"\t{field[1]} = models.JSONField(default=dict, null={field[5]}, blank={field[6]}, unique={field[8]}"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif type == 'DateTimeField':
                _class += f"\t{field[1]} = models.DateTimeField(default=timezone.now, null={field[5]}, blank={field[6]}, unique={field[8]}"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif type == 'CharField':
                _class += f"\t{field[1]} = models.CharField(max_length=255, null={field[5]}, blank={field[6]}, unique={field[8]}"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif type == 'EmailField':
                _class += f"\t{field[1]} = models.EmailField(max_length=255, null={field[5]}, blank={field[6]}, unique={field[8]}"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif type == 'ImageField':
                _class += f'\t{field[1]} = models.ImageField(upload_to="{field[3]}", null={field[5]}, blank={field[6]}, unique={field[8]}'
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            elif len(type.split('.')) > 1 and type.split('.')[1] == 'id':
                _class += f"\t{field[1]} = models.ForeignKey(to={field[2].split('.')[0]}, on_delete=models.SET_NULL, null={field[5]}, blank={field[6]}, unique={field[8]}"
                _class += f', default="{field[3]}"' if field[3] else ''
                _class += f', verbose="{field[4]}"' if field[4] else ''
                _class += ')\n'
            else:
                _class += f"\t{field[1]} = models.{type}(null={field[5]}, blank={field[6]}, unique={field[8]})\n"

        _class += '\n'
    
    return f"""import uuid
from django.db import models
from django.utils import timezone


{_class}
"""


def APP_URLS(app):
    endpoints = app['endpoints']
    urls = [f"from django.urls import path\n\nfrom {app['name']}.views import *\n\nurlpatterns = ["]

    for endpoint in endpoints:
        urls.append(
            f"""\tpath('{endpoint.get('request').get('uri')}{'/' if len(endpoint['params']) > 0 else ''}{'/'.join(['<'+param[0]+'>' for param in endpoint['params'].values() if param[0]])}', {endpoint.get('misc').get('token')}),""")
    return '\n'.join(urls) + "\n]"


def ADMIN(app):
    models = app.get('models')

    registers = '\n'.join(['admin.site.register(' + model.get('table_name') + ')' for model in models])
    return f"""from django.contrib import admin

from .models import *

{registers}
"""


def REQUIREMENTS():
    return """"""


def README():
    return """"""
