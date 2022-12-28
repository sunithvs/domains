from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.response import Response
# program to read nginx config and save it in database

import os
import re
from .models import SubDomain


def collect_domains():
    for file in os.listdir('/etc/nginx/sites-enabled'):

        # open each file
        with open('/etc/nginx/sites-enabled/' + file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'server_name' in line:
                    domain = re.findall(r'server_name (.*)', line)[0]
                    domain = domain.replace(';', '')

                if 'proxy_pass' in line:
                    proxy_pass = re.findall(r'proxy_pass (.*)', line)[0]
                    proxy_pass = proxy_pass.replace('https://', '')
                    proxy_pass = proxy_pass.replace('http://', '')
                    proxy_pass = proxy_pass.replace(';', '')
                # save the domain and proxy_pass in database

            if domain and proxy_pass and domain != "example.com":
                if not SubDomain.objects.filter(domain=domain).exists():
                    try:
                        SubDomain.objects.create(domain=domain, proxy_pass=proxy_pass)
                    except Exception as e:
                        print(e)
            # Domain.objects.create(domain=domain, proxy_pass=proxy_pass)
        f.close()

# read all the files in sites-enabled
