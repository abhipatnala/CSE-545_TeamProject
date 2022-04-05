# from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
from io import BytesIO
from multiprocessing import context
from re import template
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from .models import *
import django_tables2 as tables
from django.template import loader
from .tables import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
from .helpers import *
from datetime import datetime
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from .decorators import *
from django.utils import timezone
import requests
import json
from django.conf import settings
from django.utils.dateparse import parse_date
from xhtml2pdf import pisa
import http.client

def home(request):
    if request.user.is_authenticated:
        if not twofaEnabled(request.user):
            return redirect('/settings/security')
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

@login_required
@twoFARequired()
def findPatientDoc(request):
    context1 = getRoleBasedMenus(request.user.id)
    docList = Doctor.objects.all()
    context = {
		'docList':docList
	}
    context.update(context1)
    return render(request, "PATIENTDOC.html", context)

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

def patientContactUs(request):
    context = getRoleBasedMenus(request.user.id)
    return render(request, "patientContactUs.html", context)

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
        messages.success(request,"Email sent successfully")

    return render(request, 'home.html')

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def bookingAppointmentsForSelectedDocByExistingPatients(request):
	doctor_id = request.POST['docId']
	print('doctor_id ',doctor_id)
	updateContext = getRoleBasedMenus(request.user.id)
	context = {
		'doctor_id':doctor_id
	}
	context.update(updateContext)
	return render(request,"ExistingPatientsAppointmentBooking.html",context)

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def bookingAppointmentsByExistingPatients(request):
	userId = request.user
	userContext = getRoleBasedMenus(userId.id)
	doctor_id = 1
	context = {
		'doctor_id' : doctor_id
	}
	context.update(userContext)
	return render(request,"ExistingPatientsAppointmentBooking.html",context)

def bookAppointmentForSelectedDoc(request):
	#doctors = Doctor.objects.filter(doctor_id = doctor_id)
	doctor_id = request.POST['docId']
	insuranceProviders = InsuranceProvider.objects.all().values_list('provider_name', flat=True)
	insuranceProviders = list(insuranceProviders)
	return render(request,"BOOKAPPT.html",{'doctor_id':doctor_id, 'insurance_providers':insuranceProviders})

def bookAppointment(request):
	doctor_id =1 #General Physician is hard coded
	#doctors = Doctor.objects.filter(doctor_id = doctorid)
	#doctors = ''
	#if request.method == 'POST':
	#	print("inside POST bookAppointment")
	#	doctorid = request.POST['docid']
	#	if doctorid:
	#		doctors = Doctor.objects.filter(doctor_id = doctorid)
	#	else:
	#		doctors = Doctor.objects.all()
	insuranceProviders = InsuranceProvider.objects.all().values_list('provider_name', flat=True)
	insuranceProviders = list(insuranceProviders)
	return render(request,"BOOKAPPT.html",{'doctor_id':doctor_id, 'insurance_providers':insuranceProviders})

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def appointmentRequests(request):
	updateContext = getRoleBasedMenus(request.user.id)
	return render(request, 'appointmentRequests.html',updateContext) 

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def appointments(request):
	context1 = getRoleBasedMenus(request.user.id)
	#patient_id =1
	shsUser = SHSUser.objects.filter(user = request.user)
	patient_id = Patient.objects.filter(user_id=shsUser[0])
	upcomingAppointments = Doctor_availability_booked.objects.filter(patient_id=patient_id[0])
	upcomingAppointments  = upcomingAppointments.filter(appointment_date__gte=date.today())
	upcomingAppointments  = upcomingAppointments.filter(status='approved')
	upcomingAppointmentsTable = PastOrPresentAppointments(upcomingAppointments)

	pastAppointments = Doctor_availability_booked.objects.filter(patient_id=patient_id[0])
	pastAppointments  = pastAppointments.filter(appointment_date__lt=date.today())
	pastAppointments  = pastAppointments.filter(status='approved')
	pastAppointmentsTable = PastOrPresentAppointments(pastAppointments)
	
	template = loader.get_template('appointments.html')
	context = {
		'upcomingAppointment' : upcomingAppointmentsTable,
		'pastAppointment' : pastAppointmentsTable
	}
	context.update(context1)
	return HttpResponse(template.render(context, request))

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def appointmentsRetrieval(request):
	if request.method == 'POST':
		patient_id = request.POST['patient_id']
		existingAppointments = Doctor_availability_booked.objects.filter(fk_patient_id=patient_id)
		existingAppointments  = existingAppointments.filter(appointment_date__gte=date.today())
		return('appointments')
	else:
		return('/')

