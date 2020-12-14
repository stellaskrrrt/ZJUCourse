from django.urls import path
from . import views

urlpatterns = [
    path('<class_id>/home/', views.home),
    path('<class_id>/exam/', views.exam),
    path('<class_id>/experiment/', views.experiment),
    path('<class_id>/forum/', views.forum),
    path('<class_id>/group/', views.group),
    path('<class_id>/homework/', views.homework),
    path('<class_id>/material/', views.material),
    path('<class_id>/notification/', views.notification),
    path('<class_id>/viewScore/', views.score),
    path('<class_id>/homework/<homework_id>/detail/', views.homework_detail),
    path('<class_id>/homework/<homework_id>/check/', views.homework_check),
    path('<class_id>/homework/<homework_id>/submit/', views.submit),
    path('<class_id>/homework/<homework_id>/check_detail/', views.check_detail),
    path('<class_id>/homework/<homework_id>/new_score/', views.new_score),
    path('<class_id>/FileUploads/', views.FileUploads),
    path('<class_id>/homework/new_homework/', views.new_homework),
]
