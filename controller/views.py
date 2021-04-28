from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from .models import User, Search, Article
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
        user = User.objects.get(email=request.session['email'])
        searches = []
        if user.searches.exists():
            for search in user.searches.all():
                searches += [search.content]
        context = {
            'user': user,
            'searches': searches
        }
        return render(request, 'knownuser_search.html', context)

def knownuser_search_input_already_received(request, received_search):
    if 'email' in request.session.keys():
        user = User.objects.get(email=request.session['email'])
        searches = []
        if user.searches.exists():
            for search in user.searches.all():
                searches += [search.content]
        context = {
            'user': user,
            'searches': searches,
            'received_search': received_search
        }
        print(received_search)
        return render(request, 'knownuser_search.html', context)

def record_search(request):
    if request.method == 'POST':
        print(request.POST)
        for item in request.POST.lists():
            print(item)
        obj = Search.objects.create(
            user=User.objects.get(email=request.session['email']),
            content=request.POST['content']
        )
        serialized_obj = serializers.serialize('json', [ obj, ])
        return JsonResponse({'obj': serialized_obj})
    
def logout(request):
    request.session.flush()
    return redirect('/')