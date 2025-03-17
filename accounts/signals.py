from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile

# After saving an User this function will be called by the signal post_save send from the User model
@receiver(post_save, sender=User)
def post_save_create_user_profile_receiver(sender, instance, created, **kwargs):
    '''
        sender : the model from which the signal is coming
        instance: for which record, the signal is coming
        created: bool, if a new record is created returns True, else (if updated) returns False
    '''
    # if User is created then created=True
    if created:
        UserProfile.objects.create(user=instance)

    # if User gets updated then created=False
    else:
        # if UserProfile already exists and User model is updated
        try:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.save()
        
        # if User gets updated but for that user we don't have any UserProfile, then created one
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)