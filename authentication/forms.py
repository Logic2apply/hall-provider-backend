from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "username": forms.TextInput(attrs={"class": ""}),
            "password": forms.PasswordInput(attrs={"class": ""})
        }


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": ""}),
            "last_name": forms.TextInput(attrs={"class": ""}),
            "email": forms.EmailInput(attrs={"class": ""}),
            "username": forms.TextInput(attrs={"class": ""}),
            "password": forms.PasswordInput(attrs={"class": ""})
        }
