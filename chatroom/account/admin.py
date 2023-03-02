from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    search_fields = ('email', 'username',)
    list_display = ('email', 'username', 'role', 'is_superuser', 'is_staff',)
    readonly_fields = ('date_joined',)

    list_filter = ()  # I don't know what this does but I faced to an Error when deleting it


admin.site.register(User, MyUserAdmin)
