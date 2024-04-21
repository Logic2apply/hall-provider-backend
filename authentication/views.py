from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Please check your username or password.')
        return render(request, 'authentication/login.html')
    return redirect("index")

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('signin')
        return render(request, 'authentication/register.html')
    return redirect("index")

@login_required(redirect_field_name="signin")
def addStaff(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_staff=True)
            user.save()
            messages.success(request, 'Staff Account created successfully!')
            return redirect('signin')
        return render(request, 'authentication/addStaff.html')


@login_required(redirect_field_name="signin")
def signout(request):
    logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect("signin")