from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-hall/", views.addHall, name="addHall"),
]
