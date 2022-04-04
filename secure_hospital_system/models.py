from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

APPOINTMENT_STATUS = (
    ('approved','approved'),
    ('pending', 'pending'),
    ('denied','denied')
)

LAB_TEST_REQUEST_STATUS = (
    ('Approved', 'Approved'),
    ('Pending', 'Pending'),
    ('Denied','Denied'),
    ('Completed','Completed')
)

PAYMENT_STATUS = (
    ('unpaid', 'unpaid'),
    ('paid','paid')
)

GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHER', 'OTHER')
)

#Roles available are patient, admin, doctor, hospitalstaff, labstaff, insurancestaff
class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=100)

#Master Table
class SHSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

#Insurance Providers
class InsuranceProvider(models.Model):
   provider_id = models.BigAutoField(primary_key=True)
   provider_name = models.CharField(max_length=200)

#Patient Information
#pip install django-phonenumber-field[phonenumberslite]
class Patient(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(SHSUser, on_delete=models.CASCADE, related_name='patient_user')
    phone_number = models.CharField(max_length=10, default=None, blank=True, null=True)
    patient_dob = models.DateField(default=None, blank=True, null=True)
    patient_insurance_provider_id = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, default=None)
    patient_insurance_member_id = models.CharField(max_length=20, default=None, blank=True, null=True)
    patient_insurance_group_id = models.CharField(max_length=20, default=None, blank=True, null=True)
    blood_type = models.CharField(max_length=10, default=None, blank=True, null=True)
    address = models.CharField(max_length=150, default=None, blank=True, null=True)
    city = models.CharField(max_length=150, default=None, blank=True, null=True)
    state = models.CharField(max_length=150, default=None, blank=True, null=True)
    zipCode = models.CharField(max_length=5, default=None, blank=True, null=True)
    emergency_contact_firstname = models.CharField(max_length=25, default=None, blank=True, null=True)
    emergency_contact_lastname = models.CharField(max_length=25,  default=None, blank=True, null=True)
    emergency_contact_phone_number = models.CharField(max_length=10, default=None, blank=True, null=True)
    emergency_contact_email = models.CharField(max_length=50, default=None, blank=True, null=True)
    allergies = models.CharField(max_length=150, default=None, blank=True, null=True)
    medicationFollowed = models.CharField(max_length=150, default=None, blank=True, null=True)
    preExistingMedicalConditions = models.CharField(max_length=150, default=None, blank=True, null=True)
    anyOtherMedicalDetails = models.CharField(max_length=150, default=None, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDER, null=True)
    emergency_contact_gender = models.CharField(max_length=200, choices=GENDER, null=True)
    update_user = models.ForeignKey(SHSUser, on_delete=models.CASCADE, related_name='update_user', default=None)
    last_update_date = models.DateTimeField( null=True)

#Doctor Shifts
class Shift_Timings(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_type = models.CharField(max_length=150)

#Doctor Information
class Doctor(models.Model):
    doctor_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(SHSUser, on_delete=models.CASCADE) 
    shift_id = models.ForeignKey(Shift_Timings, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)

#Appointment Bookings
class Doctor_availability_booked(models.Model):
    booking_id = models.BigAutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField( null=True)
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    booking_request_timestamp = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField( null=True, default=None)
    approver_id = models.ForeignKey(SHSUser, on_delete=models.CASCADE,null=True, default=None) 
    status = models.CharField(max_length=200, choices=APPOINTMENT_STATUS, default='pending')

#Patient Documents
class Records(models.Model):
    records_id = models.BigAutoField(primary_key=True)
    class DocumentTypes(models.TextChoices):
        Diagnosis = 'D', _('Diagnosis')
        Prescription = 'P', _('Prescription')
        LabReport = 'L', _('LabReport')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    document = models.TextField(max_length=1000, null=True)
    created_date = models.DateTimeField(null=True)
    last_modified_date = models.DateTimeField(null=True)
    document_type = models.CharField(max_length=1, choices=DocumentTypes.choices)

#Payments/Bills
class Payments(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    admit_fee = models.IntegerField()
    discharge_fee = models.IntegerField()
    supplies_fee = models.IntegerField()
    consultation_fee = models.IntegerField()
    overall_payment = models.IntegerField()
    payment_generated_date = models.DateTimeField(auto_now_add=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=200, choices=PAYMENT_STATUS, default='unpaid')
    payment_update_date = models.DateTimeField()
    is_claimed = models.BooleanField(default=False)

#claims for bills
class Claim_Request(models.Model):
    claim_id = models.BigAutoField(primary_key=True)
    payment_id = models.ForeignKey(Payments, on_delete=models.CASCADE)
    claim_status = models.CharField(max_length=200, choices=APPOINTMENT_STATUS, default='pending')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    claim_raised_date = models.DateTimeField()
    claim_update_date = models.DateTimeField()

class Menu(models.Model):
    menu_id = models.BigAutoField(primary_key=True)
    menu_name = models.CharField(max_length=200)
    menu_url = models.CharField(max_length=200)

class Menu_Mapping(models.Model):
    menu_map_id = models.BigAutoField(primary_key=True)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)

class Lab_Test(models.Model):
    lab_test_id = models.BigAutoField(primary_key=True)
    record = models.ForeignKey(Records, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    recommended_test = models.TextField(max_length=200)
    recommended_date = models.DateField()
    action_taken_date = models.DateField(null=True)
    status = models.CharField(max_length=200, choices=LAB_TEST_REQUEST_STATUS, default='Pending')
