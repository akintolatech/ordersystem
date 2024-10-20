from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        "autocomplete": "off"
        #'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        "autocomplete": "off"
        #'class': 'form-control',
    }))


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your Username', "autocomplete": "off"}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your Company Email', "autocomplete": "off"}),
        }

        # Remove help text for indicated fields by setting an empty dictionary
        help_texts = {
            'username': None,
            # 'password': None,
        }

    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput (
            attrs={
                'placeholder': 'Enter a valid phone number',
                'maxlength': '11',
                # 'pattern': r'\d{2}/\d{4}'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs= {
                "placeholder": "Enter a memorable Password"
            }
        )
    )

    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput (
            attrs={
                "placeholder": "Repeat Password"
            }
        )
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'photo']
