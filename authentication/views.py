from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.forms import LoginForm, SignUpForm


# Create your views here.
def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                user = authenticate(
                    username = request.POST["username"],
                    password = request.POST["password"],
                )
                print(user)
                if user is not None:
                    login(request, user)
                    messages.success(request, "You are now logged in!")
                    return redirect("index")
                else:
                    messages.error(request, "Please check your username or password.")
                    return redirect("signin")
            except:
                messages.error(request, "A error occured")
                return redirect("signin")

        loginform = LoginForm()
        return render(request, "authentication/login.html", {"form": loginform})
    return redirect("index")


def register(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            print(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username = form.cleaned_data["username"],
                    password = form.cleaned_data["password"],
                    email = form.cleaned_data["email"],
                    first_name = form.cleaned_data["first_name"],
                    last_name = form.cleaned_data["last_name"],
                )
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect("signin")
            else:
                messages.error(request, "An error occured")
                return redirect("register")

        form = SignUpForm()
        return render(request, "authentication/register.html", {"form":form})
    return redirect("index")


@login_required(login_url="/auth/login/")
def addStaff(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            print(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                    email=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    is_staff=True,
                )
                user.save()
                messages.success(request, "Staff Account created successfully!")
                return redirect("signin")
            else:
                messages.error(request, "An error occured")
                return redirect("register")
        
        form = SignUpForm()
        return render(request, "authentication/addStaff.html", {"form":form})
    else:
        messages.error(request, "Must be superuser")
        redirect("index")

@login_required(login_url="/auth/login/")
def signout(request):
    logout(request)
    messages.success(request, "You are now logged out!")
    return redirect("signin")
