from asyncio.windows_events import NULL
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from .models import *
import django_tables2 as tables
from django.template import loader
from .tables import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from xml.dom.minidom import Document

@csrf_exempt

def getRoleBasedMenus(user_id):
    user = SHSUser.objects.filter(id = user_id)
    role = user[0].role_id
    role_name =''
    if role!=NULL:
        role_name = role.role_name
    menuList = Menu_Mapping.objects.filter(role_id = role.role_id)
    context = {
        'role_name' : role_name,
        'menuList' : menuList,
    }
    return context

def home(request):
    return render(request, 'HOME.html') 

def aboutUs(request):
    return render(request, 'ABOUT_US.html') 

def findDoc(request):
    docList = Doctor.objects.all()
    return render(request, 'FINDDOC.html',{'docList':docList}) 

def contactUs(request):
    return render(request, 'CONTACT_US.html') 

def login(request):
    return render(request, 'login.html') 

def bookAppointment(request):
    return render(request, 'BOOKAPPT.html') 

def appointmentRequests(request):
    return render(request, 'appointmentRequests.html') 

def appointments(request):
    user_id = ''
    if request.method == 'POST':
        user_id = request.POST['user_id']
    context = getRoleBasedMenus(user_id)
    template = loader.get_template('appointments.html')
    return HttpResponse(template.render(context, request))

def portal(request):
    user_id = ''
    if request.method == 'POST':
        user_id = request.POST['user_id']
    context = getRoleBasedMenus(user_id)
    template = loader.get_template('Portal.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'Portal.html') 

    
def mail(request,booking_id):
    record = Doctor_availability_booked.objects.filter(booking_id=booking_id)
    # if status=="APPROVED":
    #     subject = 'Appointment Confirmation'
    # else:
    #     subject ='Appointment Denied' 
    send_mail(
        'Appointment Confirmation',
        'Hello Your Appointment is confirmed! Please make sure to visit 10 min ahead.',
        'shsgrp1@gmail.com',
        ['lrmanogna@gmail.com'],
        fail_silently=False
    )
    return render(request, 'sentmail.html')
    

def index(request):
    return render(request, 'index.html') 

def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email'] 
        message =  request.POST['message']

        send_mail(
            message_name,
            message,
            message_email,
            ['sleevashiny@gmail.com']
        )

        return render(request, 'contact.html', {'message_name':message_name})

    else:
        return render(request, 'contact.html', {})

class TableView(tables.SingleTableView):
    table_class = SimpleTable
    queryset = Doctor_availability_booked.objects.all()
    template_name = "simple_list.html"

class DoctorViewTable(tables.SingleTableView):
    table_class = DoctorView
    queryset = Doctor_availability_booked.objects.filter()
    template_name = "simple_list.html"

def doctorView(request):
    doc_id = ''
    if request.method == "POST":
        doc_id = request.POST['docid']
    
    doctorsTable = DoctorView(Doctor_availability_booked.objects.filter(doctor_id=doc_id).filter(status='Approved').order_by('appointment_date'))
    template = loader.get_template('doctor_worklist.html')
    context = {
        'doctorsTable' : doctorsTable,
    }
    return HttpResponse(template.render(context, request))

def medical_records(request):
    patient_id = ''
    user_id = ''
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        user_id = request.POST['user_id']

    context1 = getRoleBasedMenus(user_id)

    patientDetails = PatientDetails(Patient.objects.filter(patient_id=patient_id)).as_values()
    diagnosesTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id'))
    labTestReportsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='L').order_by('records_id'))
    prescriptionsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='P').order_by('records_id'))
    paymentsList = Payments.objects.filter(patient_id=patient_id).order_by('patient_id')
    paymentsJson = serializers.serialize("json", paymentsList)

    template = loader.get_template('medical_records.html')
    context = {
        'patient_name' : patientDetails,
        'diagnosesTable' : diagnosesTable,
        'labTestReportsTable' : labTestReportsTable,
        'prescriptionsTable' : prescriptionsTable,
        'paymentsList': paymentsList,
    }
    context.update(context1)
    return HttpResponse(template.render(context, request))
    #return render(request, 'patient_portal/medical_records.html', {})

@csrf_exempt
def view_record(request):
    #patient_id = request.POST['patient_id']
    record_id = request.POST['record_id']
    record = Records.objects.filter(records_id=record_id).values('records_id', 'document', 'document_type')
    #recordJSON = serializers.serialize("json", record)
    recordString = record[0]['document']
    
    template = loader.get_template('record.html')
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

