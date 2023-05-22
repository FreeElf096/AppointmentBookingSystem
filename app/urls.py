from django.urls import path, include

from app.views import *

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('signupDoctor/', signupDoctor, name='signupDoctor'),
    path('signupPatient/', signupPatient, name='signupPatient'),

    
    path('doctorList/', doctorList, name='doctorList'),
    path('appointmententList/', appointmententList, name='appointmententList'),

    path('makeAppointment/', makeAppointment, name='makeAppointment'),
    path('appointmententStatus/', appointmententStatus, name='appointmententStatus'),
    path('makeSelectedDrAppointment/<int:pk>/', makeSelectedDrAppointment, name='makeSelectedDrAppointment'),

    
    path('adminPanel/', adminPanel, name='adminPanel'),
    path('doctorApprove/<int:pk>/', doctorApprove, name='doctorApprove'),
    path('doctorRefuse/<int:pk>/', doctorRefuse, name='doctorRefuse'),
    path('bookingApprove/<int:pk>/', bookingApprove, name='bookingApprove'),
    path('bookingRefuse/<int:pk>/', bookingRefuse, name='bookingRefuse'),

]