def getAvailableSlots(request):
	appointmentDate = request.POST['appointmentDate']
	doctorId = request.POST['doctor_id']
	doctor = Doctor.objects.get(doctor_id=doctorId)
	shift_timings = doctor.shift_id
	startTime = shift_timings.start_time
	startTimee = startTime.hour
	endTime = shift_timings.end_time
	endTimee = endTime.hour
	shiftName = shift_timings.shift_type 
	slots = []
	for i in range (startTimee,endTimee-1):
		slot = str(i)+"-"+str(i+1)
		slots.append(slot)

	data = {
		'slots' : slots,
		'doctor_id' : doctorId,
		'start_time' : startTimee,
		'end_time' : endTimee,
		'type' : shiftName,
	}
	return JsonResponse(data)

@login_required
@twoFARequired()
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
		context1 = getRoleBasedMenus(request.user.id)
		context = {
			'availabeSlots':availabeSlots
		}
		context.update(context1)
		return render(request,"test.html",context)

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


@login_required
@twoFARequired()
def getPatientDetails(request):
	if request.method == 'POST':
		patient_id= request.POST['patient_id']
		#user_id = request.POST['user_id]
		#patient_id= 13 

		patientDetails = Patient.objects.filter(patient_id=patient_id)
		return patientDetails

@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def newBillGenerated(request):
	#if request.method == 'POST':
	userId = request.user
	role = getCurrentUserRole(userId)
	patient_id= request.POST['patient_id']
	#patient_id= 13
	#overall_payment= request.POST['overallPayment']
	consultation_fee = request.POST['consultationFee']
	supplies_fee = request.POST['suppliesFee']
	admit_fee = request.POST['admitFee']
	discharge_fee = request.POST['dischargeFee']

	overall_payment = int(consultation_fee)+int(supplies_fee)+int(admit_fee)+int(discharge_fee)

	payments = Payments(admit_fee=admit_fee, patient_id=(getPatientDetails(request))[0], discharge_fee = discharge_fee,
		supplies_fee=supplies_fee, consultation_fee=consultation_fee, overall_payment = overall_payment, payment_generated_date = date.today(),
		payment_status = 'pending', payment_update_date = date.today())
	payments.save()
	userContext = getRoleBasedMenus(userId)
	context = {
		'patient_id' : request.POST['patient_id']
	}
	context.update(userContext)
	return medicalRecords(request)	
	#response = redirect('/medicalRecords/'+patient_id)
	#return response

@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def generateBills(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	userContext = getRoleBasedMenus(userId)
	context = {
		'patient_id' : request.POST['patient_id']
	}
	context.update(userContext)
	return render(request, 'generateBills.html',context) 

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

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def onSubmitOfExistingPatientsAppointmentBooking(request):
	user = request.user
	shsUser = SHSUser.objects.filter(user = request.user)
	patient = Patient.objects.filter(user_id=shsUser[0])
	saveAppointmentDetails(request, patient[0])
	messages.success(request,"Appointment booked")
	return redirect(to=reverse('home'))


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
            messages.error(request, "User already exists please login to book")
            return redirect('/accounts/login/')

        print("user about to be saved")
        user = User(password=(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))),
                    last_login = loginDate,
                    is_superuser = 0,
                    username= email,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    is_staff = 0,
                    is_active=0,
                    date_joined = loginDate
        )
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
        patient = Patient(
            update_user = shsUser,
            user_id = shsUser,
            patient_insurance_member_id = request.POST['insuranceid'],
            emergency_contact_firstname = ecFirstName,
            emergency_contact_lastname  = ecLastName,
            emergency_contact_phone_number = ecPhoneNumber,
            emergency_contact_email = ecEmailInfo,
            patient_insurance_provider_id=insuranceProviderObj[0],
            blood_type=blood_type,
            address = address,
            city = city,
            state= state,
            zipCode = zipCode,
            phone_number= phone_number,
            allergies=allergies,
            medicationFollowed=medicationFollowed,
            preExistingMedicalConditions=preExistingMedicalConditions,
            anyOtherMedicalDetails=anyOtherMedicalDetails
        )
        patient.save()
        saveAppointmentDetails(request, patient)
        current_site = get_current_site(request)
        sendActivationEmail(user, current_site, email)
        messages.success(request,"Appointment request sent")

        return redirect(to=reverse('home'))


