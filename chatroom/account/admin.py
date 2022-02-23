from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    search_fields = ('email', 'username',)
    list_display = ('email', 'username', 'role', 'is_superuser', 'is_staff',)
    readonly_fields = ('signup_date',)

    list_filter = ()  # I don't know what this does but I faced to an Error when deleting it


admin.site.register(MyUser, MyUserAdmin)
