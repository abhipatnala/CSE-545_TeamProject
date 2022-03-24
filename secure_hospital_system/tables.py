from dataclasses import fields
from pyexpat import model
from tabnanny import verbose
import django_tables2 as tables
from .models import Patient, Records

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