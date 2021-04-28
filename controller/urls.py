from django.http.response import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_search),
    path('signup', views.render_signup),
    path('login', views.render_login),
    path('process_signup', views.process_signup),
    path('process_login', views.process_login),
    path('knownuser/search', views.knownuser_search),
    path('knownuser/search/<str:received_search>', views.knownuser_search_input_already_received),
    path('record_search/', views.record_search),
    path('logout', views.logout),
]