@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def appointmentApprovedMail(request):
	booking_id = request.POST['booking_id']
	updateContext = getRoleBasedMenus(request.user.id)
	record = Doctor_availability_booked.objects.get(booking_id=booking_id)
	record.status = "approved"
	record.save()
	print(record.patient_id.user_id.user.email)
	print(record.status)
	print(record.appointment_date)
	print(record.doctor_id.user_id.user.first_name)
	subject = 'Appointment Confirmation'
	body ="Dear "+record.patient_id.user_id.user.first_name + ",\n"+"\nYour appointment has been confirmed! Below are your appointment details for your reference"+"\n\nAppointment Date:\t"+str(record.appointment_date)+"\nAppointment Timings:\t"+str(record.appointment_start_time)+" - "+str(record.appointment_end_time)+"\nDoctor Name\t:"+record.doctor_id.user_id.user.first_name+"\n\nThank you,\nSHS Healthcare"
	patient_email = record.patient_id.user_id.user.email
	send_mail(
		subject,
		body,
		'shsgrp1@gmail.com',
		[patient_email],
		fail_silently=False
	)
	messages.success(request,"Status updated successfuly")
	return appointmentApproval(request)
	
@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def appointmentDeniedMail(request):
	booking_id = request.POST['booking_id']
	updateContext = getRoleBasedMenus(request.user.id)
	record = Doctor_availability_booked.objects.get(booking_id=booking_id)
	record.status ="denied"
	record.save()
	subject ='Appointment Denied'
	body = "Dear "+record.patient_id.user_id.user.first_name + ",\n"+"\nYour appointment has been denied due to doctor unavailability. Please book your appointment again. We apologize for the inconvenience.\n\nThank you,\nSHS Healthcare"
	patient_email = record.patient_id.user_id.user.email
	send_mail(
		subject,
		body,
		'shsgrp1@gmail.com',
		[patient_email],
		fail_silently=False
	)
	messages.success(request,"Status updated successfuly")
	return appointmentApproval(request)

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

@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def appointmentApproval(request):
	userId = request.user
	worklistDetails = Doctor_availability_booked.objects.filter(status="pending")
	appointmentsTable = SimpleTable(worklistDetails)
	template = loader.get_template('simple_list.html')
	userContext = getRoleBasedMenus(userId)
	context = {
		'appointmentsTable' : appointmentsTable,
	}
	context.update(userContext)
	return render(request, 'simple_list.html', context)

class TableView(tables.SingleTableView):
	table_class = SimpleTable
	queryset = Doctor_availability_booked.objects.filter(status="pending")
	template_name = "simple_list.html"

class DoctorViewTable(tables.SingleTableView):
	table_class = DoctorView
	queryset = Doctor_availability_booked.objects.filter()
	template_name = "simple_list.html"

@login_required
@twoFARequired()
@is_doctor('home', "Oops, can't go there.")
def doctorWorklist(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	docId = doctor.doctor_id
	worklistDetails = Doctor_availability_booked.objects.filter(doctor_id=docId).filter(status='approved').order_by('appointment_date')
	filter = DoctorViewFilter(request.POST, queryset=worklistDetails)
	worklistDetails = filter.qs
	doctorsTable = DoctorView(worklistDetails)
	template = loader.get_template('doctorWorklist.html')
	userContext = getRoleBasedMenus(userId.id)
	print(userContext)
	context = {
		'filter' : filter,
		'doctorsTable' : doctorsTable,
	}
	context.update(userContext)
	return render(request, 'doctorWorklist.html', context)

@login_required
@twoFARequired()
@is_hospital_staff('home', "Oops, can't go there.")
def patientsViewWithFilter(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)
	patientDetails = (Patient.objects.all())
	filter = PatientViewFilter(request.POST, queryset=patientDetails)
	patientDetails = filter.qs
	patientsTable = PatientsView(patientDetails)
	template = loader.get_template('patientGrid.html')
	userContext = getRoleBasedMenus(userId.id)
	print(userContext)
	context = {
		'filter' : filter,
		'patientsTable' : patientsTable,
	}
	context.update(userContext)
	return render(request, 'patientGrid.html', context)


@login_required
@twoFARequired()
def medicalRecords(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	shsUser = SHSUser.objects.get(user = userId)
	patientId = ''
	isPatient = False
	isHospitalStaff = False
	if role == 'patient':
		patient = Patient.objects.get(user_id=shsUser)
		patientId = patient.patient_id
		isPatient = True
	elif role == 'doctor':
		patientId = request.POST['patient_id']
	elif role == 'hospitalstaff':
		patientId = request.POST['patient_id']
		isHospitalStaff = True

	userContext = getRoleBasedMenus(userId)
	patientDetails = PatientDetails(Patient.objects.filter(patient_id=patientId)).as_values()
	appointmentsTable = Appointments(Doctor_availability_booked.objects.filter(patient_id=patientId).order_by('appointment_date'))
	diagnosesTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='D').order_by('records_id'))
	labTestReportsTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='L').order_by('records_id'))
	prescriptionsTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='P').order_by('records_id'))
	paymentsTable = PaymentsTable(Payments.objects.filter(patient_id=patientId).order_by('patient_id'))
	
	template = loader.get_template('medicalRecords.html')
	context = {
		'patient_name' : patientDetails,
		'patient_id' : patientId,
		'appointmentsTable' : appointmentsTable,
		'diagnosesTable' : diagnosesTable,
		'labTestReportsTable' : labTestReportsTable,
		'prescriptionsTable' : prescriptionsTable,
		'paymentsTable': paymentsTable,
		'isHospitalStaff' : isHospitalStaff,
		'isPatient' : isPatient,
	}
	context.update(userContext)
	return HttpResponse(template.render(context, request))

