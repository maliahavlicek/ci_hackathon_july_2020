from django.contrib import admin
from .models import UserExtended, Family


class UserExtendedAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'profile_picture'
    )
    search_fields = (
        'user',
    )


admin.site.register(UserExtended, UserExtendedAdmin)


class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'family_name',
        'hero_image'
    )
    search_fields = (
        'family_name',
    )


admin.site.register(Family, FamilyAdmin)
