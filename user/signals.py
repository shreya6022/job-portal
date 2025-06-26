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
   
        try:
            if "redirect_to" in request.session:
                return  
            if user.is_superuser:
                request.session['redirect_to'] = '/apanel'
            elif CreatorProfile.objects.filter(user_connected__username=user.username).exists():
                request.session['redirect_to'] = f'/creator/{user.username}/'
            elif SeekerProfile.objects.filter(user_connected__username=user.username).exists():
                request.session['redirect_to'] = f'/seeker/{user.username}/'
            else:
                request.session['redirect_to'] = '/reg/'  # Redirect to register if profile doesn't exist

        except Exception as e:
            print(f"Error in login redirect signal: {e}")
            request.session['redirect_to'] = '/reg' 


