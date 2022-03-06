from django.db import models
from django.conf import settings
class Doctor_availability_booked(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    patied_id = models.IntegerField()
    doctor_id = models.IntegerField()
    appointment_date = models.DateField()
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    booking_request_timestamp = models.DateTimeField(auto_now_add=True)
    user_id_approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    status = models.CharField(max_length=30, default='Pending')