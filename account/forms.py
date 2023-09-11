from django import forms
from account.models import KYC
from django.forms import ImageField, FileInput, DateInput

class DateInput(forms.DateInput):
    # this enable automatic selection of date
    input_type = 'date'


class KYCForm (forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)

    class Meta:
        model = KYC
        fields = [
            'full_name',
            'image',
            'marital_status',
            'gender',
            'next_of_keen',
            'identity_type',
            'identity_image',
            'date_of_birth',
            'signature',
            'country',
            'state',
            'city',
            'mobile',
            'email',
            'fax',
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "Full Name"
            }),
            "mobile": forms.TextInput(attrs={
                "placeholder": "Mobile Number"
            }),
            "fax": forms.TextInput(attrs={
                "placeholder": "Fax Number"
            }),
            "country": forms.TextInput(attrs={
                "placeholder": "Country"
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "City"
            }),
            "next_of_keen": forms.TextInput(attrs={
                "placeholder": "Next of Keen"
            }),
        }
