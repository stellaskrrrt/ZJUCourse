from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'user/index.html')


def detail(request, teacher_id):
    return render(request, 'user/detail.html', {'id': teacher_id})


def home(request):
    return render(request, 'user/home.html')


def mycourse(request):
    return render(request, 'user/myCourse.html')


def myexercise(request):
    return render(request, 'user/myExercise.html')


def myforum(request):
    return render(request, 'user/myForum.html')


def mymessage(request):
    return render(request, 'user/myMessage.html')


def mynotification(request):
    return render(request, 'user/myNotification.html')


def myresource(request):
    return render(request, 'user/myResource.html')


def setting(request):
    return render(request, 'user/setting.html')


def viewmessage(request):
    return render(request, 'user/viewMessage.html')


def indexmanager(request):
    return render(request, 'user/indexManager.html')


def addcourse(request):
    return render(request, 'user/addCourse.html')


def addclass(request):
    return render(request, 'user/addClass.html')


def addteacher(request):
    return render(request, 'user/addTeacher.html')


def addstudent(request):
    return render(request, 'user/addStudent.html')