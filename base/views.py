from django.shortcuts import redirect, render
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

# Create your views here.
def home(request):
    q = request.GET.get('q','')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q) 
    ) 
    topics = Topic.objects.all()
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count': rooms.count()
    }
    return render(request,'home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)  # type: ignore
        if form.is_valid():
            form.save()
        return redirect(home)
    
    context ={
        'form':form
    }
    return render(request,'room_form.html', context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)  # type: ignore
        if form.is_valid():
            form.save()
        return redirect(home)
    
    context ={
        'form':form
    }
    return render(request,'room_form.html', context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    context = {'obj':room}
    if request.method=="POST":
        room.delete()
        return redirect(home)
    return render(request,'delete.html',context)
