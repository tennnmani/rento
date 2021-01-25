from django import forms
from enquiry.models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email",
                  "address", "occupation", "question"]

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.NumberInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "occupation": forms.TextInput(attrs={'class': 'form-control'}),
            "question": forms.Textarea(attrs={'class': 'form-control'}),

        }