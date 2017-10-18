from django.contrib import admin

from .models import EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']


admin.site.register(EmailTemplate, EmailTemplateAdmin)
