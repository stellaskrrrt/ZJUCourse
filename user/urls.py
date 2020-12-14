from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('home/', views.home),
    path('detail/<teacher_id>/', views.detail),
    path('myCourse/', views.mycourse),
    path('myExercise/', views.myexercise),
    path('myForum/', views.myforum),
    path('myMessage/', views.mymessage),
    path('myNotification/', views.mynotification),
    path('myResource/', views.myresource),
    path('setting/', views.setting),
    path('viewMessage/', views.viewmessage),
    path('indexManager/', views.indexmanager),
    path('addCourse/', views.addcourse),
    path('addClass/', views.addclass),
    path('addTeacher/', views.addteacher),
    path('addStudent/', views.addstudent),
]