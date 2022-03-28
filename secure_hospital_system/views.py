from multiprocessing import context
from re import template
from urllib import request
from xml.dom.minidom import Document
from django.template import loader
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctor_availability_booked, Patient, Records, Payments
from .tables import DoctorView, PatientDetails, RecordsTable
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You've visited the Medical Records page in the Patient portal.")

@csrf_exempt
def medical_records(request):

    patient_id = ''
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
    elif request.method == 'GET':
        patient_id = request.GET['patient_id']
    #patientDetails = PatientDetails(Patient.objects.filter(patient_id=patient_id)).as_values()


    diagnosesTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id'))
    labTestReportsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='L').order_by('records_id'))
    prescriptionsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='P').order_by('records_id'))

    paymentsList = Payments.objects.filter(patient_id=patient_id).order_by('patient_id')
    paymentsJson = serializers.serialize("json", paymentsList)

    template = loader.get_template('patient_portal/medical_records.html')
    context = {
        #'patient_name' : patientDetails[0]['Patient_Name'],
        'diagnosesTable' : diagnosesTable,
        'labTestReportsTable' : labTestReportsTable,
        'prescriptionsTable' : prescriptionsTable,
        'paymentsList': paymentsList,
    }
    return HttpResponse(template.render(context, request))
    #return render(request, 'patient_portal/medical_records.html', {})

@csrf_exempt
def view_record(request):
    #patient_id = request.POST['patient_id']
    record_id = request.POST['record_id']
    record = Records.objects.filter(records_id=record_id).values('records_id', 'document', 'document_type')
    #recordJSON = serializers.serialize("json", record)
    recordString = record[0]['document']
    
    template = loader.get_template('patient_portal/record.html')
    context = {
        'record_id' : record_id,
        'document_type' : record[0]['document_type'],
        'document' : recordString,
    }
    return HttpResponse(template.render(context, request))

def diagnoses(request, patient_id):
    diagnosesList = Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id')
    diagnosesListCount = len(diagnosesList)
    diagnosesJson = serializers.serialize("json", diagnosesList)
    if(diagnosesListCount > 0):
        #return HttpResponse(diagnosesJson)
        return HttpResponse(diagnosesList)
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

def transaction(request, patient_id):
    paymentsList = Payments.objects.filter(patient_id=patient_id).order_by('patient_id')
    paymentsListCount = len(paymentsList)
    paymentsJson = serializers.serialize("json", paymentsList)
    #return HttpResponse("%d"%(paymentsListCount))
    #return HttpResponse("Hello %s, this is the diagnosis section of the Patient Portal. There are %d diagnosis available for you. The Diagnosis is provided by Doctor" % (patient_id, paymentsListCount))
    if(paymentsListCount > 0):
        return HttpResponse(paymentsJson)
        #return HttpResponse(type(diagnosesList))
        #return HttpResponse("Hello %s, this is the diagnoses section of the Patient Portal. There are %d diagnoses available for you. The first diagnosis is provided by Doctor %s" % (patient_id, diagnosesListCount, diagnosesList[0].doctor_id_id))
    else:
        return HttpResponse("There are no payments currently for you...")


def doctorView(request):
    doc_id=1
    if request.method == "POST":
        doc_id = request.POST['docid']
    doctorsTable = DoctorView(Doctor_availability_booked.objects.filter(doctor_id=doc_id).filter(status='Approved').order_by('appointment_date'))
    template = loader.get_template('doctor_worklist.html')
    context = {
        'doctorsTable' : doctorsTable,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def view_appointment(request):
    #patient_id = request.POST['patient_id']
    appointment_id = request.POST['appointmentid']
    #record = Records.objects.filter(records_id=record_id).values('records_id', 'document', 'document_type')
    #recordJSON = serializers.serialize("json", record)
    #recordString = record[0]['document']
    
    #template = loader.get_template('patient_portal/record.html')
    #context = {
    #    'record_id' : record_id,
    #    'document_type' : record[0]['document_type'],
    #    'document' : recordString,
    #}
    return HttpResponse("Appointment Details")