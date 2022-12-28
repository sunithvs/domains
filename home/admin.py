# register domain
from django.contrib import admin

from home.models import SubDomain, Domain


@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'proxy_pass', 'domain_name']
    search_fields = ['domain', 'proxy_pass']

    def domain_name(self, obj):
        return obj.domain_name


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
