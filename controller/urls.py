from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_search),
    path('signup', views.render_signup),
    path('login', views.render_login),
    path('process_signup', views.process_signup),
    path('process_login', views.process_login),
    path('knownuser/search', views.knownuser_search),
    path('logout', views.logout),
]