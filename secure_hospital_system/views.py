# from asyncio.windows_events import NULL
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
	slots = ["8-9", "9-10", "10-11", "11-12"]
	if doctorid != NULL:
		doctors = Doctor.objects.filter(doctor_id = doctorid)
	else:
		doctors = Doctor.objects.all()
	context = {
		'doctors' : doctors,
		'slots' : slots,
	}
	return render(request,"BOOKAPPT.html",context)

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
		patient_id= request.POST['patient_id']
		#user_id = request.POST['user_id]
		#patient_id= 13 

		patientDetails = Patient.objects.filter(patient_id=patient_id)
		return patientDetails

@csrf_exempt
def newBillGenerated(request):
	if request.method == 'POST':
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
			payment_status = 'PENDING', payment_update_date = date.today())
		payments.save()
	#return render(request,"medical_records.html")	
	response = redirect('/medical_records/'+patient_id)
	return response

def generateBills(request):
	return render(request, 'generateBills.html',{'patient_id':request.GET['patient_id']}) 

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

def doctor_worklist(request):
	doc_id=1
	if request.method == "POST":
		doc_id = request.POST['docid']
	doctorsTable = DoctorView(Doctor_availability_booked.objects.filter(doctor_id=doc_id).filter(status='approved').order_by('appointment_date'))
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
		#recordsTable = (Records.objects.exclude(LabReport__isnull=True))
		recordsTable = (Records.objects.filter(document_type="L"))
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


@csrf_exempt
def medical_records(request):

	patient_id = ''
	user_id = ''
	if request.method == 'POST':
		patient_id = request.POST['patient_id']
		user_id = request.POST['user_id']
	elif request.method == 'GET':
		user_id='1'
		patient_id='1'

	#context1 = getRoleBasedMenus(user_id)

	patientDetails = PatientDetails(Patient.objects.filter(patient_id=patient_id)).as_values()
	appointmentsTable = Appointments(Doctor_availability_booked.objects.filter(patient_id=patient_id).order_by('appointment_date'))
	diagnosesTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='D').order_by('records_id'))
	labTestReportsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='L').order_by('records_id'))
	prescriptionsTable = RecordsTable(Records.objects.filter(patient_id=patient_id).filter(document_type='P').order_by('records_id'))
	paymentsList = Payments.objects.filter(patient_id=patient_id).order_by('patient_id')
	
	template = loader.get_template('medical_records.html')
	context = {
		'patient_name' : patientDetails,
		'appointmentsTable' : appointmentsTable,
		'diagnosesTable' : diagnosesTable,
		'labTestReportsTable' : labTestReportsTable,
		'prescriptionsTable' : prescriptionsTable,
		'paymentsList': paymentsList,
	}
	#context.update(context1)
	return HttpResponse(template.render(context, request))

@csrf_exempt
def view_record(request):
	record_id = request.POST['record_id']
	record = Records.objects.filter(records_id=record_id).values('records_id', 'document', 'document_type')
	recordString = record[0]['document']
	#user_id = request.POST['user_id']
	user_id = '1'
	template = loader.get_template('record.html')
	context = {
		'record_id' : record_id,
		'document_type' : record[0]['document_type'],
		'document' : recordString,
		'editAccess' : True,
		'patient_id' : request.POST['patient_id']
	}
	context1 = getRoleBasedMenus(user_id)
	context.update(context1)
	return HttpResponse(template.render(context, request))

#def insuranceLoginRecords(request):
#	insuranceRequests = Claim_Request.objects.all()
#	filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
#	insuranceRequests = filter.qs
#	return render(request, 'insuranceApproverGrid.html', {'filter': filter, 'insuranceRequests': insuranceRequests})

def view_patient(request):
	context = getRoleBasedMenus(request.user.id)
	template = loader.get_template('viewPatient.html')
	return HttpResponse(template.render(context, request))

@csrf_exempt
def edit_record(request):
	user_id = '1'
	#user_id = request.POST['user_id']
	record_id = request.POST['record_id']
	document = request.POST['document']
	document_type = request.POST['document_type']
	patient_id = request.POST['patient_id']
	context = {
		'user_id' : 1,
		'record_id' : record_id,
		'document' : document,
		'document_type' : document_type,
		'patient_id' : patient_id,
	}
	context1 = getRoleBasedMenus(user_id)
	context.update(context1)
	template = loader.get_template('editRecords.html')
	return HttpResponse(template.render(context, request))

@csrf_exempt
def save_record(request):
	record_id = request.POST['record_id']
	document = request.POST['editeddocument']
	patient_id = request.POST['patient_id']
	Records.objects.filter(records_id=record_id).update(document=document, last_updated_date=timezone.now())
	return medical_records(request)

@csrf_exempt
def view_appointment_doctor(request):
	#user_id = request.POST['user_id']
	user_id = '1'
	patient_id = request.POST['patient_id']
	appointment_id = request.POST['appointment_id']
	patient_address = Patient.objects.filter(patient_id=patient_id).order_by('patient_id').values('address')
	patient_address = patient_address[0]['address']
	patient_zipcode = Patient.objects.filter(patient_id=patient_id).order_by('patient_id').values('zipCode')
	patient_zipcode = patient_zipcode[0]['zipCode']
	patient_DOB = Patient.objects.filter(patient_id=patient_id).order_by('patient_id').values('patient_dob')
	patient_DOB = patient_DOB[0]['patient_dob']
	patientTable = Patient.objects.filter(patient_id=patient_id).order_by('patient_id')
	patientJson = serializers.serialize("json", patientTable)
	template = loader.get_template('appointment_view_doctor.html')
	context={
		'patient_id' : patient_id,
		'patient_address': patient_address,
		'patient_zipcode': patient_zipcode,
		'patient_DOB': patient_DOB,
		'user_id' : user_id
	}
	#context1 = getRoleBasedMenus(user_id)
	#context.update(context1)
	return HttpResponse(template.render(context,request))

