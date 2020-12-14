from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'course/index.html')


def information(request, course_id):
    return render(request, 'course/CourseHome.html', {'id': course_id})
