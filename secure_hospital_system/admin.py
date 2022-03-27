from xml.dom.minidom import DocumentType
from django.contrib import admin

import secure_hospital_system.models

# Register your models here.
admin.site.register(secure_hospital_system.models.User)
admin.site.register(secure_hospital_system.models.Shift)
admin.site.register(secure_hospital_system.models.Doctor)
admin.site.register(secure_hospital_system.models.Patient)
admin.site.register(secure_hospital_system.models.Records)
admin.site.register(secure_hospital_system.models.payments)
admin.site.register(secure_hospital_system.models.Doctor_availability_booked)
