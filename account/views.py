from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .forms import SignUpForm, SignInForm
from .models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout


class SignUpView(View):
    template_name = 'account/signup.html'
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are currently logged in', 'danger')
            return redirect('room:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(username=cd['username'], email=cd['email'])
            user.set_password(cd['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Signed Up and login successfully', 'success')
            return redirect('room:home')
        messages.error(request, 'not valid', 'danger')
        return render(request, self.template_name, {'form': form})


class SignInView(View):
    form_class = SignInForm
    template_name = 'account/signin.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are currently logged in', 'danger')
            return redirect('room:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                return redirect('room:home')
            messages.error(request, 'wrong password or username', 'danger')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class SignOutView(LoginRequiredMixin, View):  # if not using loginrequiredmixin then should do by it your own(is_authed)
    def get(self, request):
        logout(request)
        messages.success(request, 'successfully loged out', 'success')
        return redirect('room:home')



















