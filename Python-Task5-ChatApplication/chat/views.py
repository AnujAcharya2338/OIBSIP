from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat_home")  # w
    else:
        form = UserCreationForm()
    return render(request, "chat/register.html", {"form": form})

from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def chat_home(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name", "").strip()
        if room_name:
            Room.objects.get_or_create(name=room_name, defaults={"created_by": request.user})
            return redirect("room", room_name=room_name)
    rooms = Room.objects.all()
    return render(request, "chat/home.html", {"rooms": rooms})