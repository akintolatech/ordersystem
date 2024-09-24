from django import forms
from .models import Client
from django.forms.utils import ErrorList


class NameForm(forms.ModelForm):
    # Additional field for estate_id
    estate_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Client
        fields = ('username', 'password', 'estate_id',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your nick-name i.e segxy'}),
            'password': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'pattern':'(080|070|090|081)\d{8}' }),
        }

        labels = {
            'username': False,
            'password': False,
            'estate_id': False,
        }

        widgets['password'].attrs['maxlength'] = '11'




