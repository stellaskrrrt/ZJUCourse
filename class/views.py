from datetime import time

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect

import json
import os
import sys
import sqlframe
import datetime

from ZJUCourse import settings

sql = sqlframe.SqlHandler('conf.txt', 'ZJUCourse')


# Create your views here.
def home(request, class_id):
    if request.method == "GET":
        if 'is_login' in request.COOKIES:
            if request.COOKIES.get('is_login'):
                query = "select Name from User where User_ID=%s"
                name = str(sql.select(query, str(request.COOKIES.get('user_id')))[0][0])

                parameter = {
                    'class_id': class_id,
                    'output': str(request.COOKIES.get('user_id')),
                    'name': name,
                }

                return render(request, 'class/home.html', parameter)
        else:
            rep = redirect('../../')
            return rep
    else:
        return HttpResponse('pass')


def submit(request, class_id, homework_id):
    return HttpResponse('ok')


def exam(request, class_id):
    return render(request, 'class/exam.html', {'class_id': class_id})


def experiment(request, class_id):
    return render(request, 'class/experiment.html', {'class_id': class_id})


def forum(request, class_id):
    return render(request, 'class/forum.html', {'class_id': class_id})


def group(request, class_id):
    return render(request, 'class/group.html', {'class_id': class_id})


def homework(request, class_id):
    if request.method == "GET":
        if 'is_login' in request.COOKIES:
            if request.COOKIES.get('is_login'):
                user_id = request.COOKIES.get('user_id')
                query = "select Name from User where User_ID=%s"
                user_name = str(sql.select(query, user_id)[0][0])

                if 'get_assignment_score' in request.GET:
                    assignment_id = str(request.GET.get('assignment_id'))

                    name_query = "select Name from Assignment where Assignment_ID=%s"
                    name = str(sql.select(name_query, assignment_id)[0][0])

                    assignment_query = "select Score, Comment from Take_Assignment where Student_ID=%s and Assignment_ID=%s"
                    assignment_result = sql.select(assignment_query, user_id, assignment_id)

                    return JsonResponse({
                        'name': name,
                        'score': str(assignment_result[0][0]),
                        'comment': str(assignment_result[0][1]),
                    })

                sort_type = 0
                if 'type' in request.GET:
                    sort_type = request.GET['type']

                query = "select Type from User where User_ID=%s"
                result = sql.select(query, user_id)

                class_query = "select Course_ID, Semester, Year, Building, Room from Class where Class_ID=%s"
                class_result = sql.select(class_query, class_id)

                course_id = class_result[0][0]
                course_query = "select Name, Department from Course where Course_ID=%s"
                course_result = sql.select(course_query, course_id)

                teaches_query = "select Teacher_ID from Teaches where Class_ID=%s"
                teaches_result = sql.select(teaches_query, class_id)

                teacher_group = []
                for teacher_id in teaches_result:
                    teacher_query = "select Name, Email from User where User_ID=%s"
                    teacher_result = sql.select(teacher_query, teacher_id[0])
                    teacher = {
                        'name': teacher_result[0][0],
                        'email': teacher_result[0][1]
                    }
                    teacher_group.append(teacher)

                total_query = "select count(*) from Takes where Class_ID=%s"
                total_student = sql.select(total_query, class_id)[0][0]

                chapter_query = "select Chapter_Number, Name from Chapter where Class_ID=%s"
                chapter_result = sql.select(chapter_query, class_id)
                chapter_group = []

                for chapter in chapter_result:
                    temp_chapter = {
                        'number': chapter[0],
                        'name': chapter[1],
                    }
                    chapter_group.append(temp_chapter)

                if result[0][0] == 2:  # teacher
                    if sort_type == 0 or sort_type == '3':
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Expire_Time desc"
                    elif sort_type == '1':
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Create_Time desc"
                    else:
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Start_Time desc"
                    assignment_result = sql.select(assignment_query, class_id)
                    assignment_group = []
                    for element in assignment_result:
                        query_submit = "select count(*) from Take_Assignment where Assignment_ID=%s and State=2"
                        submitted = sql.select(query_submit, element[0])[0][0]
                        assignment = {
                            'id': str(element[0]),
                            'name': str(element[1]),
                            'start': str(element[2]),
                            'end': str(element[3]),
                            'type': '个人作业' if element[4] else '小组作业',
                            'submitted': str(submitted),
                        }
                        assignment_group.append(assignment)

                    parameter = {
                        'course_name': course_result[0][0],
                        'semester': class_result[0][1],
                        'year': class_result[0][2],
                        'building': class_result[0][3],
                        'room': class_result[0][4],
                        'department': course_result[0][1],
                        'teacher_group': teacher_group,
                        'assignment_group': assignment_group,
                        'total_student': total_student,
                        'chapter_group': chapter_group,
                        'name': user_name,
                    }

                    if sort_type == 0:
                        return render(request, 'class/homework_teacher.html', parameter)
                    else:
                        parameter = {
                            'assignment_group': assignment_group,
                            'total_student': total_student,
                        }

                        return JsonResponse(parameter)
                else:
                    parameter = {
                        'course_name': course_result[0][0],
                        'semester': class_result[0][1],
                        'year': class_result[0][2],
                        'building': class_result[0][3],
                        'room': class_result[0][4],
                        'department': course_result[0][1],
                        'teacher_group': teacher_group,
                        'name': user_name,
                    }

                    assignment_group = []
                    if sort_type == 0 or sort_type == '3':
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Expire_Time desc"
                    elif sort_type == '1':
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Create_Time desc"
                    else:
                        assignment_query = "select Assignment_ID, Name, Start_Time, Expire_Time, Type from Assignment where Class_ID=%s order by Start_Time desc"
                    assignment_result = sql.select(assignment_query, class_id)

                    for element in assignment_result:
                        assignment_id = str(element[0])
                        take_assignment_query = "select State, Score from Take_Assignment where Student_ID=%s and Assignment_ID=%s"
                        take_assignment_result = sql.select(take_assignment_query, user_id, assignment_id)
                        print(take_assignment_result)
                        if str(take_assignment_result[0][0]) == '1':
                            state = "未提交"
                        elif str(take_assignment_result[0][0]) == '2':
                            state = "已提交"
                        else:
                            state = "已截止"

                        assignment = {
                            'name': str(element[1]),
                            'start': str(element[2]),
                            'end': str(element[3]),
                            'type': "个人作业" if str(element[4]) == '1' else "小组作业",
                            'state': state,
                            'id': assignment_id,
                            'score': str(take_assignment_result[0][1]),
                        }

                        assignment_group.append(assignment)

                    parameter['assignment_group'] = assignment_group
                    if sort_type == 0:
                        return render(request, 'class/homework_student.html', parameter)
                    else:
                        parameter = {
                            'assignment_group': assignment_group,
                        }

                        return JsonResponse(parameter)
        else:
            rep = redirect('../../../')
            return rep
    else:
        return HttpResponse('fail')


