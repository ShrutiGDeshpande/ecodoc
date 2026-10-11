# forms.py
from django import forms

class SignatureForm(forms.Form):
    employee_name = forms.CharField(max_length=100)
    signature_image = forms.ImageField()
