from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'location', 'phone_number']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            # "gender": forms.Select(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "location": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'class': 'form-control'})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'class': 'form-control'})


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'phone_number']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),

            # "gender": forms.Select(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "location": forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "type": "password",
        "placeholder": "Enter Password"
    }))
    new_password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "type": "password",
        "placeholder": "Re-enter Password"
    }))
    old_password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "type": "password",
        "placeholder": "Enter Old Password"
    }))
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password1','new_password2']

    # def __init__(self, *args, **kwargs):
    #     super(ChangePasswordForm, self).__init__(*args, **kwargs)
    #     self.fields['new_password1'].widget = widgets.PasswordInput(
    #         attrs={'class': 'form-control'})
    #     self.fields['new_password2'].widget = widgets.PasswordInput(
    #         attrs={'class': 'form-control'})
    #     self.fields['old_password'].widget = widgets.PasswordInput(
    #         attrs={'class': 'form-control'})

   
