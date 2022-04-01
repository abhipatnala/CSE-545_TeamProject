from django.contrib import admin
from .models import *
#from django.contrib.auth.models import User
admin.site.register(Roles)
admin.site.register(SHSUser)
admin.site.register(InsuranceProvider)
admin.site.register(Patient)
admin.site.register(Shift_Timings)
admin.site.register(Doctor)
admin.site.register(Doctor_availability_booked)
admin.site.register(Records)
admin.site.register(Payments)
admin.site.register(Claim_Request)
admin.site.register(Menu)
admin.site.register(Menu_Mapping)
admin.site.register(Lab_Test)