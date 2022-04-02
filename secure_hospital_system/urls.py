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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views
from secure_hospital_system.views import TableView
from secure_hospital_system.views import InsuranceLoginRecords

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^settings/', include('django_mfa.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('home',views.home, name ='home'),
    path('aboutUs',views.aboutUs, name ='aboutUs'),
    path('findDoc',views.findDoc, name ='findDoc'),
    path('contactUs',views.contactUs, name ='contactUs'),
    path('patientContactUs',views.patientContactUs, name ='patientContactUs'),
    path('bookAppointment',views.bookAppointment, name ='bookAppointment'),
    path('appointmentApprovedMail/<int:booking_id>',views.appointmentApprovedMail, name ='appointmentApprovedMail'),
    path('appointmentDeniedMail/<int:booking_id>',views.appointmentDeniedMail, name ='appointmentDeniedMail'),
    path('appointmentconf', TableView.as_view(),name ='appointmentconf'),
    path('insuranceApprovedMail/<int:claim_id>',views.insuranceApprovedMail, name ='insuranceApprovedMail'),
    path('insuranceDeniedMail/<int:claim_id>',views.insuranceDeniedMail, name ='insuranceDeniedMail'),
    path('insuranceconf', InsuranceLoginRecords.as_view(),name ='insuranceconf'),
    # path('portal',views.portal,name='portal'),
    #path('medical_records/', views.medical_records, name='medical_records'),
    path('medicalRecords', views.medicalRecords, name='medicalRecords'),
    path('patientsViewWithFilter',views.patientsViewWithFilter,name='patientsViewWithFilter'),
    path('appointments', views.appointments,name ='appointments'),
    path('onSubmitOfNewPatientsAppointmentDetails/',views.onSubmitOfNewPatientsAppointmentDetails, name = 'onSubmitOfNewPatientsAppointmentDetails'),
    path('onSubmitOfExistingPatientsAppointmentBooking/',views.onSubmitOfExistingPatientsAppointmentBooking, name = 'onSubmitOfExistingPatientsAppointmentBooking'),
    path('sendContactUsEmail',views.sendContactUsEmail,name='sendContactUsEmail'),
    #path('insuranceLoginRecords',views.insuranceLoginRecords,name='insuranceLoginRecords'),
    path('generateBills',views.generateBills,name='generateBills'),
    path('newBillGenerated',views.newBillGenerated,name='newBillGenerated'),
    path("patient", views.view_patient, name='view_patient'),
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
    path('insurancePortal/', views.payment_records, name = "payment_records"),
    path('insurancePortal/saveInsurInfo', views.saveInsurInfo, name = 'saveInsurInfo'),
    path('insurancePortal/fileClaim', views.fileClaim, name = 'fileClaim'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]
