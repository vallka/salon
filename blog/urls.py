from django.urls import path

from .views import *

app_name = 'blog'


urlpatterns = [
    #path('', ListView.as_view(), name='list'),
    #path('home/', HomeView.as_view(), name='home'),
    #path('', HomeView.as_view(), name='list'),
    path('', PostView.as_view(), name='list'),
    path('category/<str:slug>/', HomeView.as_view(), name='post-by-cat'),
    #path('translate/<str:slug>', translate, name='translate'),
    path('<str:slug>/', PostView.as_view(), name='post_en'),
    path('<str:slug>/<str:lang>/', PostView.as_view(), name='post'),
]
