import datetime
import random
import string
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from .forms import *
import pyqrcode
from pyqrcode import QRCode
import png

# Create your views here.
# create a global dictionary to store the keys
keys = {}

@unauthenticated_user 
def Login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user_auth = authenticate(username=username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('HomeFaculty')
        return render(request, 'attendance/login.html')

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Faculty'])
def GenerateQR(request, courseid):
    # generate qr code
    # genetate an alphanumeric random string
    
    key1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    key2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # time and date
    time = datetime.datetime.now()
    date = time.strftime("%d%m%Y")
    time = time.strftime("%H%M%S")

    # save the keys in the global dictionary
    keys[courseid+str(date)+str(time)+'Key1'] = key1
    keys[courseid+str(date)+str(time)+'Key2'] = key2

    s = "127.0.0.1:8001/MarkAttendance/"+courseid+"/"+str(date)+"/"+str(time)+"/"+key1+"/"+key2
    # print(s)
    # print(courseid, date, time, key1, key2)
# Generate QR code
    url = pyqrcode.create(s)
    
    # Create and save the png file naming "myqr.png"
    url.png('static/images/myqr1.png', scale = 6)
    return render(request, 'attendance/Faculty/GenerateQR.html',{'myqr': 'myqr.png', 's': s,'courseid':courseid,'key1':key1,'key2':key2,'date':str(date),'time':str(time)})

def MarkAttendance(request, courseid, date, time, key1, key2):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    valid = False

    timeobj = datetime.datetime.now()
    timedt = datetime.datetime.strptime(time, "%H%M%S")
    if (timeobj-timedt).seconds > 100:
        print('Attendance Marking Time Over')
        valid = False
        return HttpResponse('Attendance Marking Time Over')
    else:
        valid = True
    if courseid+str(date)+str(time)+'Key1' in keys and courseid+str(date)+str(time)+'Key2' in keys:
        if keys[courseid+str(date)+str(time)+'Key1'] == key1 and keys[courseid+str(date)+str(time)+'Key2'] == key2:
            valid=True
            print('Keys found')


    

    if request.method == 'POST':
        print('POST')
        if courseid+str(date)+str(time)+'Key1' in keys and courseid+str(date)+str(time)+'Key2' in keys:
            print('Keys found')
            if keys[courseid+str(date)+str(time)+'Key1'] == key1 and keys[courseid+str(date)+str(time)+'Key2'] == key2:
                print('Keys Matched')
                datec = timeobj.strftime("%d%m%Y")
                timec = timeobj.strftime("%H%M%S")

                datec = datetime.datetime.strptime(datec, "%d%m%Y")
                date = datetime.datetime.strptime(date, "%d%m%Y")
                timecdt = datetime.datetime.strptime(timec, "%H%M%S")
                timedt = datetime.datetime.strptime(time, "%H%M%S")
                print(timecdt-timedt)

                if (datec-date).days == 0 and (timecdt-timedt).seconds <= 10:
                    rollno = request.POST['Roll']
                    data_from_id = TimeTable.objects.filter(id=courseid)
                    subject = data_from_id[0].Subject
                    code=data_from_id[0].Code
                    batch=data_from_id[0].Batch
                    room=data_from_id[0].RoomNo
                    print(rollno, subject, code, batch, room)
                    data={
                        'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                        'Subject': subject,
                        'Code': code,
                        'Batch': batch,
                        'RoomNo': room,
                        'RollNo': rollno,
                        'ips': ip,
                    }
                    form = AttendanceForm(data)
                    print(form.errors)
                    if form.is_valid():
                        form.save()
                        print('Attendance Marked')
                else:
                    print('Attendance Marking Time Over')
                    return HttpResponse('Attendance Marking Time Over')
    # return HttpResponse('Attendance Marked')
    return render(request, 'attendance/MarkAttendance.html', {'valid': valid})

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Faculty'])
def HomeFaculty(request):

    tt=TimeTable.objects.filter(Faculty_id=request.user.username)
    mon=TimeTable.objects.filter(Faculty_id=request.user.username,Day='Monday')
    tue=TimeTable.objects.filter(Faculty_id=request.user.username,Day='Tuesday')
    wed=TimeTable.objects.filter(Faculty_id=request.user.username,Day='Wednesday')
    thu=TimeTable.objects.filter(Faculty_id=request.user.username,Day='Thursday')
    fri=TimeTable.objects.filter(Faculty_id=request.user.username,Day='Friday')
    if request.method == 'POST':
        TimeTable.objects.filter(Faculty_id=request.user.username).delete()
        data=request.POST
        # print(request.POST)
        data=dict(data)
        # print(data['course'])
        # print(data['class'])
        # print(data['room'])
        # print(data['batch'])
        # print(request.user.username)
        day=['Monday','Tuesday','Wednesday','Thursday','Friday']
        daypos=0
        start=9
        for i in range(len(data['course'])):
            if start==13:
                start=14
            if start==16:
                daypos=daypos+1
                start=9
            if data['batch'][i]=='none':
                # print(day[daypos],i,data['batch'][i],start,(start+1))
                if data['course'][i]=='':
                    data['course'][i]='Free'
                if data['class'][i]=='':
                    data['class'][i]='Free'
                if data['room'][i]=='':
                    data['room'][i]='Free'
                if data['batch'][i]=='':
                    data['batch'][i]='Free'
                dict1={
                    'csrfmiddlewaretoken':data['csrfmiddlewaretoken'][0],
                    'Faculty_id':str(request.user.username),
                    'Day':day[daypos],
                    'Subject':data['course'][i],
                    'Code':data['class'][i],
                    'RoomNo':data['room'][i],
                    'Batch':data['batch'][i],
                    'Start':str(start),
                    'End':str(start+1)
                }
                form=TimeTableForm(dict1)
                # print(form.errors)
                if form.is_valid():
                    form.save()
                # print(dict1)
                start=start+1

            else:
                # print(day[daypos],i,data['batch'][i],start,(start+2))
                if data['course'][i]=='':
                    data['course'][i]='Free'
                if data['class'][i]=='':
                    data['class'][i]='Free'
                if data['room'][i]=='':
                    data['room'][i]='Free'
                if data['batch'][i]=='':
                    data['batch'][i]='Free'
                dict1={
                    'csrfmiddlewaretoken':data['csrfmiddlewaretoken'][0],
                    'Faculty_id':str(request.user.username),
                    'Day':day[daypos],
                    'Subject':data['course'][i],
                    'Code':data['class'][i],
                    'RoomNo':data['room'][i],
                    'Batch':data['batch'][i],
                    'Start':str(start),
                    'End':str(start+2)
                }
                form=TimeTableForm(dict1)
                if form.is_valid():
                    # delete the previous entry
                    form.save()
                # print(form.is_valid())
                # print(form.errors)
                # print(dict1)
                start=start+2
        return redirect('HomeFaculty')
        # print(request.POST)
        # print("yes")
    return render(request, 'attendance/Faculty/Home.html',{'mon':mon,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'tt':tt})

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Faculty'])
def EditTT(request):
    if request.method == 'POST':
        TimeTable.objects.filter(Faculty_id=request.user.username).delete()
        data=request.POST
        # print(request.POST)
        data=dict(data)
        # print(data['course'])
        # print(data['class'])
        # print(data['room'])
        # print(data['batch'])
        # print(request.user.username)
        day=['Monday','Tuesday','Wednesday','Thursday','Friday']
        daypos=0
        start=9
        for i in range(len(data['course'])):
            if start==13:
                start=14
            if start==16:
                daypos=daypos+1
                start=9
            if data['batch'][i]=='none':
                # print(day[daypos],i,data['batch'][i],start,(start+1))
                if data['course'][i]=='':
                    data['course'][i]='Free'
                if data['class'][i]=='':
                    data['class'][i]='Free'
                if data['room'][i]=='':
                    data['room'][i]='Free'
                if data['batch'][i]=='':
                    data['batch'][i]='Free'
                dict1={
                    'csrfmiddlewaretoken':data['csrfmiddlewaretoken'][0],
                    'Faculty_id':str(request.user.username),
                    'Day':day[daypos],
                    'Subject':data['course'][i],
                    'Code':data['class'][i],
                    'RoomNo':data['room'][i],
                    'Batch':data['batch'][i],
                    'Start':str(start),
                    'End':str(start+1)
                }
                form=TimeTableForm(dict1)
                # print(form.errors)
                if form.is_valid():
                    form.save()
                # print(dict1)
                start=start+1

            else:
                # print(day[daypos],i,data['batch'][i],start,(start+2))
                if data['course'][i]=='':
                    data['course'][i]='Free'
                if data['class'][i]=='':
                    data['class'][i]='Free'
                if data['room'][i]=='':
                    data['room'][i]='Free'
                if data['batch'][i]=='':
                    data['batch'][i]='Free'
                dict1={
                    'csrfmiddlewaretoken':data['csrfmiddlewaretoken'][0],
                    'Faculty_id':str(request.user.username),
                    'Day':day[daypos],
                    'Subject':data['course'][i],
                    'Code':data['class'][i],
                    'RoomNo':data['room'][i],
                    'Batch':data['batch'][i],
                    'Start':str(start),
                    'End':str(start+2)
                }
                form=TimeTableForm(dict1)
                if form.is_valid():
                    # delete the previous entry
                    form.save()
                # print(form.is_valid())
                # print(form.errors)
                # print(dict1)
                start=start+2
        return redirect('HomeFaculty')
            # set the values in the TimeTable model
            # dict1 = {
            #     'Faculty_id': request.user.username,
            #     'Day': data['day'][i],

            # print(data['course'][i])
            # print(data['class'][i])
            # print(data['room'][i])
            # print(data['batch'][i])
        
    return render(request, 'attendance/Faculty/EditTT.html')

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Faculty'])
def BuildTT(request):
    
    if request.method == 'POST':
        data=request.POST
        # print(data['course'])
        # print(data.getlist('class'))
        # print(data.getlist('room'))
        # print(data.getlist('batch'))

    return render(request, 'attendance/Faculty/BuildTT.html')

def LogoutUser(request):
    logout(request)
    return redirect('Login')
