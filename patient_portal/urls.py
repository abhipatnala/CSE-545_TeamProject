from django.urls import path

from . import views
import patient_portal

app_name = 'patient_portal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:patient_id>/medical_records', views.medical_records, name='medical_records'),
    path('<int:patient_id>/diagnoses', views.diagnoses, name='diagnoses'),
    path('<int:patient_id>/lab_tests', views.lab_tests, name='lab_tests'),
    path('<int:patient_id>/prescriptions', views.prescriptions, name='lab_tests')
]