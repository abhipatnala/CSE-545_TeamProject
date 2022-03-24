from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name =models.CharField(max_length=25, null=True)


class Shift(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    shift_type = models.CharField(max_length=150)


class Doctor(models.Model):
    doctor_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)


class Patient(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateField(null=True)
    patient_dob = models.DateField(null=True)
    address = models.CharField(max_length=400, null=True)
    zipcode = models.CharField(max_length=5, null=True)
    patient_insurance_provider_id = models.CharField(max_length=15, null=True)
    civil_status = models.CharField(max_length=15, null=True)
    emergency_contact_firstname = models.CharField(max_length=25, null=True)
    emergency_contact_lastname = models.CharField(max_length=25, null=True)
    emergency_contact_info = models.CharField(max_length=15, null=True)

class Records(models.Model):
    records_id = models.BigAutoField(primary_key=True)
    class DocumentTypes(models.TextChoices):
        Diagnosis = 'D', _('Diagnosis')
        Prescription = 'P', _('Prescription')
        LabReport = 'L', _('LabReport')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    document = models.JSONField(null=True)
    created_date = models.DateTimeField(null=True)
    last_modified_date = models.DateTimeField(null=True)
    document_type = models.CharField(max_length=1, choices=DocumentTypes.choices)
