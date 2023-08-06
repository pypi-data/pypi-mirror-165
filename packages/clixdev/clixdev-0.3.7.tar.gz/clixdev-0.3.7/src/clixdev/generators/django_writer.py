import os
import json
import shutil
import requests
import psutil
import platform
from datetime import datetime

from .django_trc import MANAGE, REQUIREMENTS, WSGI, URLS, SETTINGS, VIEWS, MODELS, APP_URLS, ADMIN, README


def generate(terminal_token, project_token, *args):
    try:
        if True or requests.post('https://api.clix.dev/api/package/verify-user', data=json.dumps({'username': username, 'password': password, 'terminal_token': token})).json():
            res = requests.post('https://api.clix.dev/api/package/sync',
            data=json.dumps({
                'terminal_token': terminal_token,
                'project_token': project_token,
                'data': [None, None, None, None]
            })).json()

            secret_key = res.get('misc').get('secret_key')
            project_name = res.get('misc').get('project_name')
            working_dir = os.getcwd() + '/' + args[0] + '/' + project_name + '/' if args[0] else os.getcwd() + '/' + project_name + '/'
            
            if os.path.exists(working_dir):
                shutil.rmtree(working_dir)
            os.makedirs(working_dir)
            
            base_file_tree = {
                'README.md': README(),
                'manage.py': MANAGE(project_name),
                'requirements.txt': REQUIREMENTS(),
                'db.sqlite3': '',
                'static/': [],
                'templates/': [],
                'templates/admin/': [('base_site.html', """{% extends "admin/base_site.html" %}{% load static %}{% block extrahead %}<link rel="stylesheet" href="https://api.clix.dev/static/admin.css" type="text/css" />{% endblock %}""")],
                project_name + '/': [('__init__.py', ''), ('wsgi.py', WSGI(project_name)), ('settings.py', SETTINGS(project_name, res.get('apps'), res.get('settings'), secret_key)), ('urls.py', URLS(res.get('apps')))],
            }

            # generating base file tree
            for k, v in base_file_tree.items():
                if type(v) is str:
                    with open(working_dir + k, 'w') as ff:
                        ff.write(base_file_tree.get(k))
                else:
                    os.mkdir(working_dir + k)
                    for f in v:
                        with open(working_dir + k + f[0], 'w') as ff:
                            ff.write(f[1])
            
            # generate apps
            for app in res.get('apps'):
                file_extensions = {
                    '': [('__init__.py', ''), ('models.py', MODELS(app)), ('admin.py', ADMIN(app)), ('apps.py', f"from django.apps import AppConfig\n\n\nclass AppConfig(AppConfig):\n\tname = '{app.get('name')}'"), ('tests.py', 'from django.test import TestCase'), ('urls.py', APP_URLS(app)), ('views.py', VIEWS(app))],
                    # 'views/': [('__init__.py', 'from .views import *\nfrom ._views import *'), ('views.py', VIEWS(app)), ('_views.py', '#nothing yet')],
                    'migrations/': [('__init__.py', '')],
                }
                for k, v in file_extensions.items():
                    working_d = working_dir + app.get('name') + '/' + k
                    os.mkdir(working_d)
                    for file_name, file_content in v:
                        with open(working_d + file_name, 'w') as ff:
                            ff.write(file_content)

                return True
    
    except Exception as e:
        print(e)
        raise Exception('base template error')
