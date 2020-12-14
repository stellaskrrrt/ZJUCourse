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
        rep = redirect("../class/23505/home/")
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
    if request.method == 'GET':
        return render(request, 'index/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        query = "select * from User where User_ID = %s"
        result = sql.select(query, username)
        print(result)
        if len(result) == 1:
            return HttpResponse('no')
        else:
            sql.execute("insert into User values(%s, %s, %s, %s, %s, %s, %s)", username,
                        password, username,'', email, phone, 0)
            return HttpResponse('yes')


def fgPassword(request):
    if request.COOKIES['is_login']:
        rep = redirect("../class/23505/home/")
        if request.method == 'GET':
            return render(request, 'index/fgPassword.html')
        if request.method == 'POST':
            email = request.POST.get('email')
            captcha = request.POST.get('captcha')
            if email and captcha:
                query = "select * from User where Email = %s"
                result = sql.select(query, email)
                print(result)
                if len(result) != 1:
                    return HttpResponse('no')
                else:
                    return rep


def chPassword(request):
    if request.COOKIES['is_login']:
        rep = redirect("../class/23505/home/")
        if request.method == 'GET':
            return render(request, 'index/chPassword.html')
        if request.method == 'POST':
            userid = request.COOKIES['user_id']
            prepasswd = request.POST.get('prepasswd')
            newpasswd = request.POST.get('newpasswd')
            qurey = "update User set Password = %s where User_ID = %s"
            sql.execute(qurey, newpasswd, userid)
            return rep


def checkPassword(request):
    if request.COOKIES['is_login']:
        if request.method == 'GET':
            return render(request, 'index/checkPassword.html')
        if request.method == 'POST':
            name = request.POST.get('name')
            prepasswd = request.POST.get('prepasswd')
            print(name, prepasswd)
            qurey = "select * from User where Name= %s and Password = %s"
            res = sql.select(qurey, name, prepasswd)
            if len(res) != 1:
                return HttpResponse('no')
            else:
                return render(request, 'index/chPassword.html')
