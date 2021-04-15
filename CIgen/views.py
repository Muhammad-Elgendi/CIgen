from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm

from django.contrib.auth import authenticate, login, get_user_model

def home_page(request):
    context = {
        "title":"CIgen an open source school management system",
        "content":"Hey, there this is a home page"
    }
    if request.user.is_authenticated:
        context['auth_content'] = "Hey you are authenticated to see this :)"
    return render(request,"home_page.html",context)

def about_page(request):
    context = {
        "title":"CIgen's default about page",
        "content":"Hey, there this is a about page"
    }
    return render(request,"home_page.html",context)

def contact_page(request):
    context = {
        "title":"CIgen | Contact us",
        "content":"Hey, there this is a contact page",
        "form" : ContactForm(request.POST or None)
    }
    # if request.method =="POST":
    #     print(request.POST)
    #     print(request.POST.get('name'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('subject'))
    #     print(request.POST.get('message'))
    if context.get('form').is_valid():
        print(context.get('form').cleaned_data)

    return render(request,"contact/view.html",context)

def register_page(request):
    User = get_user_model()
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username,email,password)
        print(new_user)
    context = {"form":form}
    return render(request,"auth/register.html",context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    form = LoginForm(request.POST or None)
    context = {"form":form}
    print("User logged in :",request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        # print("User logged in :",request.user.is_authenticated)

        if user is not None:
            login(request, user)
            print("User logged in :",request.user.is_authenticated)

            # Redirect to a success page.
            # context['form'] = LoginForm()
            return redirect("/dashboard")
        else:
            # Return an 'invalid login' error message.
            print("Error")

    print("User logged in :",request.user.is_authenticated)
    return render(request,"auth/login.html",context)

def home_page_old(request):
    html_ ="""
    <!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
    -->
  </body>
</html>
    """
    return HttpResponse(html_)