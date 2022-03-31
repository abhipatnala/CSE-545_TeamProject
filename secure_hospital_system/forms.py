from django import forms
from django.forms import ModelForm
from .models import Patient

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        labels = {
            'Fname': '',
            'Lname':'',
            'age' : '',
            'phone': '',
        }
        widgets = {
            'Fname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'Lname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'age' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Age'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
        }
        