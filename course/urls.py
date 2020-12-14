from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('<course_id>/', views.information)
]