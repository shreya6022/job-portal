from django.db import models
from creator.models import BaseModel
from django.core.validators import RegexValidator
from django.conf import settings
import traceback 
# Create your models here.



from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
    ('Seeker', 'Seeker'),
    ('Creator', 'Creator')]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default="Creator" )
    password=models.CharField(max_length=200)
    username=models.CharField(max_length=50,unique="true")
    fi=models.CharField(max_length=50,default='radha')
    ln=models.CharField(max_length=50,default='shrama')

    
       
    def __str__(self):
        return self.username
 


# Creator Profile
class CreatorProfile(BaseModel):
    name = models.CharField(max_length=100)
    user_connected = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # Validators should be a list


class SeekerProfile(BaseModel):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    user_connected = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # Validators should be a list
    email=models.EmailField(max_length=50,default='no-reply@example.com',)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='pending',)
    image=models.FileField()

class addjob(BaseModel):
    user_connected = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30)
    job_title = models.CharField(max_length=30)
    sdate = models.DateField()
    edate = models.DateField()
    salary = models.FloatField(max_length=20)
    experience = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    skills = models.CharField(max_length=50)
    descri = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title


   

    


