from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
import sqlframe
import random
import hashlib

from ZJUCourse.settings import EMAIL_HOST_USER

sql = sqlframe.SqlHandler('conf.txt', 'ZJUCourse')


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def gencode2md5(str):
    code = md5(str)
    return code


def gencode(code_len=4):
    """生成指定长度的验证码
    : param code_len :验证码的长度（默认4个字符)
    : return :由大小写字母和数字构成的随机验证码
    """
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = random.sample(all_chars, code_len)
    code = ''.join(code)
    return code


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
                        password, username, '', email, phone, 0)
            return HttpResponse('yes')


def findPassword(request):
    if request.method == 'GET':
        return render(request, 'index/findPassword.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        if email and username:
            query = "select * from User where Email = %s and User_ID = %s"
            result = sql.select(query, email, username)
            print(result)
            if len(result) == 1:
                url = 'http://127.0.0.1:8000/chPassword/' + username + '/'
                send_mail('find password', url, EMAIL_HOST_USER, [result[0][4], ], fail_silently=False)
                return HttpResponse("yes")
            else:
                return HttpResponse("no")


def chPassword(request, username):
    if request.COOKIES['is_login']:
        if request.method == 'GET':
            return render(request, 'index/chPassword.html')
        if request.method == 'POST':
            prepasswd = request.POST.get('prepasswd')
            newpasswd = request.POST.get('newpasswd')
            qurey = "update User set Password = %s where User_ID = %s"
            sql.execute(qurey, newpasswd, username)
            return HttpResponse("Yes")


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


def logout(request):
    request.COOKIES.clear()
    return HttpResponse("OK")
