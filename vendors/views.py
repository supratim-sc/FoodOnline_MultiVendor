from django.shortcuts import get_object_or_404, render

from .models import Vendor
from .forms import VendorRegistrationForm

from accounts.models import UserProfile
from accounts.forms import UserProfileForm

# Create your views here.
def my_restaurant(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor_profile = get_object_or_404(Vendor, user=request.user)

    user_profile_form = UserProfileForm(instance=user_profile)
    vendor_profile_form = VendorRegistrationForm(instance=vendor_profile)

    context = {
        'user_profile' : user_profile,
        'vendor_profile' : vendor_profile,
        'user_profile_form' : user_profile_form,
        'vendor_profile_form' : vendor_profile_form,
    }

    return render(request, 'vendors/vendor_my_restaurant.html', context)