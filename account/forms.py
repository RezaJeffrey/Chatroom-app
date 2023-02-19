from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'bio')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'first_name(Not Required)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'last_name(Not Required)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': 'password'}),
            'bio': forms.Textarea(attrs={'class': 'form-control',
                                         'placeholder': 'Bio(Not Required)'}),
        }


class SignInForm(forms.Form):
    username = forms.CharField(
                               max_length=85,
                               min_length=3,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Username'})
                               )
    password = forms.CharField(
                               max_length=85,
                               min_length=3,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Username'})
                               )










