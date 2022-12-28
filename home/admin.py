# register domain
from django.contrib import admin
from django.utils.safestring import mark_safe

from home.models import SubDomain, Domain


@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'proxy_pass', 'link']
    search_fields = ['domain', 'proxy_pass']

    def link(self, obj):
        """ return domain name  as a link to the domain """
        return mark_safe('<a href="http://{}" target="_blank">{}</a>'.format(obj.domain_name, obj.domain_name))


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
