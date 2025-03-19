from django.shortcuts import render, redirect
from django.contrib import messages

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
            '''
            # ----- WAY-1 OF SAVING THE USER USING FORM
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
            '''


            # ----- WAY-2 OF SAVING THE USER USING create_user() method from the UserManager class
            # getting the data after cleaning form the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # setting the user from the data from the form
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

            # setting the role
            user.role = User.CUSTOMER

            # saving the user with all previous data from the form and the newly assigned role
            user.save()

            # showing success message using Django Messages 
            messages.success(request, 'Account has been created successfully!!')

            # after saving the user redirecting the user back to the registration form
            return redirect('user_registration')

            
    # if the user visits the page i.e., GET request the showing the blank form
    else:   # we implemented this else if have form.errors, otherwise the form will be rendered over the errors and we can't see the errors in the template
        form = UserRegistrationForm()

    # sending the form as context dictionary to the HTML Template
    context = {
        'form' : form,
    }

    return render(request, 'accounts/user_registration.html', context)