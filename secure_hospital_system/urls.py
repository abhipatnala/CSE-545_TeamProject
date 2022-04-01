"""secure_hospital_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views
from secure_hospital_system.views import TableView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^settings/', include('django_mfa.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('home',views.home, name ='home'),
    path('aboutUs',views.aboutUs, name ='aboutUs'),
    path('findDoc',views.findDoc, name ='findDoc'),
    path('contactUs',views.contactUs, name ='contactUs'),
    path('bookAppointment',views.bookAppointment, name ='bookAppointment'),
    path('appointmentApprovedMail',views.appointmentApprovedMail, name ='appointmentApprovedMail'),
    path('appointmentDeniedMail',views.appointmentDeniedMail, name ='appointmentDeniedMail'),
    path('appointmentconf', TableView.as_view(),name ='appointmentconf'),
    # path('portal',views.portal,name='portal'),
    #path('medical_records/', views.medical_records, name='medical_records'),
    path('patientsViewWithFilter',views.patientsViewWithFilter,name='patientsViewWithFilter'),
    path('appointments', views.appointments,name ='appointments'),
    path('onSubmitOfNewPatientsAppointmentDetails/',views.onSubmitOfNewPatientsAppointmentDetails, name = 'onSubmitOfNewPatientsAppointmentDetails'),
    path('onSubmitOfExistingPatientsAppointmentBooking/',views.onSubmitOfExistingPatientsAppointmentBooking, name = 'onSubmitOfExistingPatientsAppointmentBooking'),
    path('sendContactUsEmail',views.sendContactUsEmail,name='sendContactUsEmail'),
    path('insuranceLoginRecords',views.insuranceLoginRecords,name='insuranceLoginRecords'),
    path('generateBills',views.generateBills,name='generateBills'),
    path('newBillGenerated',views.newBillGenerated,name='newBillGenerated'),
    path("patient", views.view_patient, name='view_patient'),
    path('medical_records', views.medical_records, name='medical_records'),
    path('view_record', views.view_record, name='view_record'),
    path('edit_record', views.edit_record, name='edit_record'),
    path('save_record', views.save_record, name='save_record'),
    path('view_appointment_doctor', views.view_appointment_doctor, name='view_appointment_doctor'),
    path('appointments', views.appointments,name='appointments'),
    path('create_diagnosis', views.create_diagnosis, name='create_diagnosis'),
    path('recommend_labtest', views.recommend_labtest, name='recommend_labtest'),
    path('create_prescription', views.create_prescription, name='create_prescription'),
    path('labtest_requests', views.labtest_requests, name='labtest_requests'),
    path('labtest_action', views.labtest_action, name='labtest_action'),
    path('labstaff_worklist', views.labstaff_worklist, name='labstaff_worklist'),
    path('create_labtest_report', views.create_labtest_report, name='create_labtest_report'),
    path('doctorsworklist',views.doctor_worklist,name='doctor_worklist'),
]
