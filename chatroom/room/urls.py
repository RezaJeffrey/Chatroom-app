from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create-room/', views.CreateRoomView.as_view(), name='create_room'),
    path('<int:room_id>/<slug:room_slug>/', views.RoomInsideView.as_view(), name='room_inside'),

]















