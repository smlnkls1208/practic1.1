from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegisterForm

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            from .models import UserProfile
            UserProfile.objects.create(user=user, full_name=form.cleaned_data['full_name'])
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})