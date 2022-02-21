from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('room.urls', namespace='room')),
    path('account/', include('account.urls', namespace='account'))
    
]
