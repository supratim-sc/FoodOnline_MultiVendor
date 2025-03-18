from django.shortcuts import render

from .forms import UserRegistrationForm

# Create your views here.
def user_registration(request):
    form = UserRegistrationForm()

    context = {
        'form' : form,
    }

    return render(request, 'accounts/user_registration.html', context)