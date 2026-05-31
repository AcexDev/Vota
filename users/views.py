from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def login_home(request):
    return render(request, "users/loginHome.html")

def logout_view(request):
    logout(request)
    return redirect("/")