def new_homework(request, class_id):
    chapter_number = str(request.POST.get('chapter_number')).split('\xa0')[0]
    print(chapter_number)
    name = str(request.POST.get('name'))
    description = str(request.POST.get('description'))
    percentage = int(request.POST.get('percentage'))
    create_time = str(datetime.datetime.now())

    start_time = str(request.POST.get('start_time'))
    time_list = start_time.split(' ')
    date_list = time_list[0].split('/')
    start_time = date_list[2] + '-' + date_list[0] + '-' + date_list[1] + ' ' + time_list[1] + ':00'

    expire_time = request.POST.get('expire_time')
    time_list = expire_time.split(' ')
    date_list = time_list[0].split('/')
    expire_time = date_list[2] + '-' + date_list[0] + '-' + date_list[1] + ' ' + time_list[1] + ':00'

    assignment_type = str(request.POST.get('type'))

    print(class_id, chapter_number, name, description, percentage, create_time, start_time, expire_time)

    if assignment_type == 'true':
        sql.execute("insert into Assignment values(null, %s, %s, %s, %s, %s, %s, %s, %s, true)", class_id,
                    chapter_number, name, description, percentage, create_time, start_time, expire_time)
    else:
        sql.execute("insert into Assignment values(null, %s, %s, %s, %s, %s, %s, %s, %s, false)", class_id,
                    chapter_number, name, description, percentage, create_time, start_time, expire_time)

    takes_query = "select Student_ID from Takes where Class_ID=%s"
    takes_result = sql.select(takes_query, class_id)
    for element in takes_result:
        student_id = str(element[0])
        insert_take_assignment = "insert into Take_Assignment values(null, %s, %s, null, null, 0, 1, '')"
        sql.execute(insert_take_assignment, student_id,
                    str(sql.select("select max(Assignment_ID) from Assignment")[0][0]))

    return HttpResponse('ok')


