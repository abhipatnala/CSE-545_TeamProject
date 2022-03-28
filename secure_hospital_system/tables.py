from dataclasses import fields
from pyexpat import model
from tabnanny import verbose
import django_tables2 as tables
from .models import Doctor_availability_booked, Patient, Records

class RecordsTable(tables.Table):
    class Meta:
        model = Records
        fields = ['Records_id', 'Doctor_Name', 'Patient_Name', 'ViewDiagnosis', 'Last_Modified']
    Records_id = tables.Column(accessor='records_id')
    Doctor_Name = tables.Column(accessor='doctor.user.user_name', verbose_name="Doctor Name")
    Patient_Name = tables.Column(accessor='patient.user.user_name', verbose_name="Patient Name")
    ViewDiagnosis = tables.TemplateColumn(template_name='patient_portal/viewRecords.html', verbose_name="Document")
    Last_Modified = tables.Column(accessor='last_modified_date')

class PatientDetails(tables.Table):
    class Meta:
        model = Patient
        fields = ['Patient_ID', 'Patient_Name', 'Patient_DOB']
    Patient_ID = tables.Column(accessor='patient_id')
    Patient_Name = tables.Column(accessor='patient.user.user_name', verbose_name='Patient Name')
    Patient_DOB = tables.Column(accessor='patient.patient_dob', verbose_name='PatientDob')

class DoctorView(tables.Table):
    class MetaView:
        model = Doctor_availability_booked
        fields = ['patient_name','doctor_name','appointment_date','appointment_start_time','appointment_end_time','status','ViewAppointment']
    patient_Name = tables.Column(accessor='patient_id.user.user_name', verbose_name="Patient Name")
    doctor_name = tables.Column(accessor='doctor_id.user.user_name', verbose_name="Doctor Name")
    appointment_date = tables.Column(accessor='appointment_date', verbose_name='Appointment Date')
    appointment_start_time = tables.Column(accessor='appointment_start_time', verbose_name='Start Time')
    appointment_end_time = tables.Column(accessor='appointment_end_time', verbose_name='End Time')
    viewAppointment = tables.TemplateColumn(template_name='doctor_portal/viewAppointment.html', verbose_name="Appointment Details")