# from asyncio.windows_events import NULL
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
from django.db.models import Subquery
import random
import string
from dateutil import parser
from datetime import date
from .filters import *
from django.contrib.messages import constants as messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .helpers import getRoleBasedMenus

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(to=reverse('admin:index'))
        else:
            context = getRoleBasedMenus(request.user.id)
            return render(request, "Portal.html", context)
            # return redirect(portal(request))
    else:
        return render(request, 'home.html') 

def aboutUs(request):
    return render(request, 'ABOUT_US.html') 

def findDoc(request):
    docList = Doctor.objects.all()
    return render(request, 'FINDDOC.html',{'docList':docList}) 

def contactUs(request):
    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Contact request submitted successfully.')
    #         return render(request, 'CONTACT_US.html', {'form': ContactForm(request.GET)})
    #     else:
    #         messages.error(request, 'Invalid form submission.')
    #         messages.error(request, form.errors)
    # else:
    #     form = ContactForm()
    # return render(request, 'CONTACT_US.html', {'form': form})
	return render(request, 'CONTACT_US.html')

def sendContactUsEmail(request):
	if request.method == 'POST':
		name = request.POST.get('cname')
		email = request.POST.get('cemail')
		phone = request.POST.get('cphone')
		msg = request.POST.get('cmsg')
	send_mail(
        'Contact Us Message from : '+name,
        msg + "\n\n\n email:\t"+ email + "\n phone:\t"+ phone,
        'shsgrp1@gmail.com',
        ['shsgrp1@gmail.com'],
        fail_silently=False
    )
	return render(request,'sentmail.html')

def bookAppointment(request):
	doctorid =1
	if request.method == 'POST':
		doctorid = request.POST['docid']
	if doctorid!= NULL:
		doctors = Doctor.objects.filter(doctor_id = doctorid)
	else:
		doctors = Doctor.objects.all()
	return render(request,"BOOKAPPT.html",{'doctors':doctors})

def appointmentRequests(request):
    return render(request, 'appointmentRequests.html') 

def appointments(request):
    context1 = getRoleBasedMenus(request.user.id)
    patient_id =1
    #patient_id = Patient.objects.filter(patient_user = user_id)
    upcomingAppointments = Doctor_availability_booked.objects.filter(patient_id=patient_id)
    upcomingAppointments  = upcomingAppointments.filter(appointment_date__gte=date.today())
    upcomingAppointments  = upcomingAppointments.filter(status='approved')
    pastAppointments = Doctor_availability_booked.objects.filter(patient_id=patient_id)
    pastAppointments  = pastAppointments.filter(appointment_date__lt=date.today())
    pastAppointments  = pastAppointments.filter(status='approved')
	
    template = loader.get_template('appointments.html')
    context = {
		'upcomingAppointment' : upcomingAppointments,
		'pastAppointment' : pastAppointments
	}
    context.update(context1)
    return HttpResponse(template.render(context, request))


def appointmentsRetrieval(request):
	if request.method == 'POST':
		patient_id = request.POST['patient_id']
		existingAppointments = Doctor_availability_booked.objects.filter(fk_patient_id=patient_id)
		existingAppointments  = existingAppointments.filter(appointment_date__gte=date.today())
		return('appointments')
	else:
		return('/')

