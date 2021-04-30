from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Article,Search
import bcrypt
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient

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

def bbc(request):
    if request.method =='POST':
        keyword_to_search=request.POST['searchbar']
        print(keyword_to_search)
        if 'email' in request.session.keys():
            logged_user=User.objects.get(email=request.session['email'])
            searched_keyword=logged_user.searches.filter(keyword=keyword_to_search)
            print(searched_keyword)
            if len(searched_keyword)==0:
                dk=Search.objects.create(keyword=keyword_to_search)
                dk.user.add(logged_user)
        else:
            logged_user='none'
        newsapi = NewsApiClient(api_key="959759915d66465fbff7c7ec6993daf7")
        topheadlines = newsapi.get_top_headlines(sources='bbc-news', q=keyword_to_search, language='en')
        articles = topheadlines['articles']
        desc = []
        news = []
        img = []
        content = []
        url=[]
        for i in range(len(articles)):
            if True: #keyword in articles[i]['title'] or keyword in articles[i]['description']:
                myarticles = articles[i]
                news.append(myarticles['title'])
                desc.append(myarticles['description'])
                img.append(myarticles['urlToImage'])
                content.append(myarticles['content'])
                url.append(myarticles['url'])
        mylist = zip(news, desc, img, content,url)
        context={
            "mylist":mylist,
            "curr_user":logged_user
        }
        return render(request, 'bbc.html', context)

def save(request,name,url):
    if 'email' not in request.session.keys():
        return redirect('/login')
    if request.method =='POST':
        logged_user=User.objects.get(email=request.session['email'])
        saved_article=logged_user.articles.filter(name=name)
        print(saved_article)
        if len(saved_article)==0:
            dk=Article.objects.create(name=name,url=url)
            dk.user.add(logged_user)
    return redirect('/knownuser/search')

def delete_searches(request):
    if 'email' not in request.session.keys():
        return redirect('/login')
    logged_user=User.objects.get(email=request.session['email'])
    searches_to_remove=logged_user.searches.all()
    for search in searches_to_remove:
        logged_user.searches.remove(search)
    return redirect('knownuser/search')

def delete_articles(request):
    if 'email' not in request.session.keys():
        return redirect('/login')
    logged_user=User.objects.get(email=request.session['email'])
    articles_to_remove=logged_user.articles.all()
    for article in articles_to_remove:
        logged_user.articles.remove(article)
    return redirect('knownuser/search')

