from django import forms
from complaint.models import report

class reportForm(forms.ModelForm):
    class Meta:
        model = report
        fields = ["report_type", "report_description"]

        widgets = {
            "report_type": forms.Select(attrs={'class': 'form-control'}),
            "report_description": forms.Textarea(attrs={'class': 'form-control'}),


        }