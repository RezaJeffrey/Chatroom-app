from django.shortcuts import render, redirect, HttpResponse
from .models import Room, Message
from django.views import View
from .forms import CreateRoomForm, CreatePrivateRoomForm, RoomAuthForm, SendMessageForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'room/home.html', {'rooms': rooms})


class RoomTypeView(View):
    def get(self, request):
        return render(request, 'room/room_choose.html')


class CreateRoomView(View):
    form_class = CreateRoomForm
    template_name = 'room/create_room.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'warning')
            return redirect('account:signin')
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
                room = Room(room_name=cd['room_name'], slug=new_room_slug)
                room.save()
                messages.success(request, 'room created', 'success')
                return redirect('room:home')
            messages.error(request, 'This room is already exists', 'warning')
        return render(request, self.template_name, {'form': form})


class CreatePrivateRoomView(View):
    form_class = CreatePrivateRoomForm
    template_name = 'room/create_room.html'


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            room = Room.objects.filter(room_name=cd['room_name'])
            if room:
                messages.error(request, 'a room with this name is already exists', 'danger')
                return render(request, self.template_name, {'form': form})
            privateroom_slug = slugify(cd['room_name'][:25], allow_unicode=True)
            privateroom = Room(room_name=cd['room_name'], slug=privateroom_slug)
            privateroom.set_is_private(True)
            privateroom.set_password(cd['password'])
            privateroom.save()
            messages.success(request, f"Room {cd['room_name']} created", 'success')
            return redirect('room:room_inside', privateroom.id, privateroom.slug)
        messages.error(request, 'not valid', 'danger')
        return render(request, self.template_name, {'form': form})


class RoomInsideView(View):
    template_name = 'room/room_inside.html'
    form_class = SendMessageForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'danger')
            return redirect('account:signin')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.room = Room.objects.get(id=kwargs['room_id'])
        self.all_messages = Message.objects.filter(room=self.room)
        return super().setup(request, *args, **kwargs)

    def get(self, request, room_id, room_slug):
        if request.user.room_set.filter(id=room_id).exists():
            self.room = Room.objects.get(id=room_id)
            # if self.room.is_private:
            #     return redirect('room:private_room_auth', self.room.id)
            form = self.form_class()
            context =  {
                        'room': self.room,
                        'form': form,
                        'message': self.all_messages,
            }

            return render(request, self.template_name, context)
        messages.error(request, 'Join the room first', 'warning')
        return redirect('room:join_room', room_id)

    def post(self, request, room_id, room_slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(self.room)
            new_msg = Message(body=form.cleaned_data['body'])
            new_msg.user = request.user
            new_msg.room = self.room
            new_msg.save()
            return redirect('room:room_inside', room_id, room_slug)
        else:
            messages.error(request, 'form not valid', 'warning')
        return render(request, self.template_name, {'form': form, 'message': self.all_messages})


class JoinRoomView(LoginRequiredMixin, View):
    template_name = 'room/join_room.html'
    form_class = RoomAuthForm
    def setup(self, request, *args, **kwargs):
        self.new_room = Room.objects.get(id=kwargs['room_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, room_id):
        if self.new_room.is_private:
            form = self.form_class()
            return render(request, self.template_name, {'room': self.new_room, 'form': form})
        return render(request, self.template_name, {'room': self.new_room})

    def post(self, request, room_id):
        if self.new_room.is_private:
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if check_password(cd['password'], self.new_room.password):
                    request.user.room_set.add(self.new_room)
                    messages.success(request, 'joined room', 'success')
                    return redirect('room:room_inside', room_id, self.new_room.slug)
                messages.error(request, 'wrong password', 'danger')
                return redirect('room:join_room', room_id)
            messages.warning(request, 'form not valid', 'warning')
            return redirect('room:join_room', room_id)
        request.user.room_set.add(self.new_room)
        messages.success(request, "Joined ...", 'success')
        return redirect('room:room_inside', room_id, self.new_room.slug)


class PrivateRoomInsideView(View):
    template_name = 'room/room_inside.html'
    form_class = SendMessageForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'danger')
            return redirect('account:signin')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.room = Room.objects.get(id=kwargs['room_id'])
        self.all_messages = Message.objects.filter(room=self.room)
        return super().setup(request, *args, **kwargs)

    def get(self, request, room_id, room_slug):
        if request.user.room_set.filter(id=room_id).exists():
            self.room = Room.objects.get(id=room_id)
            form = self.form_class()
            context =  {
                        'room': self.room,
                        'form': form,
                        'message': self.all_messages,
            }

            return render(request, self.template_name, context)
        messages.error(request, 'Join the room first', 'warning')
        return redirect('room:join_room', room_id)

    def post(self, request, room_id, room_slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(self.room)
            new_msg = Message(body=form.cleaned_data['body'])
            new_msg.user = request.user
            new_msg.room = self.room
            new_msg.save()
            return redirect('room:room_inside', room_id, room_slug)
        else:
            messages.error(request, 'form not valid', 'warning')
        return render(request, self.template_name, {'form': form, 'message': self.all_messages})


