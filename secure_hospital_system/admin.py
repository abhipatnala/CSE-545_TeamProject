from django.contrib import admin
from .models import *
import django_mfa
#from django.contrib.auth.models import User

admin.site.register(SHSUser)
admin.site.register(InsuranceProvider)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Doctor_availability_booked)
admin.site.register(Records)
admin.site.register(Payments)
admin.site.register(Claim_Request)
admin.site.register(Lab_Test)
admin.site.unregister(django_mfa.models.U2FKey)