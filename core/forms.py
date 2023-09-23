from django import forms
from core.models import CreditCard


class CreditCardForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Card Holder Name"})
    )
    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Card Number"})
    )
    month = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Expiry Month"})
    )
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Expiry Year"})
    )
    cvv = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "CVV / Security Number"})
    )

    card_type = forms.ChoiceField(
        choices=[('visa', 'Visa'), ('mastercard', 'Mastercard')],
        initial='visa',
        widget=forms.Select(attrs={"placeholder": "Card Type"})
    )

    class Meta:
        model = CreditCard
        fields = ['name', 'number', 'month', 'year', 'cvv', 'card_type']

