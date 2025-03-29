from django.db import models

from .utils import send_vendor_is_approved_email
from accounts.models import User, UserProfile

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    # OVERWRITING THE save() METHOD
    def save(self, *args, **kwargs):
        # checking if the record already exists
        if self.pk is not None: # if new entry then pk will be None and if updated the record then pk will not be Nont
            
            # getting the old record which we had before updating
            old_record = Vendor.objects.get(pk=self.pk)

            # checking if old is_approved and new is_approved are different or not
            if old_record.is_approved != self.is_approved:

                # checking if admin marked is_approved to True
                if self.is_approved == True:
                    mail_subject = 'Congratulations!! Your restaurant has been approved!!'

                # if admin marked is_approved to false
                else:
                    mail_subject = 'Sorry!! You are not allowed anymore to publish your restaurant on our marketplace!!'

                mail_template = 'accounts/email/vendor_admin_approval_status_change.html'
                context = {
                    'user' : self.user,
                    'is_approved' : self.is_approved
                }
                send_vendor_is_approved_email(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)

