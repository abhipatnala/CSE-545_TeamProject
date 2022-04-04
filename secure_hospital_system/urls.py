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
    path('findPatientDoc',views.findPatientDoc, name ='findPatientDoc'),
    path('contactUs',views.contactUs, name ='contactUs'),
    path('patientContactUs',views.patientContactUs, name ='patientContactUs'),
    path('bookAppointmentForSelectedDoc/<int:doctor_id>',views.bookAppointmentForSelectedDoc, name ='bookAppointmentForSelectedDoc'),
    path('bookingAppointmentsByExistingPatients',views.bookingAppointmentsByExistingPatients, name ='bookingAppointmentsByExistingPatients'),
    path('bookingAppointmentsForSelectedDocByExistingPatients/<int:doctor_id>',views.bookingAppointmentsForSelectedDocByExistingPatients, name ='bookingAppointmentsForSelectedDocByExistingPatients'),
    path('bookAppointment',views.bookAppointment, name ='bookAppointment'),
    path('appointmentApprovedMail/<int:booking_id>',views.appointmentApprovedMail, name ='appointmentApprovedMail'),
    path('appointmentDeniedMail/<int:booking_id>',views.appointmentDeniedMail, name ='appointmentDeniedMail'),
    path('appointmentConf', views.appointmentApproval,name ='appointmentApproval'),
    path('insuranceApprovedMail/<int:claim_id>',views.insuranceApprovedMail, name ='insuranceApprovedMail'),
    path('insuranceDeniedMail/<int:claim_id>',views.insuranceDeniedMail, name ='insuranceDeniedMail'),
    #path('insuranceconf', InsuranceLoginRecords.as_view(),name ='insuranceconf'),
    path('patientsViewWithFilter',views.patientsViewWithFilter,name='patientsViewWithFilter'),
    path('appointments', views.appointments,name ='appointments'),
    path('onSubmitOfNewPatientsAppointmentDetails/',views.onSubmitOfNewPatientsAppointmentDetails, name = 'onSubmitOfNewPatientsAppointmentDetails'),
    path('onSubmitOfExistingPatientsAppointmentBooking/',views.onSubmitOfExistingPatientsAppointmentBooking, name = 'onSubmitOfExistingPatientsAppointmentBooking'),
    path('sendContactUsEmail',views.sendContactUsEmail,name='sendContactUsEmail'),
    path('insuranceconf',views.insuranceLoginRecords,name='insuranceLoginRecords'),
    path('addInsuranceProvider', views.addInsuranceProvider, name='addInsuranceProvider'),
    path('generateBills',views.generateBills,name='generateBills'),
    path('newBillGenerated',views.newBillGenerated,name='newBillGenerated'),
    path("patient", views.view_patient, name='view_patient'),
    path('appointments', views.appointments,name='appointments'),
    path('medicalRecords', views.medicalRecords, name='medicalRecords'),
    path('viewRecord', views.viewRecord, name='viewRecord'),
    path('editRecord', views.editRecord, name='editRecord'),
    path('saveRecord', views.saveRecord, name='saveRecord'),
    path('downloadRecord', views.downloadRecord, name='downloadRecord'),
    path('viewAppointmentDoctor', views.viewAppointmentDoctor, name='viewAppointmentDoctor'),
    path('appointments', views.appointments,name='appointments'),
    path('createDiagnosis', views.createDiagnosis, name='createDiagnosis'),
    path('recommendLabtest', views.recommendLabtest, name='recommendLabtest'),
    path('createPrescription', views.createPrescription, name='createPrescription'),
    path('labtestRequests', views.labtestRequests, name='labtestRequests'),
    path('labtestAction', views.labtestAction, name='labtestAction'),
    path('labstaffWorklist', views.labstaffWorklist, name='labstaffWorklist'),
    path('createLabtestReport', views.createLabtestReport, name='createLabtestReport'),
    path('doctorWorklist', views.doctorWorklist, name='doctorWorklist'),
    path('getAvailableSlots', views.getAvailableSlots, name='getAvailableSlots'),path('patientInsurance', views.patientInsurance, name = "patientInsurance"),
    path('saveInsurInfo', views.saveInsurInfo, name = 'saveInsurInfo'),
    path('fileClaim', views.fileClaim, name = 'fileClaim'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('updatePatient', views.updatePatient, name='updatePatient'),
    path('viewBlockChainInfo', views.viewBlockChainInfo, name='viewBlockChainInfo'),
 ]
