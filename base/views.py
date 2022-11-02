from django.shortcuts import redirect, render, HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# login-register
def laginPage(request):

    if request.user.is_authenticated:
        return redirect(home)
     
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist.')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            messages.error(request,'Username or Password not matched.')


    context ={}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect(home)


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

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)  # type: ignore
        if form.is_valid():
            form.save()
        return redirect(home)
    
    context ={
        'form':form
    }
    return render(request,'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    context = {'obj':room}

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method=="POST":
        room.delete()
        return redirect(home)
    return render(request,'delete.html',context)
