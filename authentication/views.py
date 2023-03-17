from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User


register_page_validation = """<!DOCTYPE html>
<html>
  <head>
    <title>Invalid</title>
  </head>
  <body>
    <h1>Please provide full details</h1>
    <a href="register">Go back to the previous page.</a>
  </body>
 </html>
"""

def register(request):
    """

    :param request: Request object.
    :return: View to register a new user.
    """
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return HttpResponse(register_page_validation)
        new_user = User.objects.create(username=username, password=make_password(password))
        new_user.save()
        messages.success(request, 'User registered Successfully')
        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    """

    :param request: Request object.
    :return: View that handles login.
    """
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'User login Successfully')
                return redirect('home')
            else:
                messages.error(request, 'Error')
                return render(request, 'login.html', {'message': "Invalid Credentials"})
        return render(request, 'login.html')
    except Exception as error:
        print(error)