def FileUploads(request, class_id):
    file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
    belong = request.POST.get('belong')
    user_id = request.COOKIES.get('user_id')
    upload_time = "".join(str(datetime.datetime.now()).split(':')).split('.')[0]
    create_time = str(datetime.datetime.now())
    size = file.size / 1024
    file_name = file.name
    file_type = ''
    if '.html' in file_name:
        file_type = "link"
    elif '.avi' in file_name or '.mp4' in file_name or '.rmvb' in file_name or '.mkv' in file_name or '.mov' in file_name:
        file_type = "video"
    elif '.mp3' in file_name or '.flac' in file_name or '.wav' in file_name:
        file_type = "audio"
    elif '.jpg' in file_name or '.png' in file_name or '.bmp' in file_name or '.gif' in file_name:
        file_type = "image"
    else:
        file_type = "document"

    if belong == 'assignment' or belong == 'experiment':

        route = sys.argv[0][0:len(sys.argv[0]) - 9] + 'static/Files/class/' + class_id + '/'

        chapter_number = str(request.POST.get('chapter_number')).split('\xa0')[0]

        start_time = str(request.POST.get('start'))
        time_list = start_time.split(' ')
        date_list = time_list[0].split('/')
        start_time = date_list[2] + '-' + date_list[0] + '-' + date_list[1] + ' ' + time_list[1] + ':00'

        expire_time = request.POST.get('end')
        time_list = expire_time.split(' ')
        date_list = time_list[0].split('/')
        expire_time = date_list[2] + '-' + date_list[0] + '-' + date_list[1] + ' ' + time_list[1] + ':00'

        assignment_query = "select max(Assignment_ID) from Assignment"
        assignment_id = sql.select(assignment_query)[0][0] + 1

        experiment_query = "select max(Experiment_ID) from Experiment"
        experiment_id = sql.select(experiment_query)[0][0] + 1

        modify_resource = "insert into Resource values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if belong == 'assignment':
            sql.execute("insert into Resource values(null, %s, %s, %s, null, %s, %s, %s, %s, true, %s, %s, %s)",
                        user_id, class_id, assignment_id, chapter_number, file_name,
                        size, file_type, create_time, start_time, expire_time)
        elif belong == 'experiment':
            sql.execute("insert into Resource values(null, %s, %s, null, %s, %s, %s, %s, %s, true, %s, %s, %s)",
                        user_id, class_id, experiment_id, chapter_number, file_name,
                        size, file_type, create_time, start_time, expire_time)
    else:
        route = sys.argv[0][0:len(sys.argv[0]) - 9] + 'static/Files/user/' + user_id + '/'
        if 'assignment_id' in request.POST:
            sql.execute("insert into Resource values(null, %s, %s, %s, null, '', %s, %s, %s, true, %s, now(), now())",
                        user_id, class_id, str(request.POST.get('assignment_id')), file_name, size, file_type,
                        create_time)
        if 'experiment_id' in request.POST:
            sql.execute("insert into Resource values(null, %s, %s, null, %s, '', %s, %s, %s, true, %s, now(), now())",
                        user_id, class_id, str(request.POST.get('experiment_id')), file_name, size, file_type,
                        create_time)

    if not os.path.exists(route):
        os.mkdir(route)

    f = open(route + upload_time + file.name, 'wb+')

    for chunk in file.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse('ok')


