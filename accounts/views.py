from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import UserRegistrationForm, VendorRegistrationForm
from .models import User, UserProfile
from .utils import get_url_by_user_role, send_email

from vendors.models import Vendor


# Restrict customer to access vendor_dahsboard
def check_role_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied

# Restrict vendor to access customer_dahsboard
def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied


# Create your views here.
def user_registration(request):
    # if the user is already logged in
    if request.user.is_authenticated:
        # Showing message
        messages.warning(request, 'You already have an account!!')

        # redirecting to the my_account page
        return redirect('my_account')
    
    # if the user submits the form then
    elif request.method == "POST":
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

            # # sending User activation email
            # send_user_activation_mail(request, user)

            # sending Vendor activation email using new combined method
            send_email(request, user, mail_subject='Activate your account', html_template_name='accounts/email/user_account_verification_email.html')

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


def vendor_registration(request):
    # if the user is already logged in
    if request.user.is_authenticated:
        # Showing message
        messages.warning(request, 'You already have an account!!')

        # redirecting to the my_account page
        return redirect('my_account')
    
    elif request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and vendor_form.is_valid():
            # getting the data after cleaning form the form
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']

            # setting the user from the data from the form
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

            # setting the role
            user.role = User.VENDOR

            # saving the user with all previous data from the form and the newly assigned role
            user.save()

            # Saving the Vendor
            # here, commit=False as we want to add user and user_profile which is not present in the vendor_form, 
            # as vendor_form only has two fields, vendor_name and vendor_license
            vendor = vendor_form.save(commit=False) 

            # setting the user to the vendor
            vendor.user = user

            # fetching the UserProfile using the user
            user_profile = UserProfile.objects.get(user=user)

            # setting the user_profile
            vendor.user_profile = user_profile

            # saving the vendor 
            vendor.save()

            # # sending Vendor activation email
            # send_user_activation_mail(request, user)

            # sending Vendor activation email using new combined method
            send_email(request, user, mail_subject='Activate your account', html_template_name='accounts/email/user_account_verification_email.html')

            # showing success message using Django Messages 
            messages.success(request, 'Account has been created successfully!!')

            # after saving the user redirecting the user back to the registration form
            return redirect('vendor_registration')
    
    # if GET request then show the foorm
    else:
        user_form = UserRegistrationForm()
        vendor_form = VendorRegistrationForm()

    context = {
        'user_form' : user_form,
        'vendor_form' : vendor_form,
    }

    return render(request, 'accounts/vendor_registration.html', context)


def login(request):
    # if the user is already logged in
    if request.user.is_authenticated:
        # Showing message
        messages.warning(request, 'You are already logged in!!')
        # redirecting to the my_account page
        return redirect('my_account')
    
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # checking if user exists with the provided email and password
        user = auth.authenticate(email=email, password=password)

        # if any user found with the provided credentials
        if user:
            # logging in the user
            auth.login(request, user)

            # showing success message
            messages.success(request, 'You have logged in successfully!!')

            # redirecting the user to the my_account page
            return redirect('my_account')
        
        # if not correct credentials
        else:
            # showing error mesage
            messages.error(request, 'Invalid credentials!! Enter correct credentials!!')

            # redirecting the user again to the login page
            return redirect('login')
        
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    # loging out the user
    auth.logout(request)
    
    # showing message
    messages.info(request, 'You have logged out successfully!!')

    # redirecting the user to login page
    return redirect('login')


@login_required(login_url='login')
def my_account(request):
    # getting the user
    user = request.user
    
    # determining the redirecting page by the role of the user
    redirect_url = get_url_by_user_role(user)

    # redirecting the user
    return redirect(redirect_url)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)

    context = {
        'vendor' : vendor
    }

    return render(request, 'accounts/vendor_dashboard.html', context)


def account_activation(request, user_id_encoded, token):
    try:
        # retriving/decoding the user_id from the encoded user_id
        user_id = urlsafe_base64_decode(user_id_encoded).decode()

        # getting the user using the user_id
        user = User.objects.get(pk=user_id)

    # if user not found or token not valid or other errors
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        # set user to None
        user = None

    # if user is not None and token is valid
    if user and default_token_generator.check_token(user, token):
        # setting the is_active status of the user to True
        user.is_active = True

        # saving the user
        user.save()

        # showing the success message
        messages.success(request, 'Congratulations!! Your account has been activated!!')
    
    # if user is None or token is invalid 
    else:
        # showing error message
        messages.error(request, 'Invalid activation link!! Please try again!!')

    # redirecting the user to my_account page, for showing the login page to Customer/Vendor
    return redirect('my_account')



def forgot_password(request):
    if request.method == 'POST':
        # getting the email
        email = request.POST['email']

        # checking if any user exist with the provided email
        if User.objects.filter(email=email).exists():
            # getting the user
            user = User.objects.get(email__exact=email)

            # # sending password reset email
            # send_password_reset_mail(request, user)

            # sending password reset email
            send_email(request, user, mail_subject='Reset your password', html_template_name='accounts/email/user_password_reset_email.html')

            # showing success message
            messages.success(request, 'Password reset email has been sent to your email!!')

            # redirecting the user to the login page
            return redirect('login')
        
        # if any user with the provided email does not exists
        else:
            # showing error message
            messages.error(request, 'Account does not exist!!')

            # redirecting user to the forgot_password page
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validation(request, user_id_encoded, token):
    try:
        # retriving/decoding the user_id from the encoded user_id
        user_id = urlsafe_base64_decode(user_id_encoded).decode()

        # getting the user using the user_id
        user = User.objects.get(pk=user_id)

    # if user not found or token not valid or other errors
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        # set user to None
        user = None

    # if user is not None and token is valid
    if user and default_token_generator.check_token(user, token):
        # saving the user id to the request.sesion so that we can access it in the reset_password method
        request.session['user_id'] = user_id

        # showing message
        messages.info(request, 'Please reset your password!!')

        # redirecting the user to the password reset page
        return redirect('reset_password')
    
    # if user is None or token is invalid 
    else:
        # showing error message
        messages.error(request, 'Password reset link is invalid or expired!!')

    # redirecting the user to my_account page, for showing the login page to Customer/Vendor
    return redirect('my_account')


def reset_password(request):
    # if user submits the form
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # checking if password and confirm_password are equal or not
        if password == confirm_password:
            # retriving the user_id from the request.session which is saved earlier
            user_id = request.session.get('user_id')

            # getting the use from the user_id
            user = User.objects.get(pk=user_id)

            # setting the password
            user.set_password(password)

            # saving hte user
            user.save()
            
            # deleting the user_id from the request.session
            del request.session['user_id']

            # showing success message
            messages.success(request, 'Password changed successfully!!')

            # redirecting the user to the login page
            return redirect('login')
        
        # if password and confirm_password does not matches
        else:
            # showing error message
            messages.error(request, 'Password and Confirm Password does not matches!! Try again!!')

            # redirecting the user back to the reset_password page
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')