from django.contrib import admin
from .models import Room, Message, Membership
from django.contrib.admin import ModelAdmin


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('room_name', 'is_private',)
    search_fields = ('members', 'room_name')
    list_filter = ()
    filter_horizontal = ()


@admin.register(Membership)
class MembershipAdmin(ModelAdmin):
    list_display = ('__str__', 'is_admin')
    search_fields = ('members', 'room_name')
    list_filter = ()
    filter_horizontal = ()


@admin.register(Message)
class MessagesAdmin(ModelAdmin):
    list_display = ('user', 'room', 'short_body', )
    search_fields = ('user', 'room', 'body',)
    list_filter = ()
    filter_horizontal = ()





