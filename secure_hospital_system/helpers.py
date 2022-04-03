from .models import *
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import *
from django.core.mail import send_mail

def getRoleBasedMenus(user_id):
    user =  SHSUser.objects.select_related().filter(user = user_id)

    role = user[0].role_id
    role_name =''
    if role is not None:
        role_name = role.role_name
    menuList = Menu_Mapping.objects.filter(role_id = role.role_id)
    context = {
        'role_name' : role_name,
        'menuList' : menuList,
    }
    return context


def twofaEnabled(user):
    return hasattr(user, 'userotp')


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


def sendActivationEmail(user, current_site, user_email):
    subject = 'Activate Your MySite Account'
    body = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })

    send_mail(
        subject,
        body,
        'shsgrp1@gmail.com',
        [user_email],
        fail_silently=False
    )

def getCurrentUserRole(user_id):
    user =  SHSUser.objects.select_related().filter(user = user_id)
    role = user[0].role_id
    if role is not None:
        role_name = role.role_name
        return role_name
    return ''