def homework_detail(request, class_id, homework_id):
    if request.method == "GET":
        if 'is_login' in request.COOKIES:
            if request.COOKIES.get('is_login'):
                user_id = request.COOKIES.get('user_id')
                query = "select Name from User where User_ID=%s"
                user_name = str(sql.select(query, user_id)[0][0])
                if 'content' in request.GET:
                    update_query = "update Take_Assignment set Submit_Time=now(), Content=%s, State=2 where Student_ID=%s and Assignment_ID=%s"
                    sql.execute(update_query, str(request.GET['content']), user_id, homework_id)
                    return HttpResponse('ok')

                query = "select Type from User where User_ID=%s"
                result = sql.select(query, user_id)

                class_query = "select Course_ID, Semester, Year, Building, Room from Class where Class_ID=%s"
                class_result = sql.select(class_query, class_id)

                course_id = class_result[0][0]
                course_query = "select Name, Department from Course where Course_ID=%s"
                course_result = sql.select(course_query, course_id)

                teaches_query = "select Teacher_ID from Teaches where Class_ID=%s"
                teaches_result = sql.select(teaches_query, class_id)

                teacher_group = []
                for teacher_id in teaches_result:
                    teacher_query = "select Name, Email from User where User_ID=%s"
                    teacher_result = sql.select(teacher_query, teacher_id[0])
                    teacher = {
                        'name': teacher_result[0][0],
                        'email': teacher_result[0][1]
                    }
                    teacher_group.append(teacher)

                assignment_query = "select Name, Percentage, Chapter_Number, Description, Create_Time, Start_Time, Expire_Time, Type from Assignment where Assignment_ID=%s"
                assignment_result = sql.select(assignment_query, homework_id)
                print(assignment_result)

                chapter_query = "select Name from Chapter where Chapter_Number=%s and Class_ID=%s"
                chapter_result = sql.select(chapter_query, str(assignment_result[0][2]), class_id)
                print(chapter_result)

                file_query = "select Name, Type, Size, Upload_Time from Resource where Class_ID=%s and Assignment_ID=%s"
                file_result = sql.select(file_query, class_id, homework_id)
                file_group = []

                for element in file_result:
                    name = str(element[0])
                    file_type = str(element[1])
                    if '.pdf' in name:
                        file_type = 'pdf'
                    elif '.doc' in name:
                        file_type = 'word'
                    elif '.xls' in name:
                        file_type = 'excel'
                    elif '.ppt' in name:
                        file_type = 'powerpoint'
                    elif '.txt' in name:
                        file_type = 'text'
                    elif file_type == 'audio' or file_type == 'video':
                        pass
                    elif file_type == 'image':
                        file_type = 'photo'
                    elif '.rar' in name or '.zip' in name:
                        file_type = 'zip'
                    else:
                        file_type = 'code'
                    file = {
                        'name': name,
                        'type': file_type,
                        'size': str(element[2]),
                        'link': '/static/Files/class/' + class_id + '/' + "".join(str(element[3]).split(':')) + name,
                    }
                    file_group.append(file)

                print(file_group)
                parameter = {
                    'course_name': course_result[0][0],
                    'semester': class_result[0][1],
                    'year': class_result[0][2],
                    'building': class_result[0][3],
                    'room': class_result[0][4],
                    'department': course_result[0][1],
                    'teacher_group': teacher_group,
                    'description': str(assignment_result[0][3]),
                    'chapter_name': str(chapter_result[0][0]),
                    'assignment_name': str(assignment_result[0][0]),
                    'percentage': str(assignment_result[0][1]),
                    'create_time': str(assignment_result[0][4]),
                    'start_time': str(assignment_result[0][5]),
                    'expire_time': str(assignment_result[0][6]),
                    'assignment_type': "个人作业" if str(assignment_result[0][7]) == '1' else "小组作业",
                    'assignment_id': homework_id,
                    'file_group': file_group,
                    'name': user_name,
                }

                user_type = str(request.COOKIES.get('user_type'))
                if user_type == '2':
                    return render(request, 'class/homework_detail_teacher.html', parameter)
                else:
                    return render(request, 'class/homework_detail_student.html', parameter)
        else:
            rep = redirect('/')
            return rep

    elif request.method == 'POST':
        return HttpResponse('fail')