@login_required
@twoFARequired()
def viewRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	isDoctor = False
	isPatient = False
	if(role == 'doctor' or role == 'labstaff'):
		isDoctor = True
	elif(role == 'patient'):
		isPatient = True
	recordId = request.POST['record_id']
	record = Records.objects.filter(records_id=recordId).values('records_id', 'document', 'document_type')
	recordString = record[0]['document']
	userContext = getRoleBasedMenus(userId)
	template = loader.get_template('record.html')
	context = {
		'record_id' : recordId,
		'isDoctor': isDoctor,
		'isPatient' : isPatient,
		'document_type' : record[0]['document_type'],
		'document' : recordString,
		'patient_id' : request.POST['patient_id'],
	}
	context.update(userContext)
	return HttpResponse(template.render(context, request))

#def insuranceLoginRecords(request):
#	insuranceRequests = Claim_Request.objects.all()
#	filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
#	insuranceRequests = filter.qs
#	return render(request, 'insuranceApproverGrid.html', {'filter': filter, 'insuranceRequests': insuranceRequests})

@login_required
@twoFARequired()
@is_doc_or_labstaff('home', "Oops, can't go there.")
def editRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	action_taken = request.POST['action_taken']
	document_type = request.POST['document_type']
	record_id = request.POST['record_id']
	if (role == 'doctor' and (document_type == 'D' or document_type == 'P')):
		if action_taken == 'edit':
			
			document = request.POST['document']
			patient_id = request.POST['patient_id']
			context = {
				'user_id' : userId,
				'record_id' : record_id,
				'document' : document,
				'document_type' : document_type,
				'patient_id' : patient_id,
			}
			userContext = getRoleBasedMenus(userId)
			context.update(userContext)
			template = loader.get_template('editRecords.html')
			return HttpResponse(template.render(context, request))
		elif action_taken == 'delete':
			Records.objects.filter(records_id=record_id).delete()
			return medicalRecords(request)
	elif (role == 'labstaff' and document_type == 'L'):
		if action_taken == 'edit':
			document = request.POST['document']
			patient_id = request.POST['patient_id']
			context = {
				'user_id' : userId,
				'record_id' : record_id,
				'document' : document,
				'document_type' : document_type,
				'patient_id' : patient_id,
			}
			userContext = getRoleBasedMenus(userId)
			context.update(userContext)
			template = loader.get_template('editRecords.html')
			return HttpResponse(template.render(context, request))
		elif action_taken == 'delete':
			record_id = request.POST['record_id']
			Records.objects.filter(records_id=record_id).delete()
			return labstaffWorklist(request)

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there.")
def downloadRecord(request):
	userId = request.user
	patientId = request.POST['patient_id']
	template = loader.get_template('downloadRecord.html')
	recordId = request.POST['record_id']
	record = Records.objects.filter(records_id=recordId).values('records_id', 'document', 'document_type')
	recordString = record[0]['document']
	patient = Patient.objects.get(patient_id=patientId)
	patient_name = patient.user_id.user.first_name
	patient_address = patient.address
	patient_zipcode = patient.zipCode
	patient_DOB = patient.patient_dob
	patientBloodGroup = patient.blood_type
	patientPhoneNumber = patient.phone_number
	patientEmail = patient.user_id.user.email
	patientAllergies = patient.allergies
	patientMedicationFollowed = patient.medicationFollowed
	patientPreExistingMedicalConditions = patient.preExistingMedicalConditions
	patientAnyOtherMedicalDetails = patient.anyOtherMedicalDetails
	userContext = getRoleBasedMenus(userId)
	context = {
		'record_id' : recordId,
		'document_type' : record[0]['document_type'],
		'document' : recordString,
		'patient_id' : request.POST['patient_id'],
		'patient_name' : patient_name,
		'patient_address': patient_address+" "+patient_zipcode,
		'patient_zipcode': patient_zipcode,
		'patient_DOB': patient_DOB,
		'patientBloodGroup' : patientBloodGroup,
		'patientPhoneNumber' : patientPhoneNumber,
		'patientEmail' : patientEmail,
		'patientAllergies' : patientAllergies,
		'patientMedicationFollowed' : patientMedicationFollowed,
		'patientPreExistingMedicalConditions' : patientPreExistingMedicalConditions,
		'patientAnyOtherMedicalDetails' : patientAnyOtherMedicalDetails,
	}
	context.update(userContext)
	document = template.render(context)
	result = BytesIO()
	downloadFile = pisa.pisaDocument(BytesIO(document.encode("ISO-8859-1")), result)
	if not downloadFile.err:
		downloadDocument =  HttpResponse(result.getvalue(), content_type='application/pdf')
		return HttpResponse(downloadDocument, content_type='application/pdf')



