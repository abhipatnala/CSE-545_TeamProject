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
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^settings/', include('django_mfa.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('medical_records/', views.MedicalRecordsListView.as_view(), name='MedicalRecordsListView'),
    path('patient_portal/medical_records', views.medical_records, name='medical_records'),
    path('patient_portal/view_appointment', views.view_appointment, name='view_appointment'),
    path('patient_portal/view_record', views.view_record, name='view_record'),
    path('<int:patient_id>/diagnoses', views.diagnoses, name='diagnoses'),
    path('<int:patient_id>/lab_tests', views.lab_tests, name='lab_tests'),
    path('<int:patient_id>/prescriptions', views.prescriptions, name='lab_tests'),
    path('<int:patient_id>/payments', views.transaction, name='transaction'),
    path('doctor_portal/worklist', views.doctorView,name='doctorView'),
    path('doctor_portal/view_appointment', views.view_appointment, name='view_appointment'),
    path('patient_portal/edit_record', views.edit_record, name='edit_record'),
]
