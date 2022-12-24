# register domain
from django.contrib import admin

from home.models import Domain


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'proxy_pass']
