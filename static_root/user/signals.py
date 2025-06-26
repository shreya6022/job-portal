from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver
from user.models import CreatorProfile,SeekerProfile,CustomUser
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django import forms
User=get_user_model()
from django.contrib.auth.models import AbstractUser
import traceback



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Signal Triggered: {instance.username}, Created: {created},User Type: {instance.user_type}")

        if instance.user_type == "Creator":
            CreatorProfile.objects.create(user_connected=instance)
            print(f"✅ CreatorProfile created for {instance.username}")
        elif instance.user_type == "Seeker":
            SeekerProfile.objects.create(user_connected=instance)
            print(f"✅ SeekerProfile created for {instance.username}")

    else:
        print(f"⚠️ Ignoring extra signal for {instance.username}")

@receiver(user_logged_in)
def redirect_after_login(sender, request, user, **kwargs):
     # Redirect to seeker profile
    if user.user_type == 'Creator' and user.is_superuser:
    # Add the code to redirect to the admin panel here
        request.session['redirect_to'] = '/admin/'
    elif user.user_type == 'Seeker' and user.is_superuser:
    # Add the code to redirect to the admin panel here
        request.session['redirect_to'] = '/admin/'
    elif user.user_type == 'Creator':
        request.session['redirect_to'] = 'cp' 
    elif user.user_type == 'Seeker':
        request.session['redirect_to'] = 'sp'              
    