from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import City, Location, Room


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["city", "location", "house_number", "floor", "price",
                  "image1", "image2", "image3", "water", "internet", "parking", "description",
                   'c_parking', 'bedroom', 'bathroom','kitchen',
                  ]

        widgets = {
            "city": forms.Select(attrs={'class': 'form-control'}),
            "location": forms.Select(attrs={'class': 'form-control'}),
            "house_number": forms.TextInput(attrs={'class': 'form-control'}),
            "floor": forms.NumberInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}),
            "bedroom": forms.NumberInput(attrs={'class': 'form-control'}),
            "c_parking": forms.NumberInput(attrs={'class': 'form-control'}),
            
            "bathroom": forms.NumberInput(attrs={'class': 'form-control'}),
            "water": forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
            "internet": forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
            "parking": forms.NumberInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "kitchen": forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = "Select City"
        self.fields['location'].empty_label = "Select Location"
        self.fields['location'].queryset = Location.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['location'].queryset = Location.objects.filter(
                    city_id=city_id).order_by('location')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['location'].queryset = self.instance.city.location_set
            # .order_by('name')


class EditForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["city", "location", "house_number", "floor", "price", "image1", "image2", "image3", "water",
                  "internet", "parking", "description", 'room_status',  'c_parking', 'bedroom', 'bathroom','kitchen' ]

        widgets = {
            "city": forms.Select(attrs={'class': 'form-control'}),
            "location": forms.Select(attrs={'class': 'form-control'}),
            "house_number": forms.TextInput(attrs={'class': 'form-control'}),
            "floor": forms.NumberInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}),
            "water": forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
            "internet": forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
            "parking": forms.NumberInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "room_status": forms.Select(attrs={'class': 'form-control'}),
            
            "c_parking": forms.NumberInput(attrs={'class': 'form-control'}),
            "bedroom": forms.NumberInput(attrs={'class': 'form-control'}),
            "bathroom": forms.NumberInput(attrs={'class': 'form-control'}),
            "kitchen": forms.NumberInput(attrs={'class': 'form-control'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['image1'].queryset = Room.objects.none()
    #     self.fields['image2'].queryset = Room.objects.none()
    #     self.fields['image3'].queryset = Room.objects.none()

    #     if 'city' in self.data:
    #         try:
    #             city_id = int(self.data.get('city'))
    #             self.fields['location'].queryset = Location.objects.filter(city_id=city_id).order_by('location')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['location'].queryset = self.instance.city.location_set
    #         # .order_by('name')
