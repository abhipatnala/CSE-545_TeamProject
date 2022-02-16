from django.db import models


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
