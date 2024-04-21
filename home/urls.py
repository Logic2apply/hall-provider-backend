from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-hall/", views.addHall, name="addHall"),
    path("view-halls/", views.viewHalls, name="viewHalls"),
    path("remove-hall/<int:hallid>", views.removeHall, name="removeHall"),
]
