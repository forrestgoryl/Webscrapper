from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def render_search(request):
    return render(request, 'search.html')

def render_signup(request):
    return render(request, 'signup.html')

def render_login(request):
    return render(request, 'login.html')

def process_signup(request):
    if request.method == 'POST':
        errors = User.objects.validate_signup(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                    messages.error(request, value)
            return redirect('/signup')
        else:
            email = request.POST['email']
            first_name = request.POST['first_name']
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name=first_name,
                email=email,
                password=password,
            )
            request.session['email'] = email
            return redirect('/knownuser/search')
    else:
        return redirect('/signup')

def process_login(request):
    if request.method =='POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                    messages.error(request, value)
            return redirect('/login')
        else:
            email = request.POST['email']
            request.session['email'] = email
            return redirect('/knownuser/search')
    else:
        return redirect('/login')
    
def knownuser_search(request):
    if 'email' in request.session.keys():
        context = {
            'user': User.objects.get(email=request.session['email'])
        }
        return render(request, 'knownuser_search.html', context)
    
def logout(request):
    request.session.flush()
    return redirect('/')