@csrf_exempt
def create_diagnosis(request):
	patient_id = request.POST['patient_id']
	diagnosis = request.POST['diagnosis_string']
	user_id = request.POST['user_id']
	##write code to save the diagnosis to record table
	patient=Patient.objects.get(patient_id=patient_id)
	doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
	diagnosisRecord = Records(document=diagnosis, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='D')
	diagnosisRecord.save()
	return view_appointment_doctor(request)


@csrf_exempt
def create_prescription(request):
	patient_id = request.POST['patient_id']
	prescription = request.POST['prescription_string']
	user_id = request.POST['user_id']
	patient=Patient.objects.get(patient_id=patient_id)
	doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
	prescriptionRecord = Records(document=prescription, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='P')
	prescriptionRecord.save()
	return view_appointment_doctor(request)    

@csrf_exempt
def recommend_labtest(request):
	patient_id = request.POST['patient_id']
	labtest_recommendation = request.POST['labtest_recommendation']
	user_id = request.POST['user_id']
	patient=Patient.objects.get(patient_id=patient_id)
	doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
	labTest = Lab_Test(recommended_test=labtest_recommendation, patient=patient,doctor=doctor,recommended_date=timezone.now())
	labTest.save()
	return view_appointment_doctor(request)

@csrf_exempt
def labtest_requests(request):
	lab_test_requests = LabTestRequests(Lab_Test.objects.filter(status='Pending').order_by('recommended_date'))
	context = {
		'lab_test_requests' : lab_test_requests,
	}
	template = loader.get_template('lab_test_requests.html')
	return HttpResponse(template.render(context,request))

@csrf_exempt
def labtest_action(request):
	lab_test_id = request.POST['lab_test_id']
	post_data = dict(request.POST.lists())
#    Records.objects.filter(records_id=record_id).update(document=document, last_updated_date=timezone.now())
	action_taken = request.POST['action_taken']
	if(action_taken == 'Approve'):
		Lab_Test.objects.filter(lab_test_id=lab_test_id).update(status='Approved', action_taken_date=timezone.now())
	elif(action_taken == 'Deny'):
		Lab_Test.objects.filter(lab_test_request_id=lab_test_request_id).update(status='Denied', action_taken_date=timezone.now())
	return labtest_requests(request)

@csrf_exempt
def labstaff_worklist(request):
	labStaffTable = LabStaffView(Lab_Test.objects.filter(status='Approved').order_by('action_taken_date'))
	template = loader.get_template('labstaff_worklist.html')
	context = {
		'labStaffTable' : labStaffTable,
	}
	return HttpResponse(template.render(context,request))

@csrf_exempt
def create_labtest_report(request):
	labtest_report_string = request.POST['labtest_report_string']
	lab_test_id = request.POST['lab_test_id']
	user_id = request.POST['user_id']
	labTest = Lab_Test.objects.get(lab_test_id=lab_test_id)
	patient = labTest.patient
	doctor = labTest.doctor
	labTestReportRecord = Records(document=labtest_report_string,patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='L')
	labTestReportRecord.save()
	labTestRecord = Records.objects.get(records_id=labTestReportRecord.records_id)
	Lab_Test.objects.filter(lab_test_id=lab_test_id).update(record=labTestRecord,status='Completed')
	return labstaff_worklist(request)

@csrf_exempt
def insuranceApprovedMail(request):
	#how to fetch the claim_id
    record = Claim_Request.objects.get(claim_id=1)
    record.claim_status = "approved"
    record.save()
    print(record.patient_id.user_id.user.email)
    print(record.claim_status)
    #print(record.appointment_date)
    #print(record.doctor_id.user_id.user.first_name)
    subject = 'Appointment Confirmation'
    body ="Dear ,\n"+"\nYour insurance has been confirmed! \n\nThank you,\nSHS Healthcare"
    patient_email = record.patient_id.user_id.user.email
    send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
        fail_silently=False
    )
    return render(request, 'sentmail.html')
    
class InsuranceLoginRecords(tables.SingleTableView):
	table_class = ClaimRequestTable
	queryset = insuranceRequests = Claim_Request.objects.filter(claim_status='pending')
	#filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
	#insuranceRequests = filter.qs
	template_name = "simple_list.html"

@csrf_exempt
def insuranceDeniedMail(request):
    record = Claim_Request.objects.get(claim_id=1)
    record.claim_status = "denied"
    record.save()
    subject ='Appointment Denied'
    body = "Your insurance claim has been denied due to doctor unavailability. We apologize for the inconvenience.\n\nThank you,\nSHS Healthcare"
    patient_email = record.patient_id.user_id.user.email
    send_mail(
		subject,
        body,
        'shsgrp1@gmail.com',
        [patient_email],
        fail_silently=False
    )
    return render(request, 'sentmail.html')
