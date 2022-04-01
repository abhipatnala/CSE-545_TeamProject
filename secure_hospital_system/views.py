from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Claim_Request, Payments
from .tables import ClaimTable, PaymentTable
import django_tables2 as tables
from datetime import datetime
from .models import InsuranceProvider, Patient
from django.views.decorators.csrf import csrf_exempt 



class ClaimTableView(tables.SingleTableView):
    table_class = ClaimTable
    queryset = Claim_Request.objects.all()
    template_name = "ClaimTable.html"
    
def payment_records(request):
    #patient_id = request.user.patient_id
    patient_id = '10'
    paymentsTable = PaymentTable(Payments.objects.filter(patient_id=patient_id).order_by('payment_update_date'))
    claimsTable = ClaimTable(Claim_Request.objects.filter(patient_id=patient_id).order_by('claim_raised_date'))
    
    template = loader.get_template('insurance_portal.html')
    context = {

        'paymentsTable' : paymentsTable,
        'claimsTable' : claimsTable,
        'patient_id' : patient_id,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def saveInsurInfo(request):
    if request.method == "POST":

        insurName = request.POST.get('insurName')
        insurancePv = InsuranceProvider.objects.get(provider_name=insurName)
        #request.user.patient_insurance_provider_id = insurancePv.provider_id
        patientMemID = request.POST.get('patientInsurID')
        #request.user.patient_insurance_member_id = patientMemID

        #Patient.objects.filter(patient_id = request.user.patient_id).update(patient_insurance_provider_id = insurancePv, patient_insurance_member_id = patientMemID )
        Patient.objects.filter(patient_id = 10).update(patient_insurance_provider_id = insurancePv, patient_insurance_member_id = patientMemID )

    return payment_records(request)

@csrf_exempt
def fileClaim(request):
    #patient_id = request.user.patient_id
    patient_id = '10' 
    claim_raised_date = datetime.now()
    payment_ID = request.POST['payment_id']
    if Claim_Request.objects.filter(payment_id = payment_ID).count() == 0:
        
        Claim_Request.objects.create(patient_id_id = patient_id, payment_id_id = payment_ID, claim_status = 'Pending', claim_raised_date = claim_raised_date)
        
    return payment_records(request) 