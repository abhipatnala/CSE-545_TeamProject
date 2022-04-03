# from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
from django.http import HttpResponse
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

def findPatientDoc(request):
    context1 = getRoleBasedMenus(request.user.id)
    docList = Doctor.objects.all()
    context = {
		'docList':docList
	}
    context.update(context1)
    return render(request, "patientDoc.html", context)

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
	return render(request,'sentmail.html')

def bookAppointment(request):
	doctorid =1
	if request.method == 'POST':
		doctorid = request.POST['docid']
	slots = ["8-9", "9-10", "10-11", "11-12"]
	if doctorid != None:
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
			payment_status = 'pending', payment_update_date = date.today())
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

        return render(request,"test.html")

def appointmentApprovedMail(request,booking_id):
	record = Doctor_availability_booked.objects.get(booking_id=booking_id)
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
	
def appointmentDeniedMail(request,booking_id):
	record = Doctor_availability_booked.objects.get(booking_id=booking_id)
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

@csrf_exempt
@login_required
def doctorWorklist(request):
	userId = request.user
	if getCurrentUserRole(userId) == 'Doctor':
		shsUser = SHSUser.objects.get(user = userId)
		doctor = Doctor.objects.get(user_id=shsUser)
		docId = doctor.doctor_id
		worklistDetails = Doctor_availability_booked.objects.filter(doctor_id=docId).filter(status='approved').order_by('appointment_date')
		filter = DoctorViewFilter(request.POST, queryset=worklistDetails)
		worklistDetails = filter.qs
		doctorsTable = DoctorView(worklistDetails)
		template = loader.get_template('doctorWorklist.html')
		userContext = getRoleBasedMenus(userId)
		context = {
			'filter' : filter,
			'doctorsTable' : doctorsTable,
		}
		context.update(userContext)
		return render(request, 'doctorWorklist.html', context)

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
@login_required
def medicalRecords(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	shsUser = SHSUser.objects.get(user = userId)
	doctor = Doctor.objects.get(user_id=shsUser)
	patientId = ''
	if request.method == 'POST':
		patientId = request.POST['patient_id']
	userContext = getRoleBasedMenus(userId)

	patientDetails = PatientDetails(Patient.objects.filter(patient_id=patientId)).as_values()
	appointmentsTable = Appointments(Doctor_availability_booked.objects.filter(patient_id=patientId).order_by('appointment_date'))
	diagnosesTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='D').order_by('records_id'))
	labTestReportsTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='L').order_by('records_id'))
	prescriptionsTable = RecordsTable(Records.objects.filter(patient_id=patientId).filter(document_type='P').order_by('records_id'))
	paymentsList = Payments.objects.filter(patient_id=patientId).order_by('patient_id')
	
	template = loader.get_template('medicalRecords.html')
	context = {
		'patient_name' : patientDetails,
		'appointmentsTable' : appointmentsTable,
		'diagnosesTable' : diagnosesTable,
		'labTestReportsTable' : labTestReportsTable,
		'prescriptionsTable' : prescriptionsTable,
		'paymentsList': paymentsList,
	}
	context.update(userContext)
	return HttpResponse(template.render(context, request))

@csrf_exempt
@login_required
def viewRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if(role == 'Doctor'):
		isDoctor = True
	else:
		isDoctor = False
	recordId = request.POST['record_id']
	record = Records.objects.filter(records_id=recordId).values('records_id', 'document', 'document_type')
	recordString = record[0]['document']
	userContext = getRoleBasedMenus(userId)
	template = loader.get_template('record.html')
	context = {
		'record_id' : recordId,
		'isDoctor': True,
		'document_type' : record[0]['document_type'],
		'document' : recordString,
		'editAccess' : True,
		'patient_id' : request.POST['patient_id']
	}
	context.update(userContext)
	return HttpResponse(template.render(context, request))

#def insuranceLoginRecords(request):
#	insuranceRequests = Claim_Request.objects.all()
#	filter = ClaimRequestViewFilter(request.GET, queryset=insuranceRequests)
#	insuranceRequests = filter.qs
#	return render(request, 'insuranceApproverGrid.html', {'filter': filter, 'insuranceRequests': insuranceRequests})

@is_patient('home', {'message': "Oops, can't go there."})
def view_patient(request):
	context = getRoleBasedMenus(request.user.id)
	template = loader.get_template('viewPatient.html')
	return HttpResponse(template.render(context, request))

@csrf_exempt
@login_required
def editRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	action_taken = request.POST['action_taken']
	document_type = request.POST['document_type']
	record_id = request.POST['record_id']
	if (role == 'Doctor' and (document_type == 'D' or document_type == 'P')):
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
	elif (role == 'Lab Staff' and document_type == 'L'):
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
			return medicalRecords(request)

