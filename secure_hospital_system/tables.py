import django_tables2 as tables
from .models import *
from dataclasses import fields
from pyexpat import model
from tabnanny import verbose

class SimpleTable(tables.Table):
    class Meta:
        model = Doctor_availability_booked
        fields = ['Appointment_id','patient_name','doctor_name','appointment_date','appointment_start_time','appointment_end_time','edit']
    patient_name = tables.Column(accessor='patient_id.user_id.user.first_name', verbose_name="Patient Name")
    Appointment_id = tables.Column(accessor="booking_id", verbose_name="Appointment ID", visible=False)
    doctor_name =  tables.Column(accessor='doctor_id.user_id.user.first_name', verbose_name='Doctor Name')
    appointment_date = tables.Column(accessor='appointment_date', verbose_name='Appointment Date')
    appointment_start_time = tables.Column(accessor='appointment_start_time', verbose_name='Start Time')
    appointment_end_time = tables.Column(accessor='appointment_end_time', verbose_name='End Time')    
    edit = tables.TemplateColumn(template_name='btn.html'  )

class ClaimRequestTable(tables.Table):
    class Meta:
        model = Claim_Request
        fields = ['claim_status','claim_raised_date']
    edit = tables.TemplateColumn(template_name='insuranceconf.html')

class Appointments(tables.Table):
    class Meta:
        model = Doctor_availability_booked
        fields = ['Appointment_id', 'Doctor_Name', 'Appointment_Date', 'Appointment_start_time', 'Appointment_end_time', 'Status', 'AppointmentDetails']
    Appointment_id = tables.Column(accessor="booking_id", verbose_name="Appointment ID", visible=False)
    Doctor_Name =  tables.Column(accessor='doctor_id.user_id.user.first_name', verbose_name='Doctor Name')
    Appointment_Date = tables.Column(accessor='appointment_date', verbose_name='Appointment Date')
    Appointment_start_time = tables.Column(accessor='appointment_start_time', verbose_name='Start Time')
    Appointment_end_time = tables.Column(accessor='appointment_end_time', verbose_name='End Time')
    Status = tables.Column(accessor='status', verbose_name='Appointment Status')
    AppointmentDetails = tables.TemplateColumn(template_name='viewAppointment.html', verbose_name="Appointment Details")

class DoctorView(tables.Table):
    class MetaView:
        model = Doctor_availability_booked
        fields = ['patient_name','doctor_name','appointment_date','appointment_start_time','appointment_end_time','status','ViewAppointment']
    patient_Name = tables.Column(accessor='patient_id.user_id.user.first_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor_id.user_id.user.first_name', verbose_name="Doctor Name")
    appointment_date = tables.Column(accessor='appointment_date', verbose_name='Appointment Date')
    appointment_start_time = tables.Column(accessor='appointment_start_time', verbose_name='Start Time')
    appointment_end_time = tables.Column(accessor='appointment_end_time', verbose_name='End Time')
    Status = tables.Column(accessor='status', verbose_name='Appointment Status')
    viewAppointment = tables.TemplateColumn(template_name='viewAppointment.html', verbose_name="Appointment Details")
    patient_id = tables.Column(accessor='patient_id.patient_id', visible=False)

class PatientsView(tables.Table):
    class MetaView:
        model = Patient
        fields = ['patient_name','phone_number','patient_insurance_member_id','blood_type',
        'emergency_contact_phone_number','emergency_contact_firstname','emergency_contact_email','allergies',
        'medicationFollowed','preExistingMedicalConditions','anyOtherMedicalDetails']
    patient_name = tables.Column(accessor='user_id.user.first_name', verbose_name="Patient Name")
    phone_number = tables.Column(accessor='phone_number', verbose_name="Phone Number")
    patient_insurance_member_id = tables.Column(accessor='patient_insurance_member_id', verbose_name='Insurance Member Id')
    blood_type = tables.Column(accessor='blood_type', verbose_name='Blood Type')
    emergency_contact_phone_number = tables.Column(accessor='emergency_contact_phone_number', verbose_name='Emergency Contact Number')
    emergency_contact_firstname = tables.Column(accessor='emergency_contact_firstname',verbose_name='Emergency Contact Name')
    emergency_contact_email = tables.Column(accessor='emergency_contact_email', verbose_name='Emergency Contact Email')
    allergies = tables.Column(accessor='allergies', verbose_name='Allergies')
    medicationFollowed = tables.Column(accessor='medicationFollowed', verbose_name='Medication Followed')
    preExistingMedicalConditions = tables.Column(accessor='preExistingMedicalConditions', verbose_name='Pre Existing Medical Conditions')
    anyOtherMedicalDetails = tables.Column(accessor='anyOtherMedicalDetails',verbose_name='Other Medical Details')
    viewDetails = tables.TemplateColumn(template_name='viewPatientDetails.html', verbose_name="View Details")
    patient_id = tables.Column(accessor='patient_id', visible=False)
    
