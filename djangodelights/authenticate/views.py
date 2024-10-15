from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user()) #form.get_user() returns a user object
            return redirect('inventory:profit')
        else: 
            messages.success(request, ("Incorrrect username and/or password"))
            return redirect('login')
            
    else: 
        form = AuthenticationForm() #if the request method is GET, render an empty form
    
    return render(request, "authenticate/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('authenticate:login')
            
    