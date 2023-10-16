from django.contrib import admin

from .models import Follow, CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username',)
    list_filter = ('username', 'email')
    ordering = ('username',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'author'
    )
    search_fields = ('username',)
    list_filter = ('username', 'author')
    ordering = ('username',)
