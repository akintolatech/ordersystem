from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                # 'maxlength': '7',
                # 'pattern': r'\d{2}/\d{4}'
            }
        )
    )
