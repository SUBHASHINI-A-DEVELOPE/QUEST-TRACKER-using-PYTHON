from django.shortcuts import render, redirect
from .forms import NewUser, TaskForm, UpdateForm, contactform
from .models import new_user, Task
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as user_login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# ========== method-to-access-home-view ==========

def home(request):
    return render(request, 'home.html')


# ========== method-to-access-addtask-view ==========

@login_required(login_url='login')
def task(request):
    developers = new_user.objects.filter(designation='Developer')
    if request.user.is_authenticated:
        user = request.user
        if user.designation == 'Manager' or user.designation == 'Team lead':
            if request.method == 'POST':
                form = TaskForm(request.POST)
                if form.is_valid():
                    task = form.save(commit=False)
                    task.unique_user = request.user
                    task.developer = request.POST.get('developer')
                    task.save()
                    messages.info(request, 'Task Added Successfully')
                    return redirect('quest')
            else:
                form = TaskForm()
        else:
            return redirect('viewtask')
    else:
        form = TaskForm()
    return render(request, 'quest.html', {'form': form, 'dev': developers})


# ========== method-to-access-viewtask-view ==========

@login_required(login_url='login')
def viewtask(request):
    if request.user.is_authenticated:
        user = request.user
        if user.designation == 'Developer':
            username = user.username
            designation = False
            devPage = False
            tasks = Task.objects.filter(developer=username)
        else:
            tasks = Task.objects.all()
            designation = True
            devPage = True
        if user.designation == 'Team Lead':
            devPage = False
    return render(request, 'view_task.html', {'tasks': tasks, 'designation': designation, 'devPage': devPage})


# ========== method-to-access-viewdevelopers-view ==========

@login_required(login_url='login')
def viewdev(request):
    if request.user.is_authenticated:
        user = request.user
        if user.designation == 'Manager':
            devs = new_user.objects.exclude(designation='Manager')
    return render(request, 'view_dev.html', {'devs': devs})


# ========== method-to-access-updatetask-view ==========

@login_required(login_url='login')
def updatetask(request, id):
    ls = Task.objects.get(id=id)
    form = UpdateForm(request.POST or None, instance=ls)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('viewtask')
    return render(request, "update_task.html", {'ls': ls, 'form': form})


# ========== method-to-access-deletetask-view ==========

@login_required(login_url='login')
def deletetask(request, id):
    ls = Task.objects.get(id=id)
    ls.delete()
    return redirect('viewtask')


# ========== method-to-access-deletedevelopers-view ==========

@login_required(login_url='login')
def deletedev(request, id):
    ls = new_user.objects.get(id=id)
    ls.delete()
    return redirect('viewdev')


# ========== method-to-access-contact-view ==========

def contact(response):
    if response.method == 'POST':
        form = contactform(response.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            form.save()
            send_mail(name, message, email, ['rahulsquads@gmail.com'])
            return redirect('home')
    else:
        form = contactform()
    return render(response, 'contact.html', {'form': form})


# ========== method-to-access-login-view ==========

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            user_login(request, user)
            return redirect('quest')
        else:
            messages.error(request, 'Username and Password Incorrect')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# ========== method-to-access-signup-view ==========

def signup(request):
    if request.method == "POST":
        form = NewUser(request.POST, request.FILES)
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        uname = new_user.objects.filter(username=username)
        if password1 == password2:
            if uname:
                messages.info(request, 'Username taken')
            elif form.is_valid():
                user = form.save()
                return redirect('login')
            else:
                messages.info(request, 'Password too short')
        else:
            messages.info(request, 'Password mismatch')
    else:
        form = NewUser()
    return render(request, 'registration/signup.html', {'form': form})
