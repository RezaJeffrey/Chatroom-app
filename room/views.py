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
                request.user.room_set.add(room)
                new = request.user.membership_set.get(room=room)
                new.set_is_admin(True)
                new.save()
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
            request.user.room_set.add(privateroom)
            new = request.user.membership_set.get(room=privateroom)
            new.set_is_admin(True)
            new.save()
            messages.success(request, f"Room {cd['room_name']} created", 'success')
            return redirect('room:room_inside', privateroom.room_name)
        messages.error(request, 'not valid', 'danger')
        return render(request, self.template_name, {'form': form})


class RoomInsideView(View):
    template_name = 'room/ws-room.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'danger')
            return redirect('account:signin')
        return super().dispatch(request, *args, **kwargs)

    # def setup(self, request, *args, **kwargs):
    #     self.room = Room.objects.get(room_name=kwargs['room_name'])
    #     self.all_messages = Message.objects.filter(room=self.room)
    #     return super().setup(request, *args, **kwargs)

    def get(self, request, room_name):
        room = Room.objects.get(room_name=room_name)
        if request.user.room_set.filter(room_name=room_name).exists():
            all_messages = Message.objects.filter(room=room)
            req_is_admin = request.user.membership_set.get(room=room).is_admin
            context = {
                'username': request.user.username,
                'room': room,
                'message': all_messages,
                'room_name': room_name,
                'req_is_admin': req_is_admin,
            }

            return render(request, self.template_name, context)
        messages.error(request, 'Join the room first', 'warning')
        return redirect('room:join_room', room.id)


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
                    return redirect('room:room_inside', self.new_room.room_name)
                messages.error(request, 'wrong password', 'danger')
                return redirect('room:join_room', room_id)
            messages.warning(request, 'form not valid', 'warning')
            return redirect('room:join_room', room_id)
        request.user.room_set.add(self.new_room)
        messages.success(request, "Joined ...", 'success')
        return redirect('room:room_inside', self.new_room.room_name)


class PrivateRoomInsideView(View):
    template_name = 'room/ws-room.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'login first', 'danger')
            return redirect('account:signin')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.room = Room.objects.get(room_name=kwargs['room_name'])
        self.all_messages = Message.objects.filter(room=self.room)
        return super().setup(request, *args, **kwargs)

    def get(self, request, room_name):
        if request.user.room_set.filter(room_name=room_name).exists():
            self.room = Room.objects.get(room_name=room_name)
            req_is_admin = request.user.membership_set.get(room=self.room).is_admin
            context = {
                'username': request.user.username,
                'room': self.room,
                'message': self.all_messages,
                'room_name': room_name,
                'req_is_admin': req_is_admin,
            }

            return render(request, self.template_name, context)
        messages.error(request, 'Join the room first', 'warning')
        return redirect('room:join_room', self.room.id)


class DeleteMessageView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = Message.objects.get(id=message_id)
        message_room = message.room
        room_slug = message_room.slug
        if message.user.id == request.user.id or request.user.membership_set.get(room=message_room).is_admin:
            message.delete()
            messages.success(request, 'deleted successfully', 'success')
            if message_room.is_private:
                return redirect('room:private_room_inside', message_room.id, room_slug)
            return redirect('room:room_inside', message_room.id, room_slug)
        messages.error(request, 'this is not your message or your not admin', 'danger')
        if message_room.is_private:
            return redirect('room:private_room_inside', message_room.id, room_slug)
        return redirect('room:room_inside', message_room.id, room_slug)


class EditMessageView(LoginRequiredMixin, View):
    form_class = SendMessageForm

    def setup(self, request, *args, **kwargs):
        self.message_instance = Message.objects.get(id=kwargs['message_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        message = self.message_instance
        if request.user.id != message.user.id:
            messages.error(request, 'you cant edit others posts', 'danger')
            return redirect('room:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, message_id):
        message = self.message_instance
        all_messages = Message.objects.filter(room=message.room)
        form = self.form_class(instance=message)
        return render(request, 'room/room_inside.html', {'form': form, 'room': message.room, 'message': all_messages})

    def post(self, request, message_id):
        message = self.message_instance
        form = self.form_class(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'edited', 'success')
            if message.room.is_private:
                return redirect('room:private_room_inside', message.room.id, message.room.slug)
            return redirect('room:room_inside', message.room.id, message.room.slug)


"""   ws   """


def ws_index(request):
    return render(request, "room/ws-index.html")


def ws_room(request, room_name):
    room = Room.objects.filter(room_name=room_name)
    user = request.user.username
    context = {
        "room_name": room_name,
        "room": room,
        "username": user
    }
    return render(request, "room/ws-room.html", context=context)
