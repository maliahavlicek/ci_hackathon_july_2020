from django.contrib import admin
from .models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'mood',
        'plans',
        'help'
    )


admin.site.register(Status, StatusAdmin)
