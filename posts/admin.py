from django.contrib import admin
from .models import Post, Reaction


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'datetime'
    )
    search_fields = (
        'user',
    )


admin.site.register(Post, PostAdmin)


class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(Reaction, ReactionAdmin)
