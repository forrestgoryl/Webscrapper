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
    path('bbc', views.bbc),
    path('save/<str:name>/<path:url>',views.save),
    path('deletesearches',views.delete_searches),
    path('deletearticles',views.delete_articles),
   

]