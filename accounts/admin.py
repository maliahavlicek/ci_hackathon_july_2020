from django.contrib import admin
from .models import Family


class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'family_name',
        'hero_image'
    )
    search_fields = (
        'family_name',
    )


admin.site.register(Family, FamilyAdmin)
