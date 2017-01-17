from django.contrib import admin

from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'extra_data', 'parent_user',
        'get_role_display', 'get_readable_name'
    )
