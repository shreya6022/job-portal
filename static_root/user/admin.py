from django.contrib import admin
from .models import CustomUser,CreatorProfile,SeekerProfile # Ensure CustomUser is imported correctly

admin.site.register(CustomUser)
admin.site.register(CreatorProfile)
admin.site.register(SeekerProfile)

# Register your models here.
