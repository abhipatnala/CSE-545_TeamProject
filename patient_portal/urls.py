from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='medical_records'),
    path('<int:patient_id>/diagnosis', views.diagnosis, name='diagnosis'),
    path('<int:patient_id>/lab_tests', views.lab_tests, name='lab_tests')
]