def homework_check(request, class_id, homework_id):
    if request.method == "GET":
        if 'is_login' in request.COOKIES:
            if request.COOKIES.get('is_login'):
                user_id = request.COOKIES.get('user_id')
                query = "select Name from User where User_ID=%s"
                user_name = str(sql.select(query, user_id)[0][0])
                query = "select Type from User where User_ID=%s"
                result = sql.select(query, user_id)

                class_query = "select Course_ID, Semester, Year, Building, Room from Class where Class_ID=%s"
                class_result = sql.select(class_query, class_id)

                course_id = class_result[0][0]
                course_query = "select Name, Department from Course where Course_ID=%s"
                course_result = sql.select(course_query, course_id)

                teaches_query = "select Teacher_ID from Teaches where Class_ID=%s"
                teaches_result = sql.select(teaches_query, class_id)

                teacher_group = []
                for teacher_id in teaches_result:
                    teacher_query = "select Name, Email from User where User_ID=%s"
                    teacher_result = sql.select(teacher_query, teacher_id[0])
                    teacher = {
                        'name': teacher_result[0][0],
                        'email': teacher_result[0][1]
                    }
                    teacher_group.append(teacher)

                takes_query = "select Student_ID from Takes where Class_ID=%s"
                takes_result = sql.select(takes_query, class_id)
                student_group = []

                for takes in takes_result:
                    student_id = str(takes[0])
                    student_query = "select Name from User where User_ID=%s"
                    student_result = sql.select(student_query, student_id)

                    take_assignment_query = "select State, Score from Take_Assignment where Student_ID=%s and Assignment_ID=%s"
                    take_assignment_result = sql.select(take_assignment_query, student_id, homework_id)

                    if str(take_assignment_result[0][0]) == '2':
                        state = "已提交"
                    elif str(take_assignment_result[0][0] == '1'):
                        state = "未提交"
                    else:
                        state = "已过期"

                    temp_student = {
                        'id': student_id,
                        'name': str(student_result[0][0]),
                        'state': state,
                        'score': str(take_assignment_result[0][1]),
                    }
                    student_group.append(temp_student)

                parameter = {
                    'course_name': course_result[0][0],
                    'semester': class_result[0][1],
                    'year': class_result[0][2],
                    'building': class_result[0][3],
                    'room': class_result[0][4],
                    'department': course_result[0][1],
                    'teacher_group': teacher_group,
                    'student_group': student_group,
                    'name': user_name,
                    'assignment_name': str(
                        sql.select("select Name from Assignment where Assignment_ID=%s", homework_id)[0][0]),
                }

                user_type = str(request.COOKIES.get('user_type'))
                if user_type == '2':
                    return render(request, 'class/homework_check.html', parameter)
                else:
                    rep = redirect('../detail/')
                    return rep
        else:
            rep = redirect('/')
            return rep

    else:
        return HttpResponse('fail')


def check_detail(request, class_id, homework_id):
    if request.method == 'GET':
        result = {}
        student_id = request.GET.get('student_id')

        assignment_query = "select Content from Take_Assignment where Student_ID=%s and Assignment_ID=%s"
        assignment_result = sql.select(assignment_query, student_id, homework_id)
        print(assignment_result)

        result['content'] = str(assignment_result[0][0])
        result['class_id'] = class_id

        file_query = "select Resource_ID, Name, Type, Size, Upload_Time from Resource where Upload_User_ID=%s and Class_ID=%s and Assignment_ID=%s"
        file_result = sql.select(file_query, student_id, class_id, homework_id)

        print(file_result)

        for i in range(len(file_result)):
            file = file_result[i]
            name = str(file[1])
            file_type = str(file[2])
            if '.pdf' in name:
                file_type = 'pdf'
            elif '.doc' in name:
                file_type = 'word'
            elif '.xls' in name:
                file_type = 'excel'
            elif '.ppt' in name:
                file_type = 'powerpoint'
            elif '.txt' in name:
                file_type = 'text'
            elif file_type == 'audio' or file_type == 'video':
                pass
            elif file_type == 'image':
                file_type = 'photo'
            elif '.rar' in name or '.zip' in name:
                file_type = 'zip'
            else:
                file_type = 'code'

            file_group = {
                'id': str(file[0]),
                'name': name,
                'type': file_type,
                'size': str(file[3]) + 'KB',
                'real_name': "".join(str(file[4]).split(':')) + name,
            }

            result['file_group' + str(i)] = file_group

        print(result)
        return JsonResponse(result)


def new_score(request, class_id, homework_id):
    student_id = str(request.POST.get('student_id'))
    score_get = str(request.POST.get('score'))
    comment = str(request.POST.get('comment'))

    update_query = "update Take_Assignment set Score=%s, Comment=%s where Student_ID=%s and Assignment_ID=%s"
    sql.execute(update_query, score_get, comment, student_id, homework_id)

    return HttpResponse('ok')


def material(request, class_id):
    return render(request, 'class/material.html', {'class_id': class_id})


def notification(request, class_id):
    return render(request, 'class/notification.html', {'class_id': class_id})


def score(request, class_id):
    return render(request, 'class/viewScore.html', {'class_id': class_id})
