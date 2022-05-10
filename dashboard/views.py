from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hi, You're at the dashboard index.")
    else:
        return redirect("/")