class RecordsTable(tables.Table):
    class Meta:
        model = Records
        fields = ['Records_id', 'Doctor_Name', 'Patient_Name', 'ViewDiagnosis', 'Last_Modified']
    Records_id = tables.Column(accessor='records_id', visible=False)
    Doctor_Name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    Patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    Patient_id = tables.Column(accessor='patient.patient_id',visible=False)
    ViewDiagnosis = tables.TemplateColumn(template_name='viewRecords.html', verbose_name="Document", extra_context={'patient_id' : Patient_id})
    Last_Modified = tables.Column(accessor='last_modified_date')

class PaymentsTable(tables.Table):
    class Meta:
        model = Payments
        fields = ['payment_id', 'patient_name', 'admit_fee', 'discharge_fee', 'supplies_fee', 'consultation_fee', 'overall_payment', 'payment_generated_date', 'payment_status', 'is_claimed']
    payment_id = tables.Column(accessor='payment_id', visible=False)
    patient_name = tables.Column(accessor='patient_id.user_id.user.first_name', visible='Patient Name')
    admit_fee = tables.Column(accessor='admit_fee', verbose_name='Admit Fee')
    discharge_fee = tables.Column(accessor='discharge_fee', verbose_name='Discharge Fee')
    supplies_fee = tables.Column(accessor='supplies_fee', verbose_name='Supplies Fee')
    consultation_fee = tables.Column(accessor='consultation_fee', verbose_name='Consultation Fee')
    overall_payment = tables.Column(accessor='overall_payment', verbose_name='Overall Fees')
    payment_generated_date = tables.Column(accessor='payment_generated_date', visible='Bill Date')
    payment_status = tables.Column(accessor='payment_status', verbose_name='Status')
    is_claimed = tables.Column(accessor='is_claimed', verbose_name='Insurance Claimed?')


class PatientDetails(tables.Table):
    class Meta:
        model = Patient
        fields = ['Patient_ID', 'Patient_Name', 'Patient_DOB']
    Patient_ID = tables.Column(accessor='patient_id')
    Patient_Name = tables.Column(accessor='patient.user.user_name', verbose_name='Patient Name')
    Patient_DOB = tables.Column(accessor='patient.patient_dob', verbose_name='PatientDob')

class LabTestRequests(tables.Table):
    class MetaView:
        model = Lab_Test
        fields = ['Patient_Name', 'Doctor_Name', 'Recommended_Test', 'Date', 'Approve/Deny']
    lab_test_id = tables.Column(accessor='lab_test_id', visible=False)
    patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    recommended_tests = tables.Column(accessor='Recommended_tests',verbose_name='Recommended Tests')
    date = tables.Column(accessor='recommended_date', verbose_name='Date')
    approve_deny = tables.TemplateColumn(template_name='labtestApproveDeny.html', verbose_name="Decision")

class LabStaffView(tables.Table):
    class MetaView:
        model = Lab_Test
        fields = ['Patient_Name', 'Doctor_Name', 'Test_name', 'Date', 'Approve/Deny','create_labtest_report', 'record', 'status']
    patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    test_name = tables.Column(accessor='Recommended_tests',verbose_name='Recommended Tests')
    date = tables.Column(accessor='action_taken_date', verbose_name='Date')
    status = tables.Column(accessor='status', visible=False)
    record = tables.Column(accessor='record.records_id', visible=False)
    create_labtest_report = tables.TemplateColumn(template_name='createLabtestReport.html', verbose_name="Create Report")
    
    

class ClaimTable(tables.Table):
    class Meta:
        model = Claim_Request
        fields = ['patient_name','claim_raised_date','claim_status','overall_payment']
    patient_name = tables.Column(accessor='patient_id.user_id.user.first_name', verbose_name="Patient Name")
    claim_raised_date = tables.Column(accessor='claim_raised_date', verbose_name='Claim Raised Date')
    claim_status = tables.Column(accessor='claim_status', verbose_name='Claim Status')
    overall_payment = tables.Column(accessor='payment_id.overall_payment', verbose_name='Overall Fees')
    block = tables.TemplateColumn(template_name='blockchain.html')


class PaymentTable(tables.Table):
    class Meta:
        model = Payments
        fields = ['payment_id', 'patient_name', 'admit_fee', 'discharge_fee', 'supplies_fee', 'consultation_fee',
         'overall_payment', 'payment_generated_date', 'payment_status', 'file']
    payment_id = tables.Column(accessor='payment_id', visible=False)
    patient_name = tables.Column(accessor='patient_id.user_id.user.first_name', visible='Patient Name')
    admit_fee = tables.Column(accessor='admit_fee', verbose_name='Admit Fee')
    discharge_fee = tables.Column(accessor='discharge_fee', verbose_name='Discharge Fee')
    supplies_fee = tables.Column(accessor='supplies_fee', verbose_name='Supplies Fee')
    consultation_fee = tables.Column(accessor='consultation_fee', verbose_name='Consultation Fee')
    overall_payment = tables.Column(accessor='overall_payment', verbose_name='Overall Fees')
    payment_generated_date = tables.Column(accessor='payment_generated_date', visible='Bill Date')
    payment_status = tables.Column(accessor='payment_status', verbose_name='Status')
    file = tables.TemplateColumn(template_name='claimbtn.html', verbose_name="File") 

