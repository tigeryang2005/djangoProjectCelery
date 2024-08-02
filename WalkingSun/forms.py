from django import forms
from django.core import validators


class UserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validators.MaxLengthValidator(limit_value=20)])
    last_login = forms.CharField(widget=forms.TextInput, required=False)
    is_superuser = forms.BooleanField(initial=False)
    username = forms.CharField(widget=forms.TextInput)
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput, validators=[validators.EmailValidator()])
    is_staff = forms.BooleanField(initial=False)
    is_active = forms.BooleanField(initial=False)
    date_joined = forms.DateTimeField(widget=forms.TextInput)
