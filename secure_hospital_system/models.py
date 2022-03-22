from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)


class Shift(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    start_time = models.DateTimeField
    end_time = models.DateTimeField
    shift_type = models.CharField(max_length=150)


class Doctor(models.Model):
    doctor_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_id = models.ForeignKey(Shift, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)


class Patient(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateField
    patient_dob = models.DateField
    address = models.CharField(max_length=400)
    zipcode = models.CharField(max_length=5)
    patient_insurance_provider_id = models.CharField(max_length=15)
    civil_status = models.CharField(max_length=15)
    emergency_contact_firstname = models.CharField(max_length=25)
    emergency_contact_lastname = models.CharField(max_length=25)
    emergency_contact_info = models.CharField(max_length=15)


class Records(models.Model):
    records_id = models.BigAutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # medical_history_id = models.ForeignKey(Medical_History, on_delete=models.CASCADE)
    document = models.JSONField

    class DocumentTypes(models.TextChoices):
        Diagnosis = 'D', _('Diagnosis')
        Prescription = 'P', _('Prescription')
        LabReport = 'L', _('LabReport')

    document_type = models.CharField(max_length=1, choices=DocumentTypes.choices)
