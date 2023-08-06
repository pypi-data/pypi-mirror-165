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
                'data': sys_info()
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


def sys_info():
    try:
        uname = platform.uname()
        bt = datetime.fromtimestamp(psutil.boot_time())
        system = {
            "System": uname.system,
            "Node Name": uname.node,
            "Release": uname.release,
            "Version": uname.version,
            "Machine": uname.machine,
            "Processor": uname.processor,
            "Boot Time": f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        }

        cpu_freq = psutil.cpu_freq()
        cpu = {
            "Physical cores": psutil.cpu_count(logical=False),
            "Total cores": psutil.cpu_count(logical=True),
            "Max Frequency": f"{cpu_freq.max:.2f}Mhz",
            "Min Frequency": f"{cpu_freq.min:.2f}Mhz",
            "Current Frequency": f"{cpu_freq.current:.2f}Mhz",
            "CPU Usage Per Core": [f"Core {i}: {percentage}%" for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1))],
            "Total CPU Usage": psutil.cpu_percent(),
        }

        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory = {
            "Total": get_size(svmem.total),
            "Available": get_size(svmem.available),
            "Used": get_size(svmem.used),
            "Percentage": svmem.percent,
            "Total": get_size(swap.total),
            "Free": get_size(swap.free),
            "Used": get_size(swap.used),
            "Percentage": f"{swap.percent}%",
        }

        partitions = psutil.disk_partitions()
        disk_io = psutil.disk_io_counters()
        disk = {
            "Partitions": [{
                "Device": partition.device,
                "Mount point": partition.mountpoint,
                "File system": f"type: {partition.fstype}",
                "Total Size": get_size(psutil.disk_usage(partition.mountpoint).total),
                "Used": get_size(psutil.disk_usage(partition.mountpoint).used),
                "Free": get_size(psutil.disk_usage(partition.mountpoint).free),
                "Percentage": psutil.disk_usage(partition.mountpoint).percent,
            } for partition in partitions],
            "Total read": get_size(disk_io.read_bytes),
            "Total write": get_size(disk_io.write_bytes),
        }

        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        network = {}
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    network[f"Interface: {interface_name}"] = {
                        "IP Address": address.address,
                        "Netmask": address.netmask,
                        "Broadcast IP": address.broadcast,
                    }
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    network[f"Interface: {interface_name}"] = {
                        "MAC Address": address.address,
                        "Netmask": address.netmask,
                        "Broadcast MAC": address.broadcast,
                    }
        network["Total Bytes Sent"] = get_size(net_io.bytes_sent),
        network["Total Bytes Received"] = get_size(net_io.bytes_recv),

        return [system, cpu, memory, disk, network]
    except:
        return [None, None, None, None]


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
