from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from home.models import Hall, Booking

from django.contrib import messages


# Create your views here.
def index(request):
    return HttpResponse("Welcome")


# Hall model
#     id = models.AutoField(primary_key=True)
#     name = models.TextField(null=False, max_length=500, default="")
#     description = models.CharField(null=False, max_length=1500, default="")
#     location = models.TextField(null=False, max_length=500, default="")
#     capacity = models.IntegerField(null=False, default=0)
#     images = models.ImageField(upload_to="HallImages", default="HallImages/default.jpg")
#     created_at = models.DateField(auto_now_add=True)

@login_required(redirect_field_name="login")
def addHall(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        if request.method == "POST":
            try:
                name = request.POST['name']
                description = request.POST['description']
                location = request.POST['location']
                capacity = request.POST['capacity']
                images = request.FILES['images']
                newHall = Hall(name=name, description=description, location=location, capacity=capacity, images=images)
                newHall.save()
                messages.success(request, "Hall added successfully")
                return redirect("addHall")
            except:
                messages.error(request, "Something went wrong")
                return redirect("addHall")

        return render(request, 'home/addHall.html')
