from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('roomtype/', views.RoomTypeView.as_view(), name='room_type'),
    path('create-room/', views.CreateRoomView.as_view(), name='create_room'),
    path('create-private-room/', views.CreatePrivateRoomView.as_view(), name='create_private_room'),
    path('<int:room_id>/<slug:room_slug>/', views.RoomInsideView.as_view(), name='room_inside'),
    path('<int:room_id>/', views.JoinRoomView.as_view(), name='join_room'),
    path('private/<int:room_id>/<slug:room_slug>/', views.PrivateRoomInsideView.as_view(), name='private_room_inside'),

]















