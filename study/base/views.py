from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .form import MyUserCreationForm, RoomForm, UserForm
from .models import Message, Room, Topic, User

# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'lets learn java'},
#     {'id':3,'name':'lets learn Django'},
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request, email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username OR password does not exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('land')

def registerUser(request):
    page='register'
    form=MyUserCreationForm()
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'you made an error in registration')
    
    context={'page':page, 'form':form}
    return render(request,'base/login_register.html',context)

def home(request) :
      topics=Topic.objects.all()[0:5]
      q=request.GET.get('q') if request.GET.get('q')!=None else ''
      rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q)|Q(Description__icontains=q))
      room_count=rooms.count()
      room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
      context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages }
      return render(request, 'base/home.html', context)
  
def room(request,pk):
    room=Room.objects.get(id=pk)
    roomessages=room.message_set.all()#.order_by('created') #refer to message model
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'roomessages': roomessages,'participants':participants}
    return render(request, 'base/room.html', context)

def userp(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/userprofile.html',context)
    

@login_required(login_url='login')
def create(request):
    form=RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
             Description=request.POST.get('Description'),
        )
        #form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

login_required(login_url='login')
def updater(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # Update the room with new data from the form
        room.name = request.POST.get('name')
        room.topic = topic
        room.Description = request.POST.get('Description')
        room.save()
        
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)
    
    
   

@login_required(login_url='login')
def deleter(request,pk):
    room=Room.objects.get(id=pk)
    
    if request.user !=room.host:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})
@login_required(login_url='login')
def deletem(request,pk):
    message=Message.objects.get(id=pk)
    
    if request.user !=message.user:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=request.user)
    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    return render(request ,'base/edit-user.html',{'form':form})


def topicPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request , 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages=Message.objects.all()
    return render(request, 'base/activite.html',{'room_messages':room_messages})

def landingPage(request):
    return render(request, 'base/landingPage.html',{})
def aboutUs(request):
    return render(request, 'base/about.html',{})
def contactUs(request):
    return render(request, 'base/contact.html',{})