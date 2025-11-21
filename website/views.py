from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddRecordForm, SignUpForm
from .models import Record

def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have been logged in!')
        else:
            messages.success(request, 'There was an error, please login again...')
        return redirect('home')
    return render(request, 'home.html', {'records': records})

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome..')
            return redirect('home')
    else:
        form = SignUpForm()
        
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You must be logged in to view the home page')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record successfully deleted!')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to do that!')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if form.is_valid():
            new_record = form.save()
            messages.success(request, 'Record added successfully')
            return redirect('record', new_record.id)
    else:
        messages.success(request, 'You must be logged in to do that!')
        return redirect('home')
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    record = Record.objects.get(id=pk)
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            new_record = form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('record', new_record.id)
    else:
        messages.success(request, 'You must be logged in to do that!')
        return redirect('home')
    return render(request, 'update_record.html', {'form': form})
