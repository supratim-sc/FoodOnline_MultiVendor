from django import forms

from .models import User, UserProfile

class UserRegistrationForm(forms.ModelForm):
    # making the password field of type password
    password = forms.CharField(widget=forms.PasswordInput())

    # creating new field confirm_password and making it of type password
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']

    '''
        The clean() method in Django models provides a powerful way to validate and clean data before it gets saved. This method is called during the validation process triggered by forms or model instances. By overriding clean(), you can ensure that your data meets specific business rules or integrity constraints.
    '''
    # creating DJANGO NON FIELD ERROR
    def clean(self):    # here self refers to the UserRegistrationForm
        # overriding the clean() method to add custom validation logic
        cleaned_data = super(UserRegistrationForm, self).clean()

        # getting the password from the UserRegistrationForm after cleaning
        password = self.cleaned_data.get('password')
        # getting the confirm_password from the UserRegistrationForm after cleaning
        confirm_password = self.cleaned_data.get('confirm_password')

        # checking password and confirm_password are not ame then raising non_field error 
        # as confirm password is not a field of User model, hence this errors are known as non-field errors
        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match!!")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude']