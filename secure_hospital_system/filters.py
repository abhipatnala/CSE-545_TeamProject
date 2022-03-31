import django_filters
from .tables import *
from .models import *

class PatientViewFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = '__all__'

class ClaimRequestViewFilter(django_filters.FilterSet):
    class Meta:
        model = Claim_Request
        fields = '__all__'
        exclude = ['payment_id','patient_id']