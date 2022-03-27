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

class DoctorView(tables.Table):
    class MetaView:
        model = Doctor_availability_booked
        fields = ['patient_name','doctor_name','appointment_date','appointment_start_time','appointment_end_time','status']
    patient_Name = tables.Column(accessor='Patient.SHSUser.get_full_name()', verbose_name="patient name")
    doctor_name = tables.Column(accessor='Doctor.SHSUser.get_full_name()', verbose_name="patient name")

class RecordsTable(tables.Table):
    class Meta:
        model = Records
        fields = ['Records_id', 'Doctor_Name', 'Patient_Name', 'ViewDiagnosis', 'Last_Modified']
    Records_id = tables.Column(accessor='records_id')
    Doctor_Name = tables.Column(accessor='doctor.user.user_name', verbose_name="Doctor Name")
    Patient_Name = tables.Column(accessor='patient.user.user_name', verbose_name="Patient Name")
    ViewDiagnosis = tables.TemplateColumn(template_name='viewRecords.html', verbose_name="Document")
    Last_Modified = tables.Column(accessor='last_modified_date')

class PatientDetails(tables.Table):
    class Meta:
        model = Patient
        fields = ['Patient_ID', 'Patient_Name', 'Patient_DOB']
    Patient_ID = tables.Column(accessor='patient_id')
    Patient_Name = tables.Column(accessor='patient.user.user_name', verbose_name='Patient Name')
    Patient_DOB = tables.Column(accessor='patient.patient_dob', verbose_name='PatientDob')