from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
