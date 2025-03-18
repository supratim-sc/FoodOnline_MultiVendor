from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    # making the password field of type password
    password = forms.CharField(widget=forms.PasswordInput())

    # creating new field confirm_password and making it of type password
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']