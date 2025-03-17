from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# This class is used to create the user and the superuser with our custom configuration
class UserManager(BaseUserManager):
    # method to create a new user
    def create_user(self, first_name, last_name, username, email, password = None):
        # Checking if email is provided or not
        if not email:
            raise ValueError("User must have an email")
        
        # Checking if username is provided or not
        if not username:
            raise ValueError('User must have an username')
        
        # saving inputted data into the user model
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            # changing the case of inputted email address to a normalize form i.e., all in small case
            email = self.normalize_email(email),
        )

        # Setting the password for the user
        user.set_password(password)

        # saving the user record
        '''
            here using is used to specify in which database we want to save the user record of overwritten account model
            in our case we don't need to store the overwritten account model, 
            so, we are using the self._db which specify that use the default database which is configured in the settings.py file
        '''
        user.save(using = self._db)

        # returning the user
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password = None):
        # calling the create_user() method to save the record as an normal user
        super_user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            # changing the case of inputted email address to a normalize form i.e., all in small case
            email = self.normalize_email(email),
            # sending the password to create_user() method and there setting the password to the user
            password = password,
        )

        # Setting the admin properties to the user and making it as super user
        super_user.is_admin = True
        super_user.is_active = True
        super_user.is_staff = True
        super_user.is_superadmin = True

        # saving the super super_user record
        '''
            here using is used to specify in which database we want to save the user record of overwritten account model
            in our case we don't need to store the overwritten account model, 
            so, we are using the self._db which specify that use the default database which is configured in the settings.py file
        '''
        super_user.save(using = self._db)

        # returning the super user record
        return super_user
    
# Overwriting the User model with our custom user model
class User(AbstractBaseUser):
    
    # ROLES
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )
    
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(max_length = 100, unique = True)
    phone_number = models.CharField(max_length = 10, unique = True)
    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICE, default = CUSTOMER)

    date_joined = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    last_login = models.DateTimeField(auto_now = True)

    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)


    # Setting the UserManager class as Default Manager for Custom User Model
    objects = UserManager()

    # setting the email field as the required field for logging in
    USERNAME_FIELD = 'email'
    
    # Setting mandatory fields
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']   # here email is not required as it is username filed so it will be mandatory

    def __str__(self):
        return self.email
    

    # https://docs.djangoproject.com/en/5.1/ref/contrib/auth/#:~:text=this%20specific%20object.-,has_perm
    def has_perm(self, perm, obj = None):
        '''
            Returns True if the user has the specified permission. If the user is inactive, this method will always return False. 
            For an active superuser, this method will always return True.
            If obj is passed in, this method won’t check for a permission for the model, but for this specific object.
        '''
        return self.is_admin
    

    # https://docs.djangoproject.com/en/5.1/ref/contrib/auth/#:~:text=the%20specific%20object.-,has_module_perms
    def has_module_perms(self, app_label):
        '''
            Returns True if the user has any permissions in the given package (the Django app label). If the user is inactive, this method will always return False. For an active superuser, this method will always return True.    
        '''
        return True

class UserProfile(models.Model):
    # As we want only one UserProfile to be associated with an individual User, hence used OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prifile_picture = models.ImageField(upload_to='user/profile_pictures', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='user/cover_photos', null=True, blank=True)
    address_line_1 = models.CharField(max_length=50, null=True, blank=True)
    address_line_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    State = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email