@login_required
@twoFARequired()
@is_doc_or_labstaff('home', "Oops, can't go there.")
def saveRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	record_id = request.POST['record_id']
	document = request.POST['editeddocument']
	patient_id = request.POST['patient_id']
	Records.objects.filter(records_id=record_id).update(document=document, last_modified_date=timezone.now())
	return render(request, 'home.html')

@login_required
@twoFARequired()
@is_doctor('home', "Oops, can't go there.")
def viewAppointmentDoctor(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	if request.method == 'POST':
		patientId = request.POST['patient_id']
		appointment_id = request.POST['appointment_id']
	userContext = getRoleBasedMenus(userId)
	appointment_id = request.POST['appointment_id']
	patient = Patient.objects.get(patient_id=patientId)
	patient_name = patient.user_id.user.first_name
	patient_address = patient.address
	patient_zipcode = patient.zipCode
	patient_DOB = patient.patient_dob
	patientBloodGroup = patient.blood_type
	patientPhoneNumber = patient.phone_number
	patientEmail = patient.user_id.user.email
	patientAllergies = patient.allergies
	patientMedicationFollowed = patient.medicationFollowed
	patientPreExistingMedicalConditions = patient.preExistingMedicalConditions
	patientAnyOtherMedicalDetails = patient.anyOtherMedicalDetails
	template = loader.get_template('appointmentViewDoctor.html')
	context={
		'patient_id' : patientId,
		'appointment_id' : appointment_id,
		'patient_name' : patient_name,
		'patient_address': patient_address+" "+patient_zipcode,
		'patient_zipcode': patient_zipcode,
		'patient_DOB': patient_DOB,
		'patientBloodGroup' : patientBloodGroup,
		'patientPhoneNumber' : patientPhoneNumber,
		'patientEmail' : patientEmail,
		'patientAllergies' : patientAllergies,
		'patientMedicationFollowed' : patientMedicationFollowed,
		'patientPreExistingMedicalConditions' : patientPreExistingMedicalConditions,
		'patientAnyOtherMedicalDetails' : patientAnyOtherMedicalDetails,
		'user_id' : userId,
	}
	userContext = getRoleBasedMenus(userId)
	context.update(userContext)
	return HttpResponse(template.render(context,request))

@login_required
@twoFARequired()
@is_doctor('home', "Oops, can't go there.")
def createDiagnosis(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	patient_id = request.POST['patient_id']
	diagnosis = request.POST['diagnosis_string']
	patient=Patient.objects.get(patient_id=patient_id)
	diagnosisRecord = Records(document=diagnosis, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='D')
	diagnosisRecord.save()
	return viewAppointmentDoctor(request)

@login_required
@twoFARequired()
@is_doctor('home', "Oops, can't go there.")
def createPrescription(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	patient_id = request.POST['patient_id']
	prescription = request.POST['prescription_string']
	patient=Patient.objects.get(patient_id=patient_id)
	prescriptionRecord = Records(document=prescription, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='P')
	prescriptionRecord.save()
	return viewAppointmentDoctor(request)

@login_required
@twoFARequired()
@is_doctor('home', "Oops, can't go there.")
def recommendLabtest(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	patient_id = request.POST['patient_id']
	labtest_recommendation = request.POST['labtest_recommendation']
	patient=Patient.objects.get(patient_id=patient_id)
	labTest = Lab_Test(recommended_test=labtest_recommendation, patient=patient,doctor=doctor,recommended_date=timezone.now())
	labTest.save()
	return viewAppointmentDoctor(request)

@login_required
@twoFARequired()
@is_lab_staff('home', "Oops, can't go there.")
def labtestRequests(request):
	userId = request.user
	userContext = getRoleBasedMenus(userId)
	lab_test_requests = LabTestRequests(Lab_Test.objects.filter(status='Pending').order_by('recommended_date'))
	context = {
		'lab_test_requests' : lab_test_requests,
	}
	context.update(userContext)
	template = loader.get_template('labTestRequests.html')
	return HttpResponse(template.render(context,request))

@login_required
@twoFARequired()
@is_lab_staff('home', "Oops, can't go there.")
def labtestAction(request):
	lab_test_id = request.POST['lab_test_id']
	action_taken = request.POST['action_taken']
	record = Lab_Test.objects.get(lab_test_id = lab_test_id)
	if(action_taken == 'Approve'):
		Lab_Test.objects.filter(lab_test_id=lab_test_id).update(status='Approved', action_taken_date=timezone.now())
		subject ='Lab Test Approved '
		body = "Dear "+record.patient.user_id.user.first_name + ",\n"+"\nYour "+record.recommended_test+" test that was recommended by"+record.doctor.user_id.user.first_name+" has been approved. Please visit our lab to get your test done.\n\nThank you,\nSHS Healthcare"
		patient_email = record.patient.user_id.user.email
		send_mail(
		subject,
		body,
		'shsgrp1@gmail.com',
		[patient_email],
		fail_silently=False
	    )
	elif(action_taken == 'Deny'):
		Lab_Test.objects.filter(lab_test_id=lab_test_id).update(status='Denied', action_taken_date=timezone.now())
		subject ='Lab Test Denied '
		body = "Dear "+record.patient.user_id.user.first_name + ",\n"+"\nYour "+record.recommended_test+" test that was recommended by"+record.doctor.user_id.user.first_name+" has been denied.\n\nThank you,\nSHS Healthcare"
		patient_email = record.patient.user_id.user.email
		send_mail(
		subject,
		body,
		'shsgrp1@gmail.com',
		[patient_email],
		fail_silently=False
	    )
	return labtestRequests(request)

@login_required
@twoFARequired()
@is_lab_staff('home', "Oops, can't go there.")
def labstaffWorklist(request):
	userId = request.user
	labTestQuery = Lab_Test.objects.filter(status__in=['Approved','Completed']).order_by('action_taken_date')
	filter = LabStaffViewFilter(request.POST, queryset=labTestQuery)
	labTestQuery = filter.qs
	labStaffTable = LabStaffView(labTestQuery)
	template = loader.get_template('labstaffWorklist.html')
	context = {
		'filter' : filter,
		'labStaffTable' : labStaffTable,
	}
	userContext = getRoleBasedMenus(userId)
	context.update(userContext)
	return render(request, 'labstaffWorklist.html', context)

@login_required
@twoFARequired()
@is_lab_staff('home', "Oops, can't go there.")
def createLabtestReport(request):
		labtest_report_string = request.POST['labtest_report_string']
		lab_test_id = request.POST['lab_test_id']
		labTest = Lab_Test.objects.get(lab_test_id=lab_test_id)
		patient = labTest.patient
		doctor = labTest.doctor
		labTestReportRecord = Records(document=labtest_report_string,patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='L')
		labTestReportRecord.save()
		labTestRecord = Records.objects.get(records_id=labTestReportRecord.records_id)
		Lab_Test.objects.filter(lab_test_id=lab_test_id).update(record=labTestRecord,status='Completed')
		return labstaffWorklist(request)

@login_required
@twoFARequired()
@is_insurance_staff('home', "Oops, can't go there.")
def insuranceApprovedMail(request):
	#how to fetch the claim_id
	claim_id = request.POST['claim_id']
	updateContext = getRoleBasedMenus(request.user.id)
	record = Claim_Request.objects.get(claim_id=claim_id)
	record.claim_status = "approved"
	record.save()
	try:
		url = settings.BLOCKCHAINURL + "/api/setClaimStatus"
		data = {'id': claim_id, 'claim_status':record.claim_status}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(url, data=json.dumps(data), headers=headers)
		if r.status_code == 200:		
			print("worked")
		else:
			print("not worked")
	except Exception:
		print("An exception occurred")
    #print(record.appointment_date)
    #print(record.doctor_id.user_id.user.first_name)
	subject = 'Insurance Claim Confirmation'
	body ="Dear ,\n"+"\nYour insurance claim#"+str(record.claim_id)+" has been approved! \n\nThank you,\nSHS Healthcare"
	patient_email = record.patient_id.user_id.user.email
	send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
        fail_silently=False
    )
	messages.success(request,"Status updated successfuly")
	return insuranceLoginRecords(request)
    
@login_required
@twoFARequired()
@is_insurance_staff('home', "Oops, can't go there.")
def insuranceLoginRecords(request):
	userId = request.user
	shsUser = SHSUser.objects.get(user = userId)	
	worklistDetails = Claim_Request.objects.filter(claim_status='pending')
	claimRequestTable = ClaimRequestTable(worklistDetails)
	template = loader.get_template('insuranceLoginRecords.html')
	userContext = getRoleBasedMenus(userId.id)
	print(userContext)
	context = {
		'claimRequestTable' : claimRequestTable,
	}
	context.update(userContext)
	return render(request, 'insuranceLoginRecords.html', context)

class InsuranceLoginRecords(tables.SingleTableView):
	table_class = ClaimRequestTable
	queryset = insuranceRequests = Claim_Request.objects.filter(claim_status='pending')
	#filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
	#insuranceRequests = filter.qs
	template_name = "simple_list.html"

@login_required
@twoFARequired()
@is_insurance_staff('home', "Oops, can't go there.")
def insuranceDeniedMail(request):
	claim_id = request.POST['claim_id']
	print("claim_id ",claim_id)
	updateContext = getRoleBasedMenus(request.user.id)
	record = Claim_Request.objects.get(claim_id=claim_id)
	record.claim_status = "denied"
	record.save()
	subject ='Claim Denied'
	body = "Your insurance claim#"+str(record.claim_id)+" has been denied.\n\nThank you,\nSHS Healthcare"
	patient_email = record.patient_id.user_id.user.email
	send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
        fail_silently=False
    )
	messages.success(request, "Status updated successfuly")
	return insuranceLoginRecords(request)

class ClaimTableView(tables.SingleTableView):
    table_class = ClaimTable
    queryset = Claim_Request.objects.all()
    template_name = "claimTable.html"
    
@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def patientInsurance(request):
    #patient_id = request.user.patient_id
	user = request.user
	shs_user_id = SHSUser.objects.get(user = user)
	patient_id = Patient.objects.get(user_id =shs_user_id )
	patientInsuranceMemberId = patient_id.patient_insurance_member_id
	patientInsuranceProvider = InsuranceProvider.objects.get(provider_id=patient_id.patient_insurance_provider_id.provider_id).provider_name
	paymentsTable = PaymentTable(Payments.objects.filter(patient_id=patient_id).filter(is_claimed = False).order_by('payment_update_date'))
	claimsTable = ClaimTable(Claim_Request.objects.filter(patient_id=patient_id).order_by('claim_raised_date'))
	template = loader.get_template('insurancePortal.html')
	insuranceProviders = InsuranceProvider.objects.all().values_list('provider_name', flat=True)
	insuranceProviders = list(insuranceProviders)
	context1 = getRoleBasedMenus(request.user.id)
	context = {
        'paymentsTable' : paymentsTable,
        'claimsTable' : claimsTable,
        'patient_id' : patient_id,
		'patient_insurance_member_id' : patientInsuranceMemberId,
		'insurance_providers' : insuranceProviders,
		'patient_insurance_provider_name' : patientInsuranceProvider,
    }
	context.update(context1)
	return HttpResponse(template.render(context, request))

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def saveInsurInfo(request):
	user = request.user
	shsUser = SHSUser.objects.get(user=user)
	patient = Patient.objects.get(user_id=shsUser)
	patientId = patient.patient_id
	insurName = request.POST.get('insurName')
	insurancePv = InsuranceProvider.objects.get(provider_name=insurName)
	patientMemID = request.POST.get('patientInsurID')
	Patient.objects.filter(patient_id=patientId).update(patient_insurance_provider_id = insurancePv, patient_insurance_member_id = patientMemID )
	return patientInsurance(request)

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def fileClaim(request):
    user = request.user
    shs_user_id = SHSUser.objects.get(user = user)
    patient = Patient.objects.get(user_id =shs_user_id)
    patient_id = patient.patient_id
    claim_raised_date = datetime.now()
    claim_update_date = datetime.now()
    payment_ID = request.POST['payment_id']
    if Claim_Request.objects.filter(payment_id = payment_ID).count() == 0:
        Claim_Request.objects.create(patient_id_id = patient_id, payment_id_id = payment_ID, claim_status = 'pending', claim_raised_date = claim_raised_date, claim_update_date=claim_update_date)
        Payments.objects.filter(payment_id=payment_ID).update(is_claimed = True)
        claim_created = Claim_Request.objects.get(payment_id = payment_ID)
        try:
            url = settings.BLOCKCHAINURL + "/api/addClaim"
            data = {'claim_id': claim_created.claim_id, 'patient_id': claim_created.patient_id.patient_id, 'insurance_id': claim_created.patient_id.patient_insurance_provider_id.provider_id, 'amount': claim_created.payment_id.overall_payment, 'bill_id': claim_created.payment_id.payment_id, 'status':claim_created.claim_status}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            if r.status_code == 200:
                print("worked")
        except Exception:
            print("An exception occurred")
        return patientInsurance(request)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        shs_user = SHSUser.objects.select_related().filter(user = user.id)
        shs_user.email_confirmed = True
        user.save()
        return redirect('password_reset')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
@twoFARequired()
@is_insurance_staff('home', "Oops, can't go there")
def addInsuranceProvider (request):
	providerName = request.POST['insuranceProvider']
	insurance = InsuranceProvider(provider_name=providerName)
	insurance.save()
	return insuranceLoginRecords(request)

@login_required
@twoFARequired()
@is_patient('home', "Oops, can't go there")
def view_patient(request):
    shs_user = SHSUser.objects.select_related().filter(user = request.user.id)[0]
    patient = Patient.objects.select_related().filter(user_id = shs_user)[0]

    context = {
        'user': request.user,
        'patient': patient
    }

    RoleContext = getRoleBasedMenus(request.user.id)
    template = loader.get_template('viewPatient.html')
    context.update(RoleContext)
    return HttpResponse(template.render(context, request))

@login_required
@twoFARequired()
@is_patient('home',  "Oops, can't go there.")
def updatePatient(request):
    user = User.objects.filter(id=request.user.id)[0]
    shs_user = SHSUser.objects.select_related().filter(user = request.user.id)[0]
    patient = Patient.objects.select_related().filter(user_id = shs_user)[0]
    user.first_name = request.POST.get("firstName", "")
    user.last_name = request.POST.get("lastName", "")
    patient.phone_number = request.POST.get("contact", "")
    patient.patient_dob = parse_date(request.POST.get('dateOfBirth', '1945-08-15'))
    patient.blood_type = request.POST.get('blood_type', "A+")
    patient.address = request.POST.get("address", "")
    patient.city = request.POST.get('city', "")
    patient.state = request.POST.get("state", "")
    patient.zipCode = request.POST.get("pincode", "")
    patient.emergency_contact_firstname = request.POST.get("gfirstName", "")
    patient.emergency_contact_lastname = request.POST.get("glastName", "")
    patient.emergency_contact_phone_number = request.POST.get("econtact", "")
    patient.emergency_contact_email = request.POST.get("eemail", "")
    patient.allergies = request.POST.get("allergies", "")
    patient.medicationFollowed = request.POST.get("medications", "")
    patient.preExistingMedicalConditions = request.POST.get("premedical","")
    patient.anyOtherMedicalDetails = request.POST.get("othermedical", "")
    patient.gender = request.POST.get('gender', "MALE")
    patient.emergency_contact_gender = request.POST.get('egender', "MALE")

    user.save()
    patient.save()
    messages.success(request, "Patient details updated")
    return redirect(to=reverse('view_patient'))

@login_required
@twoFARequired()
@is_patient('home',  "Oops, can't go there.")
def viewBlockChainInfo(request):
    claim_id = request.POST['claim_id']
    print(claim_id)
    action_taken = request.POST['action_taken']
    print(action_taken)
    if(action_taken == "Claim"):
        resp=viewBlockChainClaims(claim_id)
    elif(action_taken == "BlockchainRecord"):
        resp=viewBlockChainClaimStatus(claim_id)
    return HttpResponse("<html> <body><h1>Blockchain Information</h1>"+resp+"</body></html>")


def viewBlockChainClaims(claim_id):
	data = ''
	conn = http.client.HTTPSConnection("shsblockchain.pagekite.me")
	headers = {
    'cache-control': "no-cache",
    #'postman-token': "1a7651c4-8fd2-ec56-c84d-26eee9007d7f"
    }
	conn.request("GET", "/api/getClaimHistory/"+claim_id, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	return str(data)

def viewBlockChainClaimStatus(claim_id):
	# print("Inside block chain status")
	# data=''
	# try:
	# 	url = settings.BLOCKCHAINURL + "/api/getClaim/"+claim_id
	# 	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	# 	data = requests.get(url).json
	# 	print(data)
	# except Exception:
	# 	print("An exception occurred")
	# return data 
	print("Inside block chain status")
	data = ''
	conn = http.client.HTTPSConnection("shsblockchain.pagekite.me")
	headers = {
    'cache-control': "no-cache",
    #'postman-token': "1a7651c4-8fd2-ec56-c84d-26eee9007d7f"
    }
	conn.request("GET", "/api/getClaim/"+claim_id, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	return str(data)
