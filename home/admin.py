# register domain
from django.contrib import admin

from home.models import SubDomain, Domain


@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'proxy_pass']
    search_fields = ['domain', 'proxy_pass']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