@csrf_exempt
def newAppointments(request):
	if request.method == 'POST':
		# if doctor is selected
		if request.POST['doctor']:
			#patient_id = request.POST['patient_id']
			#doctor_id = request.POST['doctor_id']
			doctor_id = 1
			appointment_requested_date = parser.parse(request.POST['appointmentDate'])
			print("appointment_requested_date ",type(appointment_requested_date))
			#2022-03-23
			#timeslot fetching
			doctor = Doctor.objects.filter(doctor_id=doctor_id)
			print("doctor ",doctor)
			shiftObj = doctor[0].shift_id
			print("shift obj ",shiftObj)
			alreadyBlockedAppointmentSlotsForTheDoctor = Doctor_availability_booked.objects.filter(doctor_id=doctor_id)
			alreadyBlockedAppointmentSlotsForTheDoctor  = alreadyBlockedAppointmentSlotsForTheDoctor.filter(appointment_date__exact=appointment_requested_date)
			alreadyBlockedAppointmentSlotsForTheDoctor = alreadyBlockedAppointmentSlotsForTheDoctor.order_by('appointment_start_time')

			print("alreadyBlockedAppointmentSlotsForTheDoctor", alreadyBlockedAppointmentSlotsForTheDoctor)
			docShiftStartTime = shiftObj.start_time.hour
			docShiftEndTime = shiftObj.end_time.hour

			blockedAppointmentTimeSlots = []
			print('blockedAppointmentTimeSlots start ',blockedAppointmentTimeSlots)
			for blockedAppointments in alreadyBlockedAppointmentSlotsForTheDoctor.iterator():
				print('blockedAppointments.appointment_start_time ',blockedAppointments.appointment_start_time)
				blockedAppointmentTimeSlots.append(blockedAppointments.appointment_start_time.hour)

			print('blockedAppointmentTimeSlots end ',blockedAppointmentTimeSlots)
			docShiftTime = docShiftStartTime
			#print("hour docShiftTime ",docShiftTime.hour)
			#print("type hour docShiftTime ",type(docShiftTime.hour))

			availabeSlots = []
			while docShiftTime<docShiftEndTime :	
				if docShiftTime not in blockedAppointmentTimeSlots:
					availabeSlots.append(docShiftTime)
				docShiftTime = docShiftTime+ 1
		# if doctor is not selected
		########### get the atleast one day available
		return render(request,"test.html",{'availabeSlots':availabeSlots})

def newAppointmentBooking(request):
	if request.method == 'POST':
		if request.POST['doctor']:
			patient_id= request.POST['patient_id']
			doctor_id= request.POST['doctor_id']
			appointment_date = request.POST['date']
			appointment_start_time = request.POST['appointment_start_time']
			appointment_end_time = request.POST['appointment_end_time']

			doctorAvailabilityBooked = Doctor_availability_booked(patient_id=patient_id, doctor_id=doctor_id, appointment_date = date,
				appointment_start_time=appointment_start_time, appointment_end_time=appointment_end_time, booking_request_timestamp = date.today(),
				approver_id = 'AUTOMATED' ,status = 'pending')
			doctorAvailabilityBooked.save()


def getPatientDetails(request):
	if request.method == 'POST':
		#patient_id= request.POST['patient_id']
		#user_id = request.POST['user_id]
		patient_id= 1

		patientDetails = Patient.objects.filter(patient_id=patient_id)
		return patientDetails

@csrf_exempt		
def newBillGenerated(request):
	if request.method == 'POST':
		#patient_id= request.POST['patient_id']
		patient_id= 13
		overall_payment= request.POST['overallPayment']
		consultation_fee = request.POST['consultationFee']
		supplies_fee = request.POST['suppliesFee']
		admit_fee = request.POST['admitFee']
		discharge_fee = request.POST['dischargeFee']

		payments = Payments(admit_fee=admit_fee, patient_id=(getPatientDetails(request))[0], discharge_fee = discharge_fee,
			supplies_fee=supplies_fee, consultation_fee=consultation_fee, overall_payment = overall_payment, payment_generated_date = date.today(),
			payment_status = 'PENDING', payment_update_date = date.today())
		payments.save()
	#return render(request,"medical_records.html")	
	response = redirect('/medical_records/')
	return response

def generateBills(request):
    return render(request, 'generateBills.html')

def getUserDetails(userId):
	user = User.objects.filter(id=userId)
	return user


#def patients(request):
#	patient_id= 1
#	patientDetails = Patient.objects.filter(patient_id=patient_id)
#	#userId = patientDetails[0].user_id
#	userId = 3
#	userInfo = User.objects.filter(id=userId)[0]
#	return render(request,'appointmentBookingRequests.html',{'first_name':userInfo.first_name,'last_name':userInfo.last_name,'email_id':userInfo.email})

def patients(request):
	return render(request,'BookAppt.html')

