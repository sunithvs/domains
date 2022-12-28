# register domain
from django.contrib import admin

from home.models import SubDomain


@admin.register(SubDomain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'proxy_pass']
    search_fields = ['domain', 'proxy_pass']
