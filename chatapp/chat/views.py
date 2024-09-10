from django.shortcuts import render, redirect
from .models import Room, Message

# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]
        existing_room = Room.objects.filter(room_name__icontains=room).exists()
        if existing_room:
            return redirect("room", roomN_pk=room, userN_pk=username)
        else:
            new_room = Room.objects.create(room_name=room)
            new_room.save()
    return render(request, "home.html")


def room(request, roomN_pk, userN_pk):
    existing_room = Room.objects.get(room_name__icontains=roomN_pk)
    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": userN_pk,
        "room_name": existing_room.room_name,
    }

    return render(request, "room.html", context)
