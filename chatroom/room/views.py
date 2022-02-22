from django.shortcuts import render, redirect, HttpResponse
from .models import Room, Message
from django.views import View
from .forms import CreateRoomForm
from django.contrib import messages
from django.utils.text import slugify


class HomeView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'room/home.html', {'rooms': rooms})


class CreateRoomView(View):
    form_class = CreateRoomForm
    template_name = 'room/create_room.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'warning')
            # TODO redirect to login page after adding the feature
            return redirect('room:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            room = Room.objects.filter(room_name=cd['room_name'])
            if not room.exists():
                new_room_slug = slugify(cd['room_name'][:25], allow_unicode=True)
                Room.objects.create(room_name=cd['room_name'], slug=new_room_slug)
                messages.success(request, 'room created', 'success')
                return redirect('room:home')
            messages.error(request, 'This room is already exists', 'warning')
        return render(request, self.template_name, {'form': form})


class RoomInsideView(View):
    def get(self, request, room_id, room_slug):
        return HttpResponse(f"<h1>its room {room_slug} </h1>")






