from django.shortcuts import redirect, render, HttpResponse
from .models import Room, Topic,Message, User
from .forms import RoomForm, UserForm
from django.db.models import Q

# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm


# Create your views here.
# login-register
def laginPage(request):

    if request.user.is_authenticated:
        return redirect(home)
     
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User does not exist.')

        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            messages.error(request,'Username or Password not matched.')


    context ={'page':'login'}
    return render(request,'login_register.html',context)

def logoutUser(request): 
    logout(request)
    return redirect(home)

def registerUser(request):
    form = MyUserCreationForm()
    if request.method=='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect(home)   

        else:
            messages.error(request,'Error ocurred during registration')
            
    context={'form':form,}
    return render(request,'login_register.html',context)


def home(request):
    q = request.GET.get('q','')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q) 
    ) 
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count': rooms.count(),
        'room_messages':room_messages
    }
    return render(request,'home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  # type: ignore
    participants = room.participants.all()
    if request.method=="POST":
        body = request.POST['body']
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = body
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)  # type: ignore

    context = {'room':room,'room_messages':room_messages,'participants':participants}

    return render(request,'room.html',context)

def userProfile(request,pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()   # type: ignore
    room_messages = user.message_set.all()  # type: ignore
    topics = Topic.objects.all()
    context ={
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics,
    }
    return render(request,'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()   
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
        # form = RoomForm(request.POST)  # type: ignore
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()


        return redirect(home)
    
    context ={
        'form':form,
        'topics':topics
    }
    return render(request,'room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect(home)
    
    context ={
        'form':form,
        'topics':topics,
        'room':room
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

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    context = {'obj':message}

    if request.user != message.user:
        return HttpResponse("You are not allowed here!")

    if request.method=="POST":
        message.delete()
        return redirect(home)
    return render(request,'delete.html',context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method=="POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {
        'form':form,
    }
    return render(request,'update-user.html',context)
    

def topicsPage(request):
    q = request.GET.get('q','')
    topics = Topic.objects.filter(
        Q(name__icontains=q) 
    )
    return render(request, 'topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()[:4]
    return render(request,'activity.html',{'room_messages':room_messages})