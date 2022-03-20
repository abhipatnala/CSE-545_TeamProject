from django.template import loader
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from .models import Records
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You've visited the Medical Records page in the Patient portal.")


def medical_records(request, patient_id):
    diagnosesList = Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id')
    diagnosesJson = serializers.serialize("json", diagnosesList)

    labTestsList = Records.objects.filter(patient_id=patient_id).filter(document_type='L').order_by('records_id')
    labTestsJson = serializers.serialize("json", labTestsList)

    prescriptionsList = Records.objects.filter(patient_id=patient_id).filter(document_type='P').order_by('records_id')
    prescriptionsJson = serializers.serialize("json", prescriptionsList)

    template = loader.get_template('patient_portal/medical_records.html')
    context = {
        'diagnosesList': diagnosesJson,
        'labTestsList': labTestsJson,
        'prescriptionList': prescriptionsJson,
    }
    return HttpResponse(template.render(context, request))
    #return render(request, 'patient_portal/medical_records.html', {})


def diagnoses(request, patient_id):
    diagnosesList = Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id')
    diagnosesListCount = len(diagnosesList)
    diagnosesJson = serializers.serialize("json", diagnosesList)
    if(diagnosesListCount > 0):
        return HttpResponse(diagnosesJson)
        #return HttpResponse(type(diagnosesList))
        #return HttpResponse("Hello %s, this is the diagnoses section of the Patient Portal. There are %d diagnoses available for you. The first diagnosis is provided by Doctor %s" % (patient_id, diagnosesListCount, diagnosesList[0].doctor_id_id))
    else:
        return HttpResponse("There are no diagnoses currently for you...")

def lab_tests(request, patient_id):
    labTestsList = Records.objects.filter(patient_id=patient_id).filter(document_type='L').order_by('records_id')
    labTestsListCount = len(labTestsList)
    labTestsJson = serializers.serialize("json", labTestsList)
    if(labTestsListCount > 0):
        return HttpResponse(labTestsJson)
        #return HttpResponse("Hello %s, this is the lab test results section of the Patient Portal. There are %d lab test reports available for you. The first lab test report is provided by Doctor %s" % (patient_id, labTestsListCount, labTestsList[0].doctor_id_id))
    else:
        return HttpResponse(labTestsJson)
        #return HttpResponse("There are no lab test reports currently for you...")

def prescriptions(request, patient_id):
    prescriptionsList = Records.objects.filter(patient_id=patient_id).filter(document_type='P').order_by('records_id')
    prescritionsListCount = len(prescriptionsList)
    prescriptionsJson = serializers.serialize("json", prescriptionsList)
    if(prescritionsListCount > 0):
        return HttpResponse(prescriptionsJson)
        #return HttpResponse("Hello %s, this is the prescriptions section of the Patient Portal. There are %d prescriptions available for you. The first prescription is provided by Doctor %s" % (patient_id, prescritionsListCount, prescriptionsList[0].doctor_id_id))
    else:
        return HttpResponse(prescriptionsJson)
        #return HttpResponse("There are no prescriptions currently for you...")