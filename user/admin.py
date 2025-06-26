from django.contrib import admin
from .models import CustomUser,CreatorProfile,SeekerProfile,JobAdd,JobApplication # Ensure CustomUser is imported correctly

admin.site.register(CustomUser)
admin.site.register(CreatorProfile)
admin.site.register(SeekerProfile)
admin.site.register(JobAdd)
admin.site.register(JobApplication)
# Register your models here.
