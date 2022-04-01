from django_tables2 import tables, TemplateColumn
from secure_hospital_system.models import Claim_Request, Payments


class ClaimTable(tables.Table):
    class Meta:model = Claim_Request
    attrs = {'class': 'claim_table table-sm'}
    #fields = ['Insurance ID', 'Claim ID', 'Bill ID', 'Bill Amount', 'Bill Date', 'Claim Status', 'File_Claim']
    #fields = ['Claim ID', 'insur_id', 'claim_raised_date', 'claim_status', 'file']


class PaymentTable(tables.Table):
    class Meta:model = Payments
    attrs = {'class': 'payment_table table-sm'}
    #fields = ['Insurance ID', 'Claim ID', 'Bill ID', 'Bill Amount', 'Bill Date', 'Claim Status', 'File_Claim']
    fields = ['Claim ID', 'insur_id', 'claim_raised_date', 'claim_status', 'file']
    file = TemplateColumn(template_name='btn.html')    