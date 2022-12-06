
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .decorators import *

# Create your views here.
@login_required(login_url = 'login')
def home(request):
    u = request.user
    pu = Person.objects.get(user = u)

    if request.method == 'POST':
                    original_password = request.POST.get('original_password')
                    password_x1 = request.POST.get('password_x1')
                    password_x2 = request.POST.get('password_x2')
                    new_username = request.POST.get('new_username')
                    x = request.POST.get('avatar')
                    if x == 'Queen':
                        pu.profile_pic = "queen.png"
                        pu.save()
                    elif x == 'Choppa':
                        pu.profile_pic = "chopper.png"
                        pu.save()
                    elif x == 'Dorito bag':
                        pu.profile_pic = "dorito.png"
                        pu.save()
                    elif x == 'Bojack(default)':
                        pu.profile_pic = "Bojack.png"
                        pu.save()
                    if original_password != None:
                        if u.check_password(original_password) == True:
                            if password_x1 == password_x2:
                                u.set_password(password_x1)
                                u.save()
                                messages.info(request, 'Password is updated.')
                                return redirect('home')

                            else:
                                messages.info(request, 'Passwords do not match.')
                                return redirect('home')
                        else:
                                messages.info(request, 'Passwords is incorrect.')
                                return redirect('home')
                    elif new_username != None:
                        p = Person.objects.get(user = u)
                        u.username = new_username
                        u.save()
                        p.name = new_username
                        p.save()
                        messages.info(request, 'Username has been changed.')
                        return redirect('login')
                        
                    else:
                        pass




    return render(request,'app/home.html')


@login_required(login_url = 'login')
def send_message(request):
    u = request.user
    u_all = User.objects.all()
    context ={'u_all':u_all,'u':u}
    return render(request,'app/send_message.html',context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url = 'login')
def send_channel_message(request):
    u = request.user
    u_all = User.objects.all()
    context ={'u_all':u_all,'u':u}
    return render(request,'app/send_channel_message.html',context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url = 'login')
def delete_user(request,pk):
    Uall = User.objects.all()
    deletep = Person.objects.get(id = pk)
    for users in Uall:
        if users.username == deletep.name:
            udele = users
    udele.delete()
    return redirect("send_channel_message", )

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(request, username=username,password=password)

                    if user is not None:
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.info(request, 'Username or Password Is Incorrect')
                        return redirect('login')

        return render(request,'app/login.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)

                Person.objects.create(
				user = user,
                name = user.username
			)
                
                return redirect('login')
        context = {'form':form}
        return render(request,'app/register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url = 'login')
def message_dm(request,pk):
    allpeople = Person.objects.all() 
    u = request.user
    pu = Person.objects.get(user = u)
    p = Person.objects.get(id = pk)
    #reg profile rec
    pp = p.profile_pic
    #sender profile pic
    ppu = pu.profile_pic
    p = p.id
    pu = pu.id
    dm1 = DirectMessage.objects.filter(both_people = p).filter(both_people = pu)
    form = CreateMessageForm(request.POST)
    if request.method == 'POST':
        form = CreateMessageForm(request.POST)
        form = form.save(commit=False)
        form.sender = u
        form.save()
        form.both_people.add(pu)
        form.save()
        form.both_people.add(p)
        form.save()
        return redirect("message_dm",pk=pk )

    context = {'p':p,'pu':pu,'form':form,'dm1':dm1,'u':u,'pp':pp,'ppu':ppu,'allpeople':allpeople}
    return render(request,'app/direct.html',context)

@login_required(login_url = 'login')
def update_message(request,pk):
    u = request.user
    message = DirectMessage.objects.get(id = pk)
    inf = message.both_people.all()
    for i in inf:
        if i.user != u:
            x = i
    x = x.id
    form = CreateMessageForm(instance = message)
    if request.method == 'POST':
        form = CreateMessageForm(request.POST,instance = message)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect("message_dm",pk=x )
    context = {'form':form}
    return render(request,'app/direct.html',context)

@login_required(login_url = 'login')
def delete_message(request,pk):
    u = request.user
    message = DirectMessage.objects.get(id = pk)
    inf = message.both_people.all()
    for i in inf:
        if i.user != u:
            x = i
    x = x.id
    message.delete()
    return redirect("message_dm",pk=x )
    context = {'person':person,'message':message}
    return render(request,'app/direct.html',context)

