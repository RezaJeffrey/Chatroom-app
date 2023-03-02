from django import forms
from .models import Room, Message


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name',)


class CreatePrivateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': 'password'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Name'}),
        }


class RoomAuthForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': 'password'}),
        }


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Send'}),
        }
