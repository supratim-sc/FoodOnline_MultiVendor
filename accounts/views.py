from django.shortcuts import render, redirect

from .forms import UserRegistrationForm
from .models import User

# Create your views here.
def user_registration(request):
    # if the user submits the form then
    if request.method == "POST":
        # taking all data submitted by the user
        form = UserRegistrationForm(request.POST)
        # checking if all data is valid or not
        if form.is_valid():
            # if data is valid then taking all the data from the form and assign it to the user variable.
            # here commit=False means we are not commititg the changes 
            # as we need to add role to the user hence taking the form data and assign it the the user
            user = form.save(commit=False)

            # assigning the role as Customer to the user 
            user.role = User.CUSTOMER

            # ----- WAY-1 HASING THE PASSWORD USING THE set_password() -----
            # getting the password from the form
            password = form.cleaned_data['password']
            user.set_password(password)

            # saving the user with all previous data from the form and the newly assigned role
            user.save()

            # after saving the user redirecting the user back to the registration form
            return redirect('user_registration')
        
    # if the user visits the page i.e., GET request the showing the blank form
    form = UserRegistrationForm()

    # sending the form as context dictionary to the HTML Template
    context = {
        'form' : form,
    }

    return render(request, 'accounts/user_registration.html', context)