from django.shortcuts import redirect, render
from .models import Room
from .forms import RoomForm

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
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
    return render(request,'delete.html',context)
