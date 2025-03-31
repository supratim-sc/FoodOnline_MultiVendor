from django import forms


from vendors.models import Vendor


class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'vendor_license']