def saveAppointmentDetails(request, patient):
	purposeOfVisit = request.POST['purposeOfvisit']
	doctor_preference = request.POST['DocPref']
	appointment_date_request = request.POST['appointmentDate']
	opted_slot = request.POST['AvailableSlots']
	print("appointment details")
	appointmentStartNdEndTime = opted_slot.split("-")
	appointmentEndTimeNdAMPM = appointmentStartNdEndTime[1].split(" ")
	appointment_start_time = appointmentStartNdEndTime[0]+":00 "+(appointmentEndTimeNdAMPM)[1]
	appointment_end_time = appointmentEndTimeNdAMPM[0]+":00 "+appointmentEndTimeNdAMPM[1]
		#if opted_slot == "8-9 AM":
		#	appointment_start_time = "8:00 AM"
		#	appointment_end_time = "9:00 AM" 
		#elif opted_slot == "9-10 AM":
		#	appointment_start_time = "9:00 AM"
		#	appointment_end_time = "10:00 AM"
		#elif opted_slot == "1-2 PM":
		#	appointment_start_time = "1:00 PM"
		#	appointment_end_time = "2:00 PM"
		#elif opted_slot == "4-5 PM":
		#	appointment_start_time = "4:00 PM"
		#	appointment_end_time = "5:00 PM"
	print("appointment details abou to be saved")
	doctor_preference = "Yes"
	print("doctor_preference ",doctor_preference)
	if doctor_preference == "Yes":
		doctor_id = 1
		doctorObj = Doctor.objects.filter(doctor_id=doctor_id)
		print("doctorObj",doctorObj)
		doctorAvailabilityBooked = Doctor_availability_booked(patient_id=patient, doctor_id=doctorObj[0], appointment_date = appointment_date_request,
			appointment_start_time=appointment_start_time, appointment_end_time=appointment_end_time, booking_request_timestamp = date.today(),
			status = 'PENDING')
	else:
		doctorAvailabilityBooked = Doctor_availability_booked(patient_id=patient, appointment_date = appointment_date_request,
			appointment_start_time=appointment_start_time, appointment_end_time=appointment_end_time, booking_request_timestamp = date.today(),
			status = 'PENDING') 
	doctorAvailabilityBooked.save()

def onSubmitOfExistingPatientsAppointmentBooking(request):
	userId = request.POST("user_id")
	patient = Patient.objects.filter(user_id = userId)
	saveAppointmentDetails(request, patient)
	return render(request,"test.html")
	
@csrf_exempt
#@csrf_protect 
def onSubmitOfNewPatientsAppointmentDetails(request):
	if request.method == 'POST':
		patientRoleObj = Roles.objects.filter(role_name="patient")
		print("entered patientRoleObj ", patientRoleObj)
		# patient and user details
		first_name = request.POST.get('firstname')
		print("firstName ",first_name)
		last_name = request.POST.get('lastname')
		blood_type = request.POST['blood group']
		address = request.POST['Address']
		city = request.POST['city']
		state = request.POST['state']
		zipCode = request.POST['zip']
		email = request.POST['emailInfo']
		phone_number = request.POST['phoneNumber']
		loginDate = date.today()
		print("user email ",email)
		userInfo = User.objects.filter(email = email)
		if userInfo:
			# render login html
			print("user existed ",userInfo)
			return render(request,"error.html")

		print("user about to be saved")
		user = User(password=(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))), last_login = loginDate, is_superuser = 0, username= email, first_name = first_name, last_name = last_name, email = email, is_staff = 0, is_active=0, date_joined = loginDate)
		user.save()
		print("user saved")
		shsUser = SHSUser(user=user, role_id=patientRoleObj[0])
		shsUser.save()
		insuranceProviderObj = InsuranceProvider.objects.filter(provider_name = request.POST['insuranceprovider'])
		#medical history
		allergies = request.POST['allergies']
		medicationFollowed = request.POST['medications']
		preExistingMedicalConditions = request.POST['medicalConditions']
		anyOtherMedicalDetails = request.POST['medicalInfo']
		print("about to save patient details")
		ecFirstName = request.POST['ecFirstname']
		ecLastName = request.POST['ecLastname']
		ecEmailInfo = request.POST['ecEmailInfo']
		ecPhoneNumber = request.POST['ecPhoneNumber']
		patient = Patient(update_user = shsUser, user_id = shsUser, patient_insurance_member_id = request.POST['insuranceid'], emergency_contact_firstname = ecFirstName, emergency_contact_lastname  = ecLastName, emergency_contact_phone_number = ecPhoneNumber, emergency_contact_email = ecEmailInfo, patient_insurance_provider_id=insuranceProviderObj[0], blood_type=blood_type, address = address, city = city, state= state, zipCode = zipCode, phone_number= phone_number, allergies=allergies,medicationFollowed=medicationFollowed, preExistingMedicalConditions=preExistingMedicalConditions, anyOtherMedicalDetails=anyOtherMedicalDetails)
		patient.save()
		print("patient details saved")
		#Appointment Details
		saveAppointmentDetails(request, patient)

		print("appointment details already saved")
	return render(request,"test.html")

