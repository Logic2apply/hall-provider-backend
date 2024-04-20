from django.urls import path
from authentication import views

urlpatterns = [
    path("login/", views.signin, name="signin"),
    path("register/", views.register, name="register"),
    path("logout/", views.signout, name="logout"),
    path("add-staff/", views.addStaff, name="addstaff"),

]
