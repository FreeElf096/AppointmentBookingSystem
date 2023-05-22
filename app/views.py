from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.db import IntegrityError, transaction

from datetime import datetime
from django.utils import timezone

from app.models import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


#log in view
def signin(request):
    if request.method == "POST":
        this_username = request.POST['username']
        this_password = request.POST['password']
        user = authenticate(username=this_username, password=this_password)
        login(request, user)
        if user.isDoctor == True:
            return redirect('app:index')
        if user.isPatient == True:
            return redirect('app:index')
    return redirect('app:index')


#signout view
def signout(request):
    logout(request)
    return redirect('app:index')


#Doctor sign up view
def signupDoctor(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    user_obj = myCustomUser.objects.create(
                        username = request.POST['username'],
                        email = request.POST['email'],
                        password = make_password(request.POST['password'], salt=None, hasher='default'),
                        isDoctor = True,
                        firstName = request.POST['firstname'],
                        lastName = request.POST['lastname'],
                        dateOfBirth = request.POST['dateOfBirth'],
                        address = request.POST['address'],
                        contactNo = request.POST['contactNo']
                    )
                    user_obj.save()
                    doctor_obj = Doctor.objects.create(
                        user = user_obj,
                        degree = request.POST['degree'],
                        speciality = request.POST['speciality']
                    )
                    doctor_obj.save()
                    return index(request)
            except IntegrityError:
                print("Error")
    return render(request, 'signupDoctor.html')


#Patient sign up view
def signupPatient(request):
    if request.method == "POST":
        print('hi')
        if request.POST['password'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    if request.POST['password'] == request.POST['password2']:
                        user_obj = myCustomUser.objects.create(
                            firstName = request.POST['firstname'],
                            lastName = request.POST['lastname'],
                            dateOfBirth = request.POST['dateOfBirth'],
                            address = request.POST['address'],
                            contactNo = request.POST['contactNo'],
                            username = request.POST['username'],
                            email = request.POST['email'],
                            password = make_password(request.POST['password'], salt=None, hasher='default'),
                            isPatient = True
                            
                        )
                        user_obj.save()
                        patient_obj = Patient.objects.create(
                            user = user_obj,
                            gender = request.POST['gender']
                        )
                        patient_obj.save()
                        return redirect('app:index')
            except IntegrityError:
                print("Error")
    return render(request, 'signupPatient.html')


#MakeAppointment view
def makeAppointment(request):
    Doctor_list = Doctor.objects.all()
    myDict = {
        'selected_Doctor' : None,
        'doctor' : Doctor_list
    }
    if request.method == "POST":
        Appointment_obj = Appointment.objects.create(
            pname = Patient.objects.get(user = myCustomUser.objects.get(username = request.user.username)),
            doctor = Doctor.objects.filter(pk=request.POST['doctorpk']).first(),
            date = request.POST['date']
        )
        Appointment_obj.save()
        return redirect('app:index')
    return render(request, 'makeAppointment.html', myDict)

#MakeAppointment view
def makeSelectedDrAppointment(request, pk):
    selected_Doctor = Doctor.objects.get(id=pk)
    Doctor_list = Doctor.objects.all()
    
    myDict = {
        'selected_Doctor' : selected_Doctor,
        'doctor' : Doctor_list 
    }
    if request.method == "POST":
        Appointment_obj = Appointment.objects.create(
            pname = Patient.objects.get(user = myCustomUser.objects.get(username = request.user.username)),
            doctor = Doctor.objects.filter(pk=request.POST['doctorpk']).first(),
            date = request.POST['date']
        )
        Appointment_obj.save()
        return redirect('app:index')
    return render(request, 'makeAppointment.html', myDict)


def appointmententList(request):
    mydict={
        'appoinments': Appointment.objects.all(),
    }
    return render(request, 'appointmententList.html', mydict)

def appointmententStatus(request):
    if request.user.isPatient:
        try:
            mydict={
                'appoinments': Appointment.objects.filter(pname = Patient.objects.get(user = myCustomUser.objects.get(username = request.user.username))),
            }
        except:
            mydict={
                'appoinments': None,
            }
        return render(request, 'appointmententStatus.html', mydict)
    else:
        return redirect('app:index') 


#doctorList view
def doctorList(request):
    mydict={
        'doctors': Doctor.objects.all(),
    }
    return render(request, 'doctorList.html', mydict)


#admin view
def adminPanel(request):
    mydict={
        'doctors': Doctor.objects.all(),
        'patients' : Patient.objects.all(),
        'appoinments' : Appointment.objects.all(),
    }
    return render(request, 'adminPanel.html', mydict)

#doctor approve view
def doctorApprove(request, pk):
    if request.user.is_superuser:
        doctor_obj = Doctor.objects.get(pk=pk)
        doctor_obj.isApproved = True
        doctor_obj.save()
        return redirect('app:adminPanel')
    else:
        return redirect('app:index')

#doctor approve view
def doctorRefuse(request, pk):
    if request.user.is_superuser:
        doctor_obj = Doctor.objects.get(pk=pk)
        doctor_obj.isApproved = False
        doctor_obj.save()
        return redirect('app:adminPanel')
    else:
        return redirect('app:index')


#doctor approve view
def bookingApprove(request, pk):
    if request.user.is_superuser:
        obj = Appointment.objects.get(pk=pk)
        obj.isConfiremed = True
        obj.save()
        return redirect('app:adminPanel')
    else:
        return redirect('app:index')

#doctor approve view
def bookingRefuse(request, pk):
    if request.user.is_superuser:
        obj = Appointment.objects.get(pk=pk)
        obj.isConfiremed = False
        obj.save()
        return redirect('app:adminPanel')
    else:
        return redirect('app:index')

