from django import forms


from vendors.models import Vendor


class VendorRegistrationForm(forms.ModelForm):
    vendor_license = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class' : 'btn btn-info'
            }
        )
    )

    class Meta:
        model = Vendor
        fields = ['name', 'vendor_license']