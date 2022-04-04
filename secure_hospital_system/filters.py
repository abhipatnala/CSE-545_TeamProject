import django_filters
from .tables import *
from .models import *

class PatientViewFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        #fields = '__all__'
        fields = ['patient_id', 'blood_type']
    patient_id = django_filters.CharFilter(field_name='patient_id__user_id__user__first_name',label='Patient Name' , lookup_expr='contains')
    blood_type = django_filters.CharFilter(field_name='blood_type',label='Blood Type' , lookup_expr='exact')

class ClaimRequestViewFilter(django_filters.FilterSet):
    class Meta:
        model = Claim_Request
        fields = '__all__'
        exclude = ['payment_id','patient_id']

class DoctorViewFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor_availability_booked
        fields = ['patient_id', 'appointment_date', 'status']
    patient_id = django_filters.CharFilter(field_name='patient_id__user_id__user__first_name',label='Patient Name' , lookup_expr='contains')
    appointment_date = django_filters.CharFilter(field_name='appointment_date',label='Date' , lookup_expr='contains')

class LabStaffViewFilter(django_filters.FilterSet):
    class Meta:
        model = Lab_Test
        fields = ['patient_id', 'action_taken_date']
    patient_id = django_filters.CharFilter(field_name='patient__user_id__user__first_name',label='Patient Name' , lookup_expr='contains')
    action_taken_date = django_filters.DateFilter(field_name='action_taken_date',label='Date' , lookup_expr='contains')