@csrf_exempt
@login_required
def saveRecord(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Doctor':
		record_id = request.POST['record_id']
		document = request.POST['editeddocument']
		patient_id = request.POST['patient_id']
		Records.objects.filter(records_id=record_id).update(document=document, last_modified_date=timezone.now())
		return medicalRecords(request)

@csrf_exempt
@login_required
def viewAppointmentDoctor(request):
	#user_id = request.POST['user_id']
	if request.user.is_authenticated:
		userId = request.user
		role = getCurrentUserRole(userId)
		shsUser = SHSUser.objects.get(user = userId)
		doctor = Doctor.objects.get(user_id=shsUser)
		if request.method == 'POST':
			patientId = request.POST['patient_id']
			appointment_id = request.POST['appointment_id']
		userContext = getRoleBasedMenus(userId)
		user_id = '1'
		appointment_id = request.POST['appointment_id']
		patient = Patient.objects.get(patient_id=patientId)
		patient_name = patient.user_id.user.first_name
		patient_address = patient.address
		patient_zipcode = patient.zipCode
		patient_DOB = patient.patient_dob
		template = loader.get_template('appointmentViewDoctor.html')
		context={
			'patient_id' : patientId,
			'appointment_id' : appointment_id,
			'patient_name' : patient_name,
			'patient_address': patient_address,
			'patient_zipcode': patient_zipcode,
			'patient_DOB': patient_DOB,
			'user_id' : user_id
		}
		userContext = getRoleBasedMenus(userId)
		context.update(userContext)
		return HttpResponse(template.render(context,request))

@csrf_exempt
@login_required
def createDiagnosis(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Doctor':
		patient_id = request.POST['patient_id']
		diagnosis = request.POST['diagnosis_string']
		patient=Patient.objects.get(patient_id=patient_id)
		doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
		diagnosisRecord = Records(document=diagnosis, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='D')
		diagnosisRecord.save()
		return viewAppointmentDoctor(request)


@csrf_exempt
@login_required
def createPrescription(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Doctor':
		patient_id = request.POST['patient_id']
		prescription = request.POST['prescription_string']
		patient=Patient.objects.get(patient_id=patient_id)
		doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
		prescriptionRecord = Records(document=prescription, patient=patient,doctor=doctor,created_date=timezone.now(),last_modified_date=timezone.now(),document_type='P')
		prescriptionRecord.save()
		return viewAppointmentDoctor(request)    

@csrf_exempt
@login_required
def recommendLabtest(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Doctor':
		patient_id = request.POST['patient_id']
		labtest_recommendation = request.POST['labtest_recommendation']
		patient=Patient.objects.get(patient_id=patient_id)
		doctor=Doctor.objects.get(doctor_id=1)#change to get using doctor id from request
		
		labTest = Lab_Test(recommended_test=labtest_recommendation, patient=patient,doctor=doctor,recommended_date=timezone.now())
		labTest.save()
		return viewAppointmentDoctor(request)

@csrf_exempt
@login_required
def labtestRequests(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	userContext = getRoleBasedMenus(userId)
	lab_test_requests = LabTestRequests(Lab_Test.objects.filter(status='Pending').order_by('recommended_date'))
	context = {
		'lab_test_requests' : lab_test_requests,
	}
	context.update(userContext)
	template = loader.get_template('labTestRequests.html')
	return HttpResponse(template.render(context,request))

@csrf_exempt
@login_required
def labtestAction(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Lab Staff':
		lab_test_id = request.POST['lab_test_id']
		post_data = dict(request.POST.lists())
	#    Records.objects.filter(records_id=record_id).update(document=document, last_updated_date=timezone.now())
		action_taken = request.POST['action_taken']
		if(action_taken == 'Approve'):
			Lab_Test.objects.filter(lab_test_id=lab_test_id).update(status='Approved', action_taken_date=timezone.now())
		elif(action_taken == 'Deny'):
			Lab_Test.objects.filter(lab_test_id=lab_test_id).update(status='Denied', action_taken_date=timezone.now())
		return labtestRequests(request)

@csrf_exempt
@login_required
def labstaffWorklist(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	labTestQuery = Lab_Test.objects.filter(status='Approved').order_by('action_taken_date')
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

@csrf_exempt
@login_required
def createLabtestReport(request):
	userId = request.user
	role = getCurrentUserRole(userId)
	if role == 'Lab Staff':
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
		return labstaffWorklist(request)

def insuranceApprovedMail(request,claim_id):
	#how to fetch the claim_id
    record = Claim_Request.objects.get(claim_id=claim_id)
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

def insuranceDeniedMail(request,claim_id):
    record = Claim_Request.objects.get(claim_id=claim_id)
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

class ClaimTableView(tables.SingleTableView):
    table_class = ClaimTable
    queryset = Claim_Request.objects.all()
    template_name = "claimTable.html"
    
def payment_records(request):
    #patient_id = request.user.patient_id
    patient_id = '10'
    paymentsTable = PaymentTable(Payments.objects.filter(patient_id=patient_id).order_by('payment_update_date'))
    claimsTable = ClaimTable(Claim_Request.objects.filter(patient_id=patient_id).order_by('claim_raised_date'))
    
    template = loader.get_template('insurancePortal.html')
    context = {
        'paymentsTable' : paymentsTable,
        'claimsTable' : claimsTable,
        'patient_id' : patient_id,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def saveInsurInfo(request):
    if request.method == "POST":

        insurName = request.POST.get('insurName')
        insurancePv = InsuranceProvider.objects.get(provider_name=insurName)
        #request.user.patient_insurance_provider_id = insurancePv.provider_id
        patientMemID = request.POST.get('patientInsurID')
        #request.user.patient_insurance_member_id = patientMemID

        #Patient.objects.filter(patient_id = request.user.patient_id).update(patient_insurance_provider_id = insurancePv, patient_insurance_member_id = patientMemID )
        Patient.objects.filter(patient_id = 10).update(patient_insurance_provider_id = insurancePv, patient_insurance_member_id = patientMemID )

    return payment_records(request)

@csrf_exempt
def fileClaim(request):
    #patient_id = request.user.patient_id
    patient_id = '10'
    claim_raised_date = datetime.now()
    payment_ID = request.POST['payment_id']
    if Claim_Request.objects.filter(payment_id = payment_ID).count() == 0:

        Claim_Request.objects.create(patient_id_id = patient_id, payment_id_id = payment_ID, claim_status = 'pending', claim_raised_date = claim_raised_date)

    return payment_records(request)


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
