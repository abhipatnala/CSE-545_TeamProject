from django.shortcuts import render
from django.http import HttpResponse
from .models import Records, Patient
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You've visited the Medical Records page in the Patient portal.")

def diagnosis(request, patient_id):
    diagnosisList = Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id')
    diagnosisListCount = len(diagnosisList)
    return HttpResponse("Hello %s, this is the diagnosis section of the Patient Portal. There are %d diagnosis available for you. The Diagnosis is provided by Doctor %s" % (patient_id, diagnosisListCount, diagnosisList[0].doctor_id_id))

def lab_tests(request, patient_id):
    return HttpResponse("Lab Test Reports...")