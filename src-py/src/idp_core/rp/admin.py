from django.contrib import admin

from .models import RpInfo


@admin.register(RpInfo)
class RpInfoAdmin(admin.ModelAdmin):
    list_display = 'client', 'user', 'created'
