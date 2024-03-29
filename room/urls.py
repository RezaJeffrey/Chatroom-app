from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('roomtype/', views.RoomTypeView.as_view(), name='room_type'),
    path('create-room/', views.CreateRoomView.as_view(), name='create_room'),
    path('create-private-room/', views.CreatePrivateRoomView.as_view(), name='create_private_room'),
    path('room/<str:room_name>/', views.RoomInsideView.as_view(), name='room_inside'),
    path('room/private/<str:room_name>/', views.PrivateRoomInsideView.as_view(), name='private_room_inside'),
    path('join-room/<int:room_id>/', views.JoinRoomView.as_view(), name='join_room'),
    # path('delete_message/<int:message_id>/', views.DeleteMessageView.as_view(), name='delete_message'),
    # path('edit_message/<int:message_id>/', views.EditMessageView.as_view(), name='edit_message'),
    # ws
    path('ws_chat/', views.ws_index, name='ws-index'),
    path("ws_chat/<str:room_name>/", views.ws_room, name="ws-room"),
]
















