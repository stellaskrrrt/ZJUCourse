from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('help/', views.assistant),
    path('login/', views.login),
    path('register/', views.register),
    path('fgPassword/', views.fgPassword),
    path('checkPassword/', views.checkPassword),
    path('chPassword/', views.chPassword),
]