@csrf_exempt
def appointmentApprovedMail(request):
    record = Doctor_availability_booked.objects.get(booking_id=1)
    record.status = "approved"
    record.save()
    print(record.patient_id.user_id.user.email)
    print(record.status)
    print(record.appointment_date)
    print(record.doctor_id.user_id.user.first_name)
    subject = 'Appointment Confirmation'
    body ="Dear "+record.doctor_id.user_id.user.first_name + ",\n"+"\nYour appointment has been confirmed! Below are your appointment details for your reference"+"\n\nAppointment Date:\t"+str(record.appointment_date)+"\nAppointment Timings:\t"+str(record.appointment_start_time)+" - "+str(record.appointment_end_time)+"\nDoctor Name\t:"+record.doctor_id.user_id.user.first_name+"\nTemporary login Password\t:"+record.patient_id.user_id.user.password+"\n\nThank you,\nSHS Healthcare"
    patient_email = record.patient_id.user_id.user.email
    send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
        fail_silently=False
    )
    return render(request, 'sentmail.html')
    
@csrf_exempt
def appointmentDeniedMail(request):
    record = Doctor_availability_booked.objects.get(booking_id=1)
    record.status ="denied"
    record.save()
    subject ='Appointment Denied'
    body = "Your appointment has been denied due to doctor unavailability. Please book your appointment again. We apologize for the inconvenience.\n\nThank you,\nSHS Healthcare"
    patient_email = record.patient_id.user_id.user.email
    send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
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
    queryset = Doctor_availability_booked.objects.filter(status="pending")
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

def patientsViewWithFilter(request):
	patientDetails = ''
	#roleName = request.POST['roleName']
	roleName = ''
	if roleName == "doctor":
		doctorsTable = (Doctor_availability_booked.objects.filter(doctor_id=doc_id).filter(status='Approved'))
		patientDetails = Patient.objects.filter(patient_id__in=Subquery(doctorsTable.values('patient_id')))
		# get the patients and then filter the patients
		#patientDetails =                                                                                                                                           patientDetails.filter()
	elif roleName == "labStaff":
		recordsTable = (Records.objects.exclude(LabReport__isnull=True))
		patientDetails = Patient.objects.filter(patient_id__in=Subquery(recordsTable.values('patient')))
	else:
		patientDetails = (Patient.objects.all())
		# get the patients who has lab reports as not null and then filter the patients
		#reports table
	#if request.method == "POST":
	#only get the active users
	#patientDetails = PatientDetails(Patient.objects.all())
	filter = PatientViewFilter(request.GET, queryset=patientDetails)
	patientDetails = filter.qs
	#filter = PatientViewFilter()

	template = loader.get_template('patientGrid.html')

	#return HttpResponse(template.render(context, request))
	return render(request, 'patientGrid.html', {'filter': filter, 'patientDetails': patientDetails})
	#return render(request, 'blog/filtertable2.html', {'filter': filter})


def medical_records(request):
    patient_id = request.POST['patient_id']

    context1 = getRoleBasedMenus(patient_id)

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

def insuranceLoginRecords(request):
	insuranceRequests = Claim_Request.objects.all()
	filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
	insuranceRequests = filter.qs
	return render(request, 'insuranceApproverGrid.html', {'filter': filter, 'insuranceRequests': insuranceRequests})

def view_patient(request):
	context = getRoleBasedMenus(request.user.id)
	template = loader.get_template('viewPatient.html')
	return HttpResponse(template.render(context, request))
