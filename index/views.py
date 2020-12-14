from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
import sqlframe

sql = sqlframe.SqlHandler('conf.txt', 'ZJUCourse')


# Create your views here.
def index(request):
    return render(request, 'index/index.html')


def assistant(request):
    return render(request, 'index/help.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'index/login.html')
    elif request.method == 'POST':
        rep = redirect("../class/23505/home")
        id = request.POST.get('id')
        pwd = request.POST.get('pass')
        query = "select * from User where User_ID = %s and Password = %s"

        result = sql.select(query, id, pwd)
        print(result)
        if len(result) != 1:
            return HttpResponse('no')
        else:
            print(id, result[0][1], result[0][2])

            rep.set_cookie(key='is_login', value=True)
            rep.set_cookie(key='user_id', value=str(id))
            rep.set_cookie(key='user_type', value=str(result[0][6]))
            return rep


def register(request):
    return render(request, 'index/register.html')
