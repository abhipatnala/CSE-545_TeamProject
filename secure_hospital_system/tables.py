import django_tables2 as tables
from .models import *
from dataclasses import fields
from pyexpat import model
from tabnanny import verbose

class SimpleTable(tables.Table):
    class Meta:
        model = Doctor_availability_booked
        fields = ['patient_id','doctor_id','appointment_date','appointment_start_time','appointment_end_time','edit']
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
    Appointment_id = tables.Column(accessor="booking_id", verbose_name="Appointment ID")
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

class RecordsTable(tables.Table):
    class Meta:
        model = Records
        fields = ['Records_id', 'Doctor_Name', 'Patient_Name', 'ViewDiagnosis', 'Last_Modified']
    Records_id = tables.Column(accessor='records_id')
    Doctor_Name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    Patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    Patient_id = tables.Column(accessor='patient.patient_id',visible=False)
    ViewDiagnosis = tables.TemplateColumn(template_name='viewRecords.html', verbose_name="Document", extra_context={'patient_id' : Patient_id})
    Last_Modified = tables.Column(accessor='last_modified_date')

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
    patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    recommended_tests = tables.Column(accessor='Recommended_tests',verbose_name='Recommended Tests')
    date = tables.Column(accessor='recommended_date', verbose_name='Date')
    approve_deny = tables.TemplateColumn(template_name='labtest_approve_deny.html', verbose_name="Decision")

class LabStaffView(tables.Table):
    class MetaView:
        model = Lab_Test
        fields = ['Patient_Name', 'Doctor_Name', 'Test_name', 'Date', 'Approve/Deny','create_labtest_report']
    patient_Name = tables.Column(accessor='patient.user_id.user.first_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor.user_id.user.first_name', verbose_name="Doctor Name")
    test_name = tables.Column(accessor='Recommended_tests',verbose_name='Recommended Tests')
    date = tables.Column(accessor='action_taken_date', verbose_name='Date')
    create_labtest_report = tables.TemplateColumn(template_name='create_labtest_report.html', verbose_name="Create Report")
    

class ClaimTable(tables.Table):
    class Meta:model = Claim_Request
    attrs = {'class': 'claim_table table-sm'}
    #fields = ['Insurance ID', 'Claim ID', 'Bill ID', 'Bill Amount', 'Bill Date', 'Claim Status', 'File_Claim']
    #fields = ['Claim ID', 'insur_id', 'claim_raised_date', 'claim_status', 'file']


class PaymentTable(tables.Table):
    class Meta:model = Payments
    attrs = {'class': 'payment_table table-sm'}
    #fields = ['Insurance ID', 'Claim ID', 'Bill ID', 'Bill Amount', 'Bill Date', 'Claim Status', 'File_Claim']
    fields = ['Claim ID', 'insur_id', 'claim_raised_date', 'claim_status', 'file']
    file = tables.TemplateColumn(template_name